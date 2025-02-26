# Get Bitnami PostgreSQL image
FROM bitnami/postgresql:16

USER root

# Install Dependencies
RUN apt-get update && apt-get install -y \
    lsb-release \
    gcc \
    make \
    libssl-dev \
    autoconf \
    pkg-config \
    libcurl4-gnutls-dev \
    liblz4-dev \
    libzstd-dev \
    git

# Copy setup script to PostgreSQL's pre-initialization directory
COPY ./setup.sh /scripts/setup.sh
RUN chmod +x /scripts/setup.sh && chown 1001:1001 /scripts/setup.sh

# Run the setup script
RUN /scripts/setup.sh

# Copy SQL scripts to initialize the database
COPY ./init_sql /docker-entrypoint-initdb.d/
RUN chown -R 1001:1001 /docker-entrypoint-initdb.d/

# Switch back to PostgreSQL user
USER 1001
