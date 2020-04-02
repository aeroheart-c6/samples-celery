from argparse import ArgumentParser

from celery.bin import worker

import airflow.app


def worker(arguments):
    instance = worker.worker(app=airflow.app.celery)
    instance.run(optimization="fair")


def stats(arguments):
    pass


class Entrypoint(object):
    @classmethod
    def configure(cls):
        parser = ArgumentParser()

        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.required = True

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
