# Use a smaller base image
FROM python:3.11

# Set the working directory
WORKDIR /gemini-framework

# Copy only requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt

# Install the requirements for the GEMINI REST API
RUN pip install --no-cache-dir -r requirements.txt

# Copy the complete GEMINI source code into the container
COPY . .

# Add GEMINI Framework to the PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/gemini-framework"

# Expose the port 8080
EXPOSE 8080

# Start the GEMINI REST API Flask application using waitress
# Use the shell form to execute a shell command that runs both processes
# litestar --app gemini.server.rest_api.src.app:app run --host 0.0.0.0 --port 8080 &

CMD ["litestar", "--app", "gemini.server.rest_api.src.app:app", "run", "--host", "0.0.0.0", "--port", "8080"]