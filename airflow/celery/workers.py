# -*- coding: utf-8 -*-
import functools
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

        callback = WorkerShutdownHandler(
            app=self.app,
            nodename=self.hostname,
        )

        # end goal
        platforms.signals["SIGSTOP"] = callback



class WorkerShutdownHandler(object):
    def __init__(self, app, nodename):
        self.nodename = nodename
        self.app = app

        self.control = Control(app=app)

    def __call__(self, worker):
        print(f"Marking tasks failed under: {self.nodename}")
        self.halt()
        self.terminate()

    def get_queues(self):
        # Get queues to halt
        print(f"Getting queues for: {self.nodename}")
        results = self.control.broadcast("active_queues",
            reply=True,
            destination=[self.nodename]
        )

        import json
        print(json.dumps(results, indent=4))

        try:
            queues = results[0][self.nodename]
            queues = [queue["name"] for queue in queues]
        except (IndexError, KeyError) as exception:
            print(str(exception))
            queues = []

        return queues

    def halt(self):
        queues = self.get_queues()

        for queue in queues:
            print(f"Cancelling consumer for queue: {queue}")
            results = self.control.broadcast("cancel_consumer",
                reply=True,
                destination=[self.nodename],
                arguments={"queue": queue}
            )

    def terminate(self):
        pass

    def shutdown(self):
        pass
