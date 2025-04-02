# Base Prefect image
FROM prefecthq/prefect:3-python3.12

RUN echo "Debug: Building image"

# Set Prefect API URL
ENV PREFECT_API_URL=http://localhost:4200/api

# Expose the Prefect UI port
EXPOSE 4200

# Start the Prefect server
CMD ["prefect", "server", "start", "--host", "0.0.0.0", "--port", "4200"]