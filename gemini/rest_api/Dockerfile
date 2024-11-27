FROM python:3.11

RUN echo "Debug: Building image"

# Install poetry
RUN pip install poetry

# Default ENV Values
ENV GEMINI_API_PORT="7777"
ENV GEMINI_API_USER="gemini"
ENV GEMINI_API_DEBUG="True"

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
EXPOSE 8080


# Poetry Shellz
# RUN poetry shell

# Keep Container Running
# CMD ["tail", "-f", "/dev/null"]

# # Start the GEMINI REST API LITESTAR application
CMD poetry run litestar --app gemini.rest_api.app:app run --host 0.0.0.0 --port 8080

