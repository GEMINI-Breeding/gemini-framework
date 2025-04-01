FROM python:3.12-slim

RUN echo "Debug: Building image"

# # Install poetry
RUN pip install poetry

# Add Code location for dagster
WORKDIR /opt/dagster/app

# Install poetry dependencies
COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

# Copy scheduler code into the container
COPY gemini ./gemini

# Add GEMINI Framework to the PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/opt/dagster/app"

# Expose dagster code server
EXPOSE 4000

# Start the dagster code server
# CMD allows this to be overridden from run launchers or executors to execute runs and steps
CMD ["dagster", "code-server", "start", "-h", "0.0.0.0", "-p", "4000", "-f", "./gemini/scheduler/app/definitions.py"]

