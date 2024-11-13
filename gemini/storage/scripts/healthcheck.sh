#!/bin/bash

# Healthcheck script for MinIO
curl -f "http://localhost:9000/minio/health/live" || exit 1