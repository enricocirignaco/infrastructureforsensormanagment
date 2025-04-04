#!/bin/sh

sed "s|\${TTN_USERNAME}|$TTN_USERNAME|g; s|\${TTN_PASSWORD}|$TTN_PASSWORD|g" \
    /mosquitto/config/mosquitto.template.conf > /mosquitto/config/mosquitto.conf

exec mosquitto -c /mosquitto/config/mosquitto.conf
