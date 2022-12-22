from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Store.settings')

celery_app = Celery('Store')

celery_app.autodiscover_tasks()

celery_app.conf.broker_url = ('')