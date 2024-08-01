FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagster-webserver dagster-postgres dagster-aws

COPY /gemini/server/scheduler/ /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/dagster_home

COPY /gemini/server/scheduler/dagster.yaml /opt/dagster/dagster_home/dagster.yaml

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT [ "dagster-webserver" , "-h", "0.0.0.0", "-p", "3000" ]



# FROM python:3.10-slim

# # Change working directory
# WORKDIR /usr/src/app
# ENV DAGSTER_HOME=/usr/src/app

# # Install dependencies
# COPY ./requirements.txt ./requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the gemini source code
# COPY . .

# # Add GEMINI Framework to the PYTHONPATH
# ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

# ENV DAGSTER_WORKSPACE_PATH "/usr/src/app/gemini/server/scheduler/workspace.yaml"

# # Run Dagit
# CMD ["dagit", "-w", ${DAGSTER_WORKSPACE_PATH}, "-h", "0.0.0.0", "-p", "3000"]

