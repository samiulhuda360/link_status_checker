from celery import shared_task
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from .models import Link  

import logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def normalize_url(url):
    """Normalize URLs for comparison."""
    return url.replace('http://', 'https://').replace('www.', '').rstrip('/')

def inspect_links(target_url, link_to, anchor_text):
    print(link_to)
    proxies = {
        "http": "http://letezcbn-rotate:6792gwkuo8oo@p.webshare.io:80/",
        "https": "http://letezcbn-rotate:6792gwkuo8oo@p.webshare.io:80/"
    }

    try:
        result = requests.get(link_to, proxies=proxies)
        if result.status_code in [404, 400, 500]:
            return 'Source Removed', datetime.now().date()

        page_content = result.text
        soup = BeautifulSoup(page_content, 'html.parser')
        normalized_target_url = normalize_url(target_url)
        
        for link in soup.find_all('a', href=True):
            href = normalize_url(link['href'])
            if href == normalized_target_url and link.text.strip().lower() == anchor_text.lower():
                return ('Nofollow' if 'nofollow' in link.get('rel', '') else 'Dofollow'), datetime.now().date()
                
        return 'Link Removed', datetime.now().date()
    except Exception as e:
        return 'Source Removed', datetime.now().date()  # Broad exception for simplicity
@shared_task
def crawl_and_update_links():
    logger.info("Starting crawl_and_update_links task")
    links_to_check = Link.objects.iterator()  # Or filter based on your criteria

    for link in links_to_check:
        if not link.manual_edit:
            try:
                status, last_crawl = inspect_links(
                    link.target_link,
                    link.link_to,
                    link.anchor_text
                )
                
                link.status_of_link = status
                link.last_crawl_date = last_crawl
                print(link.status_of_link)
                link.save()
                
            except Exception as e:
                logger.error(f"Error during task execution: {e}")
            logger.info("Finished crawl_and_update_links task")