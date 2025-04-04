import os

MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'mock-v3/internet-of-soils-playground@ttn/devices/cubecell-1/up')

FUSEKI_ENDPOINT = os.getenv('FUSEKI_ENDPOINT', 'http://localhost:3030/testing/update')
FUSEKI_USER = os.getenv('FUSEKI_USER', 'admin')
FUSEKI_PASSWORD = os.getenv('FUSEKI_PASSWORD', 'admin1234')

INFLUX_URL = os.getenv('INFLUX_URL', 'http://localhost:8086')
INFLUX_TOKEN = os.getenv('INFLUX_TOKEN', '')
INFLUX_ORG = os.getenv('INFLUX_ORG', 'bfh')
INFLUX_BUCKET = os.getenv('INFLUX_BUCKET', 'default')
