FROM debian:stable-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install arduino-cli
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
RUN apt remove -y curl
RUN mkdir -p /source /output /config /logs

# Default command
CMD ["/usr/bin/arduino-cli", "version"]


