FROM ghcr.io/hydradatabase/hydra:15

# Custom ENV Variables
ARG GEMINI_DB_USER="gemini"
ARG GEMINI_DB_PASSWORD="gemini"
ARG GEMINI_DB_NAME="gemini"
ARG GEMINI_DB_HOSTNAME="db"

# Copy the environment variables for PostgreSQL
ENV POSTGRES_USER=${GEMINI_DB_USER}
ENV POSTGRES_PASSWORD=${GEMINI_DB_PASSWORD}
ENV POSTGRES_DB=${GEMINI_DB_NAME}


# Expose the PostgreSQL port
EXPOSE 5432

# Copy GEMINI SQL Scripts for Database Initialization
COPY ./gemini/server/database/sql_scripts /docker-entrypoint-initdb.d/

# Configure PostgreSQL 
RUN echo "listen_addresses='*'" >> /etc/postgresql/postgresql.conf
RUN echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/pg_hba.conf

# Start PostgreSQL
CMD [ "postgres", "-c", "max_connections=1000", "-c", "shared_buffers=256MB", "-c", "effective_cache_size=768MB", "-c", "wal_level=logical"]

