#!/bin/bash

# Start another process (replace with your actual command)
echo "Starting Worker"
saq gemini.rest_api.worker.settings &


echo "Starting GEMINI REST API"
# Start the GEMINI REST API Flask application in the background
litestar --app gemini.rest_api.src.app:app run --host 0.0.0.0 --port 8080 &



# Wait for all background processes to finish
wait