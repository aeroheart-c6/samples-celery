# -*- coding: utf-8 -*-
from airflow.celery.apps import Celery


celery = Celery("airflow-worker", config_source={
    "broker_url": "redis://redis:6379/0",
    "broker_pool_limit": 0,
    "worker_concurrency": 5,
    "worker_prefetch_multiplier": 1
    "task_acks_late": True,
    "task_default_queue": "default",
    "task_default_exchange": "default"
})


@app.task
def add(a, b):
    print(f"{a} + {b} = {a + b}")


@app.task
def long_running(duration):
    print(f"Sleeping for {duration}s")
    time.sleep(duration)
    print("Woken up")
