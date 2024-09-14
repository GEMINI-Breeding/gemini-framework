FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagster-webserver dagster-postgres dagster-aws

COPY /gemini/server/scheduler/ /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/dagster_home

COPY /gemini/server/scheduler/dagster.yaml /opt/dagster/dagster_home/dagster.yaml

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT [ "dagster-webserver" , "-h", "0.0.0.0", "-p", "3000" ]

