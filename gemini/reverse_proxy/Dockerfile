# Use the official Traefik image as a base
FROM traefik:v3.3

# Expose the default ports used by Traefik
# 80: Default HTTP port for web traffic
# 8080: Default port for the Traefik API/Dashboard
EXPOSE 80 8080

# Set the default command to run when the container starts
# --api.insecure=true: Enables the API/Dashboard without authentication (use with caution)
# --providers.docker: Enables Docker as a configuration provider
CMD ["--api.insecure=true", "--providers.docker"]
