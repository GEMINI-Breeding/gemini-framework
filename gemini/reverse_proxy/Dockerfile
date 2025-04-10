# Use the official Caddy image
FROM caddy:2.9.1

# Copy the Caddyfile into the container
COPY ./gemini/reverse_proxy/Caddyfile /etc/caddy/Caddyfile

# Expose the default Caddy ports (80 for HTTP, 443 for HTTPS)
EXPOSE 80
EXPOSE 443

# The default command for the Caddy image is `caddy run --config /etc/caddy/Caddyfile --adapter caddyfile`
# No need to specify CMD unless overriding the default behavior.
