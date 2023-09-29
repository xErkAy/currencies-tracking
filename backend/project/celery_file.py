# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import django

from celery import Celery
from django.core import management
from project import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

app = Celery('project')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **_kwargs):
    for name, crontab in settings.PERIODIC_TASKS:
        sender.add_periodic_task(
            crontab,
            run_command.s(name)
        )


@app.task
def run_command(name):
    management.call_command(name)


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
