# MQTT-Broker

This broker acts as a bridge to the official TTN-Broker so that all messages can be accessed locally.

## Download CA-Certificate
This command downloads the ISRG Root X1 certificate to ensure secure TLS/SSL communication between the Mosquitto broker and The Things Network (TTN).
```
wget https://letsencrypt.org/certs/isrgrootx1.pem -O ttn-ca.pem
```

## Configure .env-mosquitto
In the main folder of this project, the following two variables have to be set in the  **.env-mosquitto** file to authenticate against the TTN MQTT-broker:
```
TTN_USERNAME=
TTN_PASSWORD=
``
