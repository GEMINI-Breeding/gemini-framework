FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt /opt/dagster/app/requirements.txt
RUN pip install --no-cache-dir -r /opt/dagster/app/requirements.txt

# Copy the complete GEMINI source code into the container
COPY . /opt/dagster/app

# Add /opt/dagster/app to the PYTHONPATH
ENV PYTHONPATH=/opt/dagster/app:$PYTHONPATH
ENV DAGSTER_HOME=/opt/dagster/dagster_home

COPY /gemini/server/scheduler/dagster.yaml /opt/dagster/dagster_home/dagster.yaml

WORKDIR /opt/dagster/app/gemini/server/scheduler

EXPOSE 3000

ENTRYPOINT [ "dagster-webserver" , "-h", "0.0.0.0", "-p", "3000" ]

