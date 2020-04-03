import logging
import os
from argparse import ArgumentParser
from signal import Signals

from celery.app.control import Control
from celery.bin import worker as worker_celery

import airflow.app
import airflow.utils


logging.basicConfig(**{
    "level": logging.INFO,
    "format": "[%(asctime)s] %(levelname)s - %(message)s"
})

def execute_task(arguments):
    logging.info("Running sleeper task for: %ss", arguments.duration)
    airflow.app.sleeper.apply_async(args=(arguments.duration,))


def worker_abort(arguments):
    nodename = f"celery@{airflow.utils.get_hostname()}"

    control = Control(app=airflow.app.celery)
    results = control.broadcast("stats", reply=True, destination=[nodename])

    proc_id = results[0][nodename]["pid"]

    logging.info("Sending SIGABRT (%s) to worker process ID: %s", Signals.SIGABRT, proc_id)
    os.kill(proc_id, Signals.SIGABRT)


def worker(arguments):
    instance = worker_celery.worker(app=airflow.app.celery)
    instance.run(optimization="fair")


def stats(arguments):
    control = Control(app=airflow.app.celery)

    nodename = f"celery@{airflow.utils.get_hostname()}"

    logging.info("Getting node stats")
    logging.info(control.broadcast("stats", reply=True, destination=[nodename]))

    logging.info("Getting active queues")
    logging.info(control.broadcast("active_queues", reply=True, destination=[nodename]))

    logging.info("Getting active tasks")
    logging.info(control.broadcast("active", reply=True, destination=[nodename]))



class Entrypoint(object):
    @classmethod
    def configure(cls):
        parser = ArgumentParser()

        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.required = True

        # configure `run` subcommand
        subparser = subparsers.add_parser("execute-task")
        subparser.add_argument("duration", **{
            "default": 10,
            "nargs": "?",
            "type": int,
        })
        subparser.set_defaults(func=execute_task)

        # configure `worker-abort` command
        subparser = subparsers.add_parser("worker-abort")
        subparser.set_defaults(func=worker_abort)

        # configure `worker` subcommand
        subparser = subparsers.add_parser("worker")
        subparser.set_defaults(func=worker)

        # configure `stats` subcommand
        subparser = subparsers.add_parser("stats")
        subparser.set_defaults(func=stats)

        return parser

    @classmethod
    def start(cls):
        arguments = cls.configure().parse_args()
        arguments.func(arguments)
