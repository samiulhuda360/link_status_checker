from celery import shared_task
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from .models import Link, LinkStatusThreshold
from celery.utils.log import get_task_logger
from celery import group
from django.utils.timezone import now
from datetime import timedelta


logger = get_task_logger(__name__)

logger.info('Your log message')



def normalize_url(url):
    """Normalize URLs for comparison."""
    return url.replace('http://', 'https://').replace('www.', '').rstrip('/')

def inspect_links(target_url, link_to, anchor_text):
    logger.info(f"Inspecting link: {link_to} targeting {target_url} with anchor text '{anchor_text}'")
    proxies = {
        "http": "http://letezcbn-rotate:6792gwkuo8oo@p.webshare.io:80/",
        "https": "http://letezcbn-rotate:6792gwkuo8oo@p.webshare.io:80/"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
    }

    try:
        result = requests.get(link_to, proxies=proxies, headers=headers, timeout=10)
        logger.info(f"HTTP Status for {link_to}: {result.status_code}")
        if result.status_code >= 400:
            logger.warning(f"Source removed or inaccessible for {link_to} with status code: {result.status_code}")
            return 'Source Removed', datetime.now().date()

        soup = BeautifulSoup(result.text, 'html.parser')
        normalized_target_url = normalize_url(target_url)
        
        found = False
        for link in soup.find_all('a', href=True):
            href = normalize_url(link['href'])
            if href == normalized_target_url:
                link_text = link.text.strip().lower()
                rel = link.get('rel', [])
                link_status = 'Nofollow' if 'nofollow' in rel else 'Dofollow'
                logger.info(f"Link match found: {href} with anchor text '{link_text}' - {link_status}")
                if link_text == anchor_text.lower():
                    found = True
                    break
                else:
                    logger.debug(f"Anchor text mismatch: found '{link_text}', expected '{anchor_text.lower()}'")
        
        if not found:
            logger.warning(f"Link not found or anchor text mismatch for target URL {target_url}")
            return 'Link Removed', datetime.now().date()
        
        return link_status, datetime.now().date()
    except requests.exceptions.ProxyError as e:
        logger.error(f"Proxy Error while inspecting links: {str(e)}")
        return 'Source Removed', datetime.now().date()
    except Exception as e:
        logger.error(f"Error while inspecting links: {str(e)}")
        return 'Error', datetime.now().date()
    
@shared_task
def crawl_single_link(link_id):
    link = Link.objects.get(id=link_id)
    if not link.manual_edit:
        status, last_crawl = inspect_links(link.target_link, link.link_to, link.anchor_text)
        logger.info(f"Updating link {link.link_to} status to {status}")
        link.status_of_link = status
        link.last_crawl_date = last_crawl
        link.save()

two_days_ago = now().date() - timedelta(days=2)

@shared_task
def crawl_and_update_links():
    logger.info("Starting crawl_and_update_links task")
    
    # Fetch thresholds for non-blank statuses and convert to a dictionary: {status: days_threshold}
    non_blank_status_thresholds = {
        threshold.status: threshold.days_threshold 
        for threshold in LinkStatusThreshold.objects.exclude(status='')
    }
    
    # Current time for comparison
    current_time = now()
    
    # Initialize an empty list to collect links to check
    links_to_check_ids = []

    # Handle non-blank statuses
    for status, days in non_blank_status_thresholds.items():
        # Calculate the threshold date for each status
        threshold_date = current_time - timedelta(days=days)
        
        # Fetch links that meet the threshold for non-blank statuses
        links_for_status = Link.objects.filter(
            last_crawl_date__lt=threshold_date, 
            status_of_link=status
        ).values_list('id', flat=True)
        
        # Extend the list of links to check
        links_to_check_ids.extend(links_for_status)

    # Explicitly include links with a blank or null 'status_of_link'
    links_with_blank_status = Link.objects.filter(
        Q(status_of_link='') | Q(status_of_link__isnull=True)
    ).values_list('id', flat=True)
    
    # Extend the list of links to check
    links_to_check_ids.extend(links_with_blank_status)

    # Remove potential duplicates
    links_to_check_ids = list(set(links_to_check_ids))

    # Log the IDs of links to be checked
    logger.info(f"Total links to be checked: {len(links_to_check_ids)} - IDs: {links_to_check_ids}")

    # If there are links to check, create subtasks
    if links_to_check_ids:
        # Create a group of subtasks to process each link independently
        job = group(crawl_single_link.s(link_id) for link_id in links_to_check_ids)
        result = job.apply_async()
        logger.info(f"Scheduled {len(links_to_check_ids)} links for crawling.")
    else:
        logger.info("No links to be crawled at this time.")

    logger.info("Finished scheduling crawl_and_update_links task")