FROM postgres:14

# Custom ENV Variables
ARG GEMINI_SCHEDULER_DB_USER="gemini"
ARG GEMINI_SCHEDULER_DB_PASSWORD="gemini"
ARG GEMINI_SCHEDULER_DB_NAME="gemini"
ARG GEMINI_SCHEDULER_DB_HOSTNAME="scheduler-db"
ARG GEMINI_SCHEDULER_DB_PORT="6432"

# Copy the environment variables for PostgreSQL
ENV POSTGRES_USER=${GEMINI_SCHEDULER_DB_USER}
ENV POSTGRES_PASSWORD=${GEMINI_SCHEDULER_DB_PASSWORD}
ENV POSTGRES_DB=${GEMINI_SCHEDULER_DB_NAME}
ENV POSTGRES_PORT=${GEMINI_SCHEDULER_DB_PORT}

# Expose the PostgreSQL port
EXPOSE 6432

# Start PostgreSQL
CMD ["postgres", "-c", "max_connections=200", "-c", "shared_buffers=128MB", "-c", "effective_cache_size=384MB", "-c", "wal_level=logical", "-p", "6432"] 
