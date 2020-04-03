# -*- coding: utf-8 -*-
import logging

import setuptools
from setuptools import Command


logger = logging.getLogger(__name__)


def setup():
    setuptools.setup(
        name="airflow",
        version="0.0.0",
        packages=setuptools.find_packages(),
        scripts=["airflow/bin/airflow"],
        install_requires=[
            "celery==4.3.0",
            "pendulum==1.4.4",
            "redis==3.4.1",
        ],
        classifiers=[
            "Programming Language:: Python :: 3.6",
            "Topic :: Sample"
        ],
        python_requires=">=3.6.*"
    )



if __name__ == "__main__":
    setup()
