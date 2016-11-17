from __future__ import absolute_import

from celery import Celery
from django.conf import settings
from django.core.management import call_command

app = Celery('feti')

CELERY_TIMEZONE = settings.TIME_ZONE

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(name="update_search_index")
def update_search_index():
    call_command('update_index')
