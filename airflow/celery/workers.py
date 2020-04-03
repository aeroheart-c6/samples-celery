# -*- coding: utf-8 -*-
import functools
import logging
import os
from signal import Signals

from billiard import process
from celery import (
    platforms,
    worker
)
from celery.app.control import Control
from celery.apps import worker as workers
from celery.apps.worker import Worker as CeleryWorker
from celery.exceptions import (
    WorkerShutdown,
    WorkerTerminate,
)
from celery.worker import state as __
from kombu.utils.objects import cached_property


class Worker(CeleryWorker):
    def install_platform_tweaks(self, worker):
        super().install_platform_tweaks(worker)

        # end goal
        platforms.signals["SIGABRT"] = WorkerShutdownHandler(worker)



class WorkerShutdownHandler(object):
    def __init__(self, worker):
        self.worker = worker
        self.nodename = worker.hostname
        self.app = worker.app

        self.control = Control(app=self.app)

    def __call__(self, *args):
        print(f"Status of: {self.nodename}")
        with self.app.connection_for_read() as connection:
            print(self.control.broadcast("stats",
                connection=connection,
                destination=[self.nodename],
                reply=True
            ))

        print(f"Consumers closed for: {self.nodename}")
        self.halt()
        print(f"Marking tasks failed under: {self.nodename}")
        self.terminate()

    def halt(self):
        with self.app.connection_for_read() as connection:
            result = self.control.broadcast("active_queues",
                connection=connection,
                destination=[self.nodename],
                reply=True
            )

            print(result)

            result = self.control.broadcast("active",
                connection=connection,
                destination=[self.nodename],
                reply=True
            )

            print(result)

        # self.worker.pool.stop()

    def terminate(self):
        print("******************")
