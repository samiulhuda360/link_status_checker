from celery import shared_task
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from .models import Link  
from celery.utils.log import get_task_logger
from celery import group



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
        "User-Agent": "Mozilla/5.0"
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

@shared_task
def crawl_and_update_links():
    logger.info("Starting crawl_and_update_links task")
    links_to_check = Link.objects.all().values_list('id', flat=True)
    
    # Create a group of subtasks to process each link independently
    job = group(crawl_single_link.s(link_id) for link_id in links_to_check)
    result = job.apply_async()
    
    logger.info("Finished scheduling crawl_and_update_links task")