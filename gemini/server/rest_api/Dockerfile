
# Use a smaller base image
FROM python:3.11

# Custom ENV Variables
ARG GEMINI_ENV="development"
ARG GEMINI_API_PORT="7777"
ARG GEMINI_API_USER="gemini"
ARG GEMINI_API_PASSWORD="gemini"
ARG GEMINI_API_DEBUG="True"
ARG GEMINI_API_HOSTNAME="gemini-api"

# Set the environment variables
ENV IS_REMOTE="True"
ENV GEMINI_ENV=${GEMINI_ENV}
ENV GEMINI_API_PORT=${GEMINI_API_PORT}
ENV GEMINI_API_USER=${GEMINI_API_USER}
ENV GEMINI_API_PASSWORD=${GEMINI_API_PASSWORD}
ENV GEMINI_API_DEBUG=${GEMINI_API_DEBUG}

# Set the working directory
WORKDIR /gemini-framework

# Copy only requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt

# Non-GPU Pytorch installation
RUN pip install --no-cache-dir torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# Install the requirements for the GEMINI REST API
RUN pip install --no-cache-dir -r requirements.txt

# Copy the complete GEMINI source code into the container
COPY . .

# Add GEMINI Framework to the PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/gemini-framework"

# Expose GEMINI API port
EXPOSE ${GEMINI_API_PORT}

# Keep the container running
CMD ["tail", "-f", "/dev/null"]

# Start the GEMINI REST API Flask application using waitress
# CMD ["litestar", "--app", "gemini.server.rest_api.src.app:app", "run", "--host", "0.0.0.0", "--port", ${GEMINI_API_PORT}]
