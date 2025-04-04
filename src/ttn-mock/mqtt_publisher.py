"""
Mock MQTT Sensor Data Publisher for TTN

Simulates sensor data and publishes it to an MQTT broker at regular intervals.
"""

import json
import base64
import time
import random
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import paho.mqtt.client as mqtt
from schema import schema_pb2

# MQTT Configuration
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "mock-v3/internet-of-soils-playground@ttn/devices/cubecell-1/up")
INTERVAL = int(os.getenv("PUBLISH_INTERVAL_SEC", 20))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)


def generate_frm_payload():
    """Generates a Base64-encoded sensor payload with random values."""
    sensor_data = schema_pb2.SensorData()
    sensor_data.firmwareVersion = 1
    sensor_data.temp1 = random.randint(-10, 30)
    sensor_data.temp2 = random.randint(-10, 30)
    sensor_data.hum1 = random.randint(10, 60)

    return base64.b64encode(sensor_data.SerializeToString()).decode("utf-8")


def load_template(path="template.json"):
    """Loads the JSON message template."""
    with open(path, "r") as f:
        return json.load(f)


def main():
    template = load_template()

    try:
        while True:
            template["uplink_message"]["frm_payload"] = generate_frm_payload()
            template["received_at"] = datetime.now(ZoneInfo("Europe/Zurich")).isoformat()

            client.publish(TOPIC, json.dumps(template))
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
