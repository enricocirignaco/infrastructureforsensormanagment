#!/bin/sh

PASSWD_FILE="/mosquitto/config/pwfile"
TTN_BRIDGE_FILE="/mosquitto/config/bridges/ttn-bridge.conf"

# Generate password file if it does not exist
if [ ! -f "$PASSWD_FILE" ]; then
  echo "[INFO] No password file found. Creating new one..."
  
  if [ -z "$MQTT_USERNAME" ] || [ -z "$MQTT_PASSWORD" ]; then
    echo "[ERROR] MQTT_USERNAME and MQTT_PASSWORD must be set to create a password file."
    exit 1
  fi

  mosquitto_passwd -b -c "$PASSWD_FILE" "$MQTT_USERNAME" "$MQTT_PASSWORD"
  echo "[INFO] Password file created at $PASSWD_FILE"
fi

# Create bridge configuration file at first run
mkdir -p /mosquitto/config/bridges
if [ ! -f "$TTN_BRIDGE_FILE" ]; then
  echo "[INFO] No TTN bridge configuration file found. Creating new one..."
  
  if [ -z "$TTN_USERNAME" ] || [ -z "$TTN_PASSWORD" ]; then
    echo "[ERROR] TTN bridge configuration variables must be set to create a bridge file."
    exit 1
  fi

  cat <<EOF > "$TTN_BRIDGE_FILE"
connection ttn_bridge
address eu1.cloud.thethings.network:8883
topic # in 2
try_private false
start_type automatic
bridge_cafile /etc/ssl/certs/ca-certificates.crt
bridge_insecure false
remote_username $TTN_USERNAME
remote_password $TTN_PASSWORD
EOF
    echo "[INFO] TTN bridge configuration file created at $TTN_BRIDGE_FILE"
fi

exec mosquitto -c /mosquitto/config/mosquitto.conf