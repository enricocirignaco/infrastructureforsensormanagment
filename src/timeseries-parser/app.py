import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from SPARQLWrapper import SPARQLWrapper, POST
import json
import base64
import uuid
import config
from datetime import datetime

class MQTTClient:
    def __init__(self, proto_parser, fuseki_client, influx_client):
        """
        Initializes the MQTT client with the necessary configurations.
        """
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        self.proto_parser = proto_parser
        self.fuseki_client = fuseki_client
        self.influx_client = influx_client

    def connect(self):
        """
        Connects to the MQTT broker and starts listening for messages.
        """
        try:
            self.client.connect(config.MQTT_BROKER, config.MQTT_PORT)
            self.client.subscribe(config.MQTT_TOPIC)
            print("📡 Listening for MQTT messages...")
            self.client.loop_forever()
        except Exception as e:
            print(f"❌ Error connecting to MQTT broker: {e}")

    def disconnect(self):
        """
        Disconnects from the MQTT broker gracefully.
        """
        self.client.loop_stop()
        self.client.disconnect()
        print("🔌 Disconnected from MQTT broker.")

    def on_message(self, client, userdata, msg):
        """
        Callback function triggered when a message is received.
        Parses the payload and writes data to InfluxDB.
        """
        try:
            mqtt_payload = json.loads(msg.payload.decode("utf-8"))
            device_id = mqtt_payload.get("end_device_ids", {}).get("device_id")
            timestamp = mqtt_payload.get("received_at")
            frm_payload_b64 = mqtt_payload.get("uplink_message", {}).get("frm_payload")

            if not frm_payload_b64:
                print("⚠️ No 'frm_payload' found!")
                return

            frm_payload = base64.b64decode(frm_payload_b64)
            sensor_data = self.proto_parser.parse_payload(frm_payload, "SensorData") # Replace with dynamic naming
            fields = {field.name: value for field, value in sensor_data.ListFields()}

            if fields:
                self.influx_client.write_sensor_data(device_id, timestamp, fields)
                self.fuseki_client.insert_sensor_data(device_id, timestamp, fields)

        except Exception as e:
            print(f"❌ Error processing MQTT message: {e}")


class ProtobufParser():

    def __init__(self, schema_path):
        with open(schema_path, "rb") as f:
                self.descriptor_data = f.read()

    def parse_payload(self, payload, message_name):
        try:                        
            parsed_message = self._parse_payload_with_dynamic_schema(self.descriptor_data, message_name, payload)
            return parsed_message

        except Exception as e:
            print(f"❌ Protobuf Parsing Error: {e}")
            return None
        
    def _parse_payload_with_dynamic_schema(self, descriptor_bytes, message_full_name, payload_bytes):
        """
        Parst das Protobuf-Payload dynamisch anhand des zur Laufzeit geladenen Schemas.
        
        :param descriptor_bytes: Byte-Daten des FileDescriptorSet
        :param message_full_name: Vollqualifizierter Name der Nachricht (z. B. "meinpaket.SensorDaten")
        :param payload_bytes: Das rohe Protobuf-Payload als Bytes
        :return: Eine Instanz des geparsten Protobuf-Nachrichtenobjekts.
        """
        # Lade den FileDescriptorSet und erzeuge einen DescriptorPool
        pool = self._load_schema_from_bytes(descriptor_bytes)
        
        # Erzeuge die dynamische Message-Klasse anhand des Namens
        MessageClass = self._get_message_class(pool, message_full_name)
        
        # Erstelle eine Instanz der Nachricht und parse das Payload
        message_instance = MessageClass()
        message_instance.ParseFromString(payload_bytes)
    
        return message_instance
        
    def _load_schema_from_bytes(self, descriptor_bytes):
        """
        Lädt einen FileDescriptorSet aus den übergebenen Bytes
        und fügt die enthaltenen FileDescriptorProtos zu einem DescriptorPool hinzu.
        """
        file_desc_set = descriptor_pb2.FileDescriptorSet()
        file_desc_set.ParseFromString(descriptor_bytes)
        
        pool = descriptor_pool.DescriptorPool()
        for file_descriptor_proto in file_desc_set.file:
            pool.Add(file_descriptor_proto)
        return pool

    def _get_message_class(self, pool, message_full_name):
        """
        Holt anhand des vollqualifizierten Namens (z. B. "meinpaket.SensorDaten")
        die entsprechende Message-Klasse aus dem DescriptorPool.
        """
        message_descriptor = pool.FindMessageTypeByName(message_full_name)
        MessageClass = message_factory.GetMessageClass(message_descriptor)
        return MessageClass

class FusekiClient:
    def __init__(self):
        """
        Initializes the Fuseki client with endpoint and authentication details.
        """
        self.endpoint = config.FUSEKI_ENDPOINT
        self.user = config.FUSEKI_USER
        self.password = config.FUSEKI_PASSWORD
        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql.setHTTPAuth("BASIC")
        self.sparql.setCredentials(self.user, self.password)

    def insert_sensor_data(self, device_id, timestamp, sensor_values):
        """
        Inserts sensor data into the Fuseki triplestore following the SSN/SOSA ontology.
        
        :param device_id: Unique ID of the sensor
        :param timestamp: Timestamp of the measurement
        :param sensor_values: Dictionary with sensor readings (e.g., {'temperature': 22.5, 'humidity': 55})
        """
        time_str = datetime.fromisoformat(timestamp).isoformat()
        observation_id = f"obs_{uuid.uuid4()}"
        
        query = f"""
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ex: <http://example.org/sensor/>

        INSERT DATA {{
            ex:{observation_id} a sosa:Observation ;
                sosa:madeBySensor ex:{device_id} ;
                sosa:resultTime "{time_str}"^^xsd:dateTime ;
                {self._format_sensor_values(sensor_values)}
                .
        }}
        """
        
        self._execute_update(query)

    def _format_sensor_values(self, sensor_values):
        """
        Formats sensor values as RDF triples following SSN/SOSA.
        """
        triples = []
        for key, value in sensor_values.items():
            triples.append(f"sosa:hasResult [ a sosa:Result ; ex:{key} \"{value}\"^^xsd:float ] ;")
        return '\n'.join(triples)

    def _execute_update(self, query):
        """
        Executes a SPARQL UPDATE query.
        """
        try:
            self.sparql.setQuery(query)
            self.sparql.setMethod(POST)
            self.sparql.query()
            print("✅ Data successfully inserted into Fuseki.")
        except Exception as e:
            print(f"❌ Error inserting data into Fuseki: {e}")

class InfluxDBHandler:
    """
    A class to handle interactions with InfluxDB.
    """

    def __init__(self):
        """Initializes the connection to InfluxDB."""
        self.client = InfluxDBClient(
            url=config.INFLUX_URL,
            token=config.INFLUX_TOKEN,
            org=config.INFLUX_ORG
        )
        self.write_api = self.client.write_api()

    def write_sensor_data(self, device_id, timestamp, fields):
        """
        Writes sensor data to InfluxDB.

        :param device_id: ID of the sensor device
        :param timestamp: Timestamp of the measurement
        :param fields: Dict of all measured data
        """
        point = (
            Point("sensor_data")
            .tag("device_id", device_id)
            .time(timestamp)
        )
        for key, value in fields.items():
            point = point.field(key, value)

        self.write_api.write(bucket=config.INFLUX_BUCKET, org=config.INFLUX_ORG, record=point)

    def close(self):
        """Closes the connection to InfluxDB."""
        self.client.close()
        print("🔌 InfluxDB connection closed.")

def main():
    parser = ProtobufParser("schema/schema.desc")
    fuseki = FusekiClient()
    influxdb = InfluxDBHandler()
    mqtt_client = MQTTClient(parser, fuseki, influxdb)

    try:
        mqtt_client.connect()
    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        mqtt_client.disconnect()
        influxdb.close()

if __name__ == "__main__":
    main()
