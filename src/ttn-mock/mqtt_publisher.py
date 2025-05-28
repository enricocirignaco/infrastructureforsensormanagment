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
DEVICE_ID = os.getenv("DEVICE_ID", "cubecell-1")
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", f"v3/leaf-link-mock@ttn/devices/{DEVICE_ID}/up")
INTERVAL = int(os.getenv("PUBLISH_INTERVAL_SEC", 20))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(
    os.getenv("MQTT_USERNAME", "admin"),
    os.getenv("MQTT_PASSWORD", "admin1234"),
)

def generate_frm_payload():
    """Generates a Base64-encoded sensor payload with random values."""
    sensor_data = schema_pb2.Msg_ba60aa1c3a024f7691ef43739f570062()
    sensor_data.temp1 = random.randint(0, 30)
    sensor_data.temp2 = random.randint(0, 30)
    sensor_data.hum1 = random.randint(10, 60)

    return base64.b64encode(sensor_data.SerializeToString()).decode("utf-8")


def load_template(path="template.json"):
    """Loads the JSON message template."""
    with open(path, "r") as f:
        return json.load(f)


def main():
    result = client.connect(BROKER, PORT)
    if result == 0:
        print("✅ Connected successfully!")
    else:
        print(f"❌ Connection failed with code {result}")

    template = load_template()

    try:
        while True:
            template["end_device_ids"]["device_id"] = DEVICE_ID
            template["uplink_message"]["frm_payload"] = generate_frm_payload()
            template["received_at"] = datetime.now(ZoneInfo("Europe/Zurich")).isoformat()

            rc, mid = client.publish(TOPIC, json.dumps(template))
            if rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"✅ Published to {TOPIC}")
            else:
                print(f"❌ Publish failed with error code {rc}")
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
