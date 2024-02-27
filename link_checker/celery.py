from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'link_checker.settings')

app = Celery('link_checker')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Explicitly set broker connection retries on startup
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'crawl_and_update_links_daily': {
        'task': 'link_crawler.tasks.crawl_and_update_links',
        'schedule': crontab(minute='*/5'),
    },
}