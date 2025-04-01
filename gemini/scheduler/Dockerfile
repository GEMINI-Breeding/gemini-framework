FROM python:3.12-slim

RUN pip install \
    dagster \
    dagster-graphql \
    dagster-postgres \
    dagster-webserver \
    dagster-docker \
    dagster-aws 

# Set $DAGSTER_HOME
ENV DAGSTER_HOME=/opt/dagster/dagster_home

# Create $DAGSTER_HOME
RUN mkdir -p $DAGSTER_HOME

# Copy dagster.yaml and workspace.yaml
COPY ./app/dagster.yaml ./app/workspace.yaml $DAGSTER_HOME

# Set the working directory
WORKDIR $DAGSTER_HOME