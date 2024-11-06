# Postgres 16
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

# Copy the SQL scripts to initialize the database
COPY ./init_sql /docker-entrypoint-initdb.d/

# Configure the PostgreSQL server
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Start the PostgreSQL server
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]