from celery import shared_task
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from .models import Link, LinkStatusThreshold, Index_checker_api
from celery.utils.log import get_task_logger
from celery import group
from django.utils.timezone import now
from datetime import timedelta
from django.core.cache import cache
import time
from urllib.parse import urlparse, urlunparse



logger = get_task_logger(__name__)


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

    # Normalize the link_to URL
    parsed_url = urlparse(link_to)
    if not parsed_url.scheme:
        link_to = urlunparse(('https', parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    elif parsed_url.scheme == 'http':
        link_to = link_to.replace('http://', 'https://', 1)

    try:
        result = requests.get(link_to, proxies=proxies, headers=headers, timeout=10)
        logger.info(f"HTTP Status for {link_to}: {result.status_code}")
        if result.status_code >= 400:
            logger.warning(f"Source removed or inaccessible for {link_to} with status code: {result.status_code}")
            return 'Source Removed', datetime.now().date(), link_to

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
            return 'Link Removed', datetime.now().date(), link_to

        return link_status, datetime.now().date(), link_to

    except requests.exceptions.ProxyError as e:
        logger.error(f"Proxy Error while inspecting links: {str(e)}")
        return 'Source Removed', datetime.now().date(), link_to
    except Exception as e:
        logger.error(f"Error while inspecting links: {str(e)}")
        return 'Error', datetime.now().date(), link_to

@shared_task
def crawl_single_link(link_id):
    link = Link.objects.get(id=link_id)
    if not link.manual_edit:
        status, last_crawl, normalized_link_to = inspect_links(link.target_link, link.link_to, link.anchor_text)
        logger.info(f"Updating link {link.link_to} status to {status}, crawl date to {last_crawl}, and link_to to {normalized_link_to}")
        link.status_of_link = status
        link.last_crawl_date = last_crawl
        link.link_to = normalized_link_to  # Update the link_to field with the normalized URL
        if status == 'Dofollow':
            link.address_status = '-'
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
        # Log the status and selected days
        logger.info(f"Processing status: {status}, Selected days: {days}")
        
        # Calculate the threshold date for each status
        threshold_date = current_time - timedelta(days=days)
        
        # Fetch links that meet the threshold for non-blank statuses
        links_for_status = Link.objects.filter(
            last_crawl_date__lt=threshold_date,
            status_of_link=status
        ).values_list('id', flat=True)
        
        # Log the link list for the current status
        logger.info(f"Links for status '{status}': {list(links_for_status)}")
        
        # Extend the list of links to check
        links_to_check_ids.extend(links_for_status)

    # Explicitly include links with a blank or null 'status_of_link'
    links_with_blank_status = Link.objects.filter(
    Q(status_of_link='') | Q(status_of_link__isnull=True) | Q(status_of_link='Error')
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
    
    
@shared_task
def check_url_index():
    logger.info("Index Checker Task Started")  # Task start log

    api_key = cache.get('index_checker_api_key')
    if not api_key:
        try:
            api_key_instance = Index_checker_api.objects.first()
            if api_key_instance:
                api_key = api_key_instance.key
                cache.set('index_checker_api_key', api_key, 3600)
                logger.info("API key fetched from database and stored in cache.")
            else:
                logger.error("API Key is not set in the database.")
                raise ValueError("API Key is not set in the database.")
        except Index_checker_api.DoesNotExist:
            logger.error("API Key model does not exist in the database.")
            raise ValueError("API Key is not set in the database.")
    
    # Fetching the index check interval
    try:
        interval_entry = LinkStatusThreshold.objects.get(status="Index_Check_Interval")
        days_threshold = interval_entry.days_threshold
        logger.info(f"Index check interval set to {days_threshold} days.")
    except LinkStatusThreshold.DoesNotExist:
        days_threshold = 10  # Default value if not set
        logger.info("Index_Check_Interval not found. Defaulting to 10 days.")

    threshold_date = now() - timedelta(days=days_threshold)
    links_to_check = Link.objects.filter(last_index_check__lt=threshold_date) | Link.objects.filter(last_index_check__isnull=True)

    logger.info(f"Total links to check: {links_to_check.count()}")

    for link in links_to_check:
        encoded_target_url = requests.utils.quote(link.link_to, safe='')
        search_query = f"site:{encoded_target_url}"
        api_endpoint = f"https://scraping.narf.ai/api/v1/?api_key={api_key}&url=https://www.google.co.uk/search?q={search_query}"

        logger.info(f"Checking index status for URL: {link.link_to}")

        response = requests.get(api_endpoint)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            search_div = soup.find('div', id='search')

            if search_div and any(link.link_to in a_tag['href'] for a_tag in search_div.find_all('a', href=True)):
                link.index_status = Link.index  # Mark as 'Indexed'
                logger.info(f"URL indexed: {link.link_to}")
            else:
                link.index_status = Link.not_index  # Mark as 'Not Indexed'
                logger.info(f"URL not indexed: {link.link_to}")

            link.last_index_check = now()
        else:
            link.index_status = Link.not_index  # Default if error occurs
            logger.error(f"Failed to check index status for URL: {link.link_to}. Response status: {response.status_code}")
            link.last_index_check = now()

        link.save()
        logger.info("Link status updated and saved.")
        time.sleep(10)  # Pause to avoid overwhelming the server or hitting rate limits

    logger.info("Index Checker Task Completed")
    
@shared_task
def check_selected_urls_index(link_ids):
    logger.info("Selected Index Checker Task Started")  # Task start log

    api_key = cache.get('index_checker_api_key')
    if not api_key:
        try:
            api_key_instance = Index_checker_api.objects.first()
            if api_key_instance:
                api_key = api_key_instance.key
                cache.set('index_checker_api_key', api_key, 3600)
                logger.info("API key fetched from database and stored in cache.")
            else:
                logger.error("API Key is not set in the database.")
                raise ValueError("API Key is not set in the database.")
        except Index_checker_api.DoesNotExist:
            logger.error("API Key model does not exist in the database.")
            raise ValueError("API Key is not set in the database.")
    
    # Only check links that have been specifically selected
    links_to_check = Link.objects.filter(id__in=link_ids)

    logger.info(f"Total selected links to check: {links_to_check.count()}")

    for link in links_to_check:
        encoded_target_url = requests.utils.quote(link.link_to, safe='')
        search_query = f"site:{encoded_target_url}"
        api_endpoint = f"https://scraping.narf.ai/api/v1/?api_key={api_key}&url=https://www.google.co.uk/search?q={search_query}"

        logger.info(f"Checking index status for selected URL: {link.link_to}")

        response = requests.get(api_endpoint)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            search_div = soup.find('div', id='search')

            if search_div and any(link.link_to in a_tag['href'] for a_tag in search_div.find_all('a', href=True)):
                link.index_status = Link.index  # Mark as 'Indexed'
                logger.info(f"URL indexed: {link.link_to}")
            else:
                link.index_status = Link.not_index  # Mark as 'Not Indexed'
                logger.info(f"URL not indexed: {link.link_to}")

            link.last_index_check = now()
        else:
            link.index_status = Link.not_index  # Default if error occurs
            logger.error(f"Failed to check index status for selected URL: {link.link_to}. Response status: {response.status_code}")
            link.last_index_check = now()

        link.save()
        logger.info("Selected link status updated and saved.")
        time.sleep(10)  # Pause to avoid overwhelming the server or hitting rate limits

    logger.info("Selected Index Checker Task Completed")