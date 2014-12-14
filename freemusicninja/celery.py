from celery import Celery
import iron_celery
from django.conf import settings

iron_celery  # iron_celery must be imported to inject the ironmq transport

app = Celery('freemusic')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
