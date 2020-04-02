FROM python:3.6-stretch

SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

ARG AIRFLOW_HOME=/home/airflow
ARG AIRFLOW_ROOT=${AIRFLOW_HOME}/airflow

ARG AIRFLOW_USER_ID=1000
ARG AIRFLOW_USER=airflow

ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

RUN useradd\
        -m\
        -s /bin/bash\
        -u ${AIRFLOW_USER_ID}\
        -d ${AIRFLOW_HOME}\
        ${AIRFLOW_USER}\
 && apt-get update -yqq\
 && apt-get install -yqq --no-install-recommends\
        apt-utils\
        vim\
        curl\
        tree

RUN pip install -U\
        pip\
        setuptools\
        wheel


WORKDIR ${AIRFLOW_ROOT}
COPY --chown=airflow:airflow airflow airflow
COPY --chown=airflow:airflow setup.py .

RUN pip install -e .

WORKDIR ${AIRFLOW_HOME}

EXPOSE 8000 8080
USER ${AIRFLOW_USER}

CMD ["airflow", "worker"]
