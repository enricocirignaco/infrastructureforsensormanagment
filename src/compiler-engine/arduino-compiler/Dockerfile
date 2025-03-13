FROM debian:stable-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install arduino-cli
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
RUN apt remove -y curl
RUN mkdir -p /source /output /logs /cache/arduino /cache/boards


# system wide configuation for arduino-cli
ENV DIRECTORIES_DATA=/cache/boards
ENV DIRECTORIES_USER=/cache/arduino
ENV LOGGING_FORMAT=json
ENV LOGGING_LEVEL=info
ENV METRICS_ENABLED=false
ENV OUTPUT_NO_COLOR=false
ENV SKETCH_ALWAYS_EXPORT_BINARIES=true
ENV UPDATER_ENABLE_NOTIFICATIONS=false
# ENV LOCALE=en_US.UTF-8        # Optional

WORKDIR /source
# Default command
CMD ["/usr/bin/arduino-cli", "version"]


