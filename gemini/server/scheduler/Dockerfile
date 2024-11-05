# Base Prefect image
FROM prefecthq/prefect:3.0.11-python3.11

# Custom ENV Variables
ARG GEMINI_SCHEDULER_SERVER_HOST="0.0.0.0"
ARG GEMINI_SCHEDULER_SERVER_HOSTNAME="scheduler"
ARG GEMINI_SCHEDULER_SERVER_PORT="4200"
ARG GEMINI_SCHEDULER_DB_CONNECTION_STRING="postgresql://gemini:gemini@db:6432/gemini"

# Add environment variables
ENV PREFECT_API_URL="http://${GEMINI_SCHEDULER_SERVER_HOST}:${GEMINI_SCHEDULER_SERVER_PORT}/api"
ENV PREFECT_API_DATABASE_CONNECTION_URL=${GEMINI_SCHEDULER_DB_CONNECTION_STRING}
ENV IS_REMOTE="True"

# Set the working directory
WORKDIR /gemini-framework

# Copy only requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt

# Non-GPU Pytorch installation
RUN pip install --no-cache-dir torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# Install the requirements for the GEMINI Scheduler
RUN pip install --no-cache-dir -r requirements.txt

# Copy the complete GEMINI source code into the container
COPY . .

# Add GEMINI Framework to the PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/gemini-framework"

# Expose the Scheduler API port
EXPOSE ${GEMINI_SCHEDULER_SERVER_PORT}

# Keep the container running
CMD ["tail", "-f", "/dev/null"]

# Start the GEMINI Scheduler
# CMD ["prefect", "server", "start", "--host", "${SCHEDULER_SERVER_HOST}, "--port", "${SCHEDULER_SERVER_PORT}"]


# FROM prefecthq/prefect:3.0.11-python3.11

# # Set the working directory
# WORKDIR /gemini-framework

# # Copy only requirements.txt first to leverage Docker cache
# COPY ./requirements.txt ./requirements.txt

# # Install the requirements for the GEMINI Scheduler
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the complete GEMINI source code into the container
# COPY . .

# # Add GEMINI Framework to the PYTHONPATH
# ENV PYTHONPATH "${PYTHONPATH}:/gemini-framework"

# CMD ["prefect", "server", "start", "--host", "0.0.0.0"]
