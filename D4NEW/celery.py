import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'D4NEW.settings')
app = Celery('D4NEW')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()