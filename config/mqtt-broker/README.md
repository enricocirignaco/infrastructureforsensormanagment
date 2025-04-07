# MQTT-Broker

This broker acts as a bridge to the official TTN-Broker so that all messages can be accessed locally.

## Configure local authentication

Anonymous access to the mqtt broker is disabled and therefor an user has to be created. First, create a file called **pwfile** in this directory.

```bash
touch pwfile
```

Then login interactively into the mqtt-broker container and create the user.

```bash
# Enter interactive shell in container
docker exec -it mqtt-broker sh

# Set better permissions for pwfile
chown mosquitto:mosquitto /mosquitto/config/pwfile
chmod 0600 /mosquitto/config/pwfile

# Create a new user and leave the container again
mosquitto_passwd -c /mosquitto/config/pwfile admin
exit

# Afterwards restart the container
docker compose restart mqtt-broker
```

## Configure Bridge to TTN

To receive all events from TTN, our mqtt broker has to be configured as a bridge. Because the bridge configuration must not be spread over multiple files and we do not commit passwords, a new file **ttn-bridge.conf** has to be create in the *bridges/* subfolder.

Copy the following content into the newly created file and set both username and password.

```
connection ttn_bridge
address eu1.cloud.thethings.network:8883
topic # in 2
try_private false
start_type automatic
bridge_cafile /etc/ssl/certs/ca-certificates.crt
bridge_insecure false
remote_username ....
remote_password ....
```

Afterwards restart the container:
```bash
docker compose restart mqtt-broker
```