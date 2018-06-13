from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_store.settings')

app = Celery('my_store')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
