# -*- coding: utf-8 -*-
from celery import Celery as CeleryApplication
from kombu.utils.objects import cached_property


class Celery(CeleryApplication):
    """
    Subclass on the celery application to instantiate the Airflow customer worker
    to override the sigquit handler
    """
    @cached_property
    def Worker(self):
        return self.subclass_with_self("airflow.celery.workers:Worker")
