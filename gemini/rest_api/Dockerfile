FROM python:3.12

RUN echo "Debug: Building image"

# Install poetry
RUN pip install poetry

# Set the working directory
WORKDIR /gemini-framework

# Install poetry dependencies
COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

# Copy the complete GEMINI source code into the container
COPY gemini ./gemini

# Add GEMINI Framework to the PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/gemini-framework"

# Expose GEMINI API port
EXPOSE 7777

# Expose Debugpy
EXPOSE 5678

# # Start the GEMINI REST API LITESTAR application
CMD poetry run litestar --app gemini.rest_api.app:app run --host 0.0.0.0 --port 7777

