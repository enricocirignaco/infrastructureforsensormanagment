FROM debian:stable-slim

# Install dependencies
RUN apt update && \
    apt install -y curl && \
    apt install -y python3 python3-pip && \
    apt install git unzip build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install arduino-cli
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
RUN apt remove -y curl
RUN mkdir -p /source /output /logs /cache/arduino /cache/boards


# system wide configuation for arduino-cli
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


