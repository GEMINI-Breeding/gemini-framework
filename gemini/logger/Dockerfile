FROM redis:latest

# Custom ENV Variables
ARG GEMINI_LOGGER_PASSWORD="gemini"
ARG GEMINI_LOGGER_PORT="6379"
ARG GEMINI_LOGGER_HOSTNAME="logger"

# Copy the environment variables for Redis
ENV REDIS_PASSWORD=${GEMINI_LOGGER_PASSWORD}
ENV REDIS_PORT=${GEMINI_LOGGER_PORT}

# Expose the Redis port
EXPOSE ${GEMINI_LOGGER_PORT}

# Start Redis
CMD ["redis-server"]