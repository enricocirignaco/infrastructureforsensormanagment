import json
import base64
import time
import random
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import paho.mqtt.client as mqtt

from schema import schema_pb2 

BROKER = os.getenv('MQTT_BROKER', 'localhost')
PORT = int(os.getenv('MQTT_PORT', 1883))
TOPIC = os.getenv('MQTT_TOPIC', 'mock-v3/internet-of-soils-playground@ttn/devices/cubecell-1/up')
INTERVAL = int(os.getenv('PUBLISH_INTERVAL_SEC', 20)) 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)

def generate_frm_payload():
    sensor_data = schema_pb2.SensorData()

    sensor_data.firmwareVersion = 1
    sensor_data.temp1 = 34
    sensor_data.temp2 = 23
    sensor_data.hum1 = 45

    # Serialisiere in Bytes
    serialized = sensor_data.SerializeToString()
    # Base64-kodiere die Bytes (TTN verwendet Base64 in frm_payload)
    b64_payload = base64.b64encode(serialized).decode('utf-8')
    return b64_payload

def load_template(path="template.json"):
    with open(path, "r") as f:
        return json.load(f)

def main():
    template = load_template()

    try:
        while True:
            template["uplink_message"]["frm_payload"] = generate_frm_payload()

            template["received_at"] = datetime.now(ZoneInfo("Europe/Zurich")).isoformat()

            # Optional: Aktualisieren Sie weitere Felder (z. B. counter oder Zeitstempel), falls gewünscht
            
            payload_str = json.dumps(template)
            client.publish(TOPIC, payload_str)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Beendet durch Benutzer")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
