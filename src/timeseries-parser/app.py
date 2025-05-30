import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Graph, URIRef, Literal, RDF, Namespace, XSD, SOSA
import json
import base64
from uuid import uuid4
import config
from datetime import datetime

class MQTTClient:
    """
    Wrapper class to handle receiving and decoding of MQTT messages.
    Also delegates writing to databases to db-clients.
    """
    
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
            self.client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
            self.client.connect(config.MQTT_BROKER, config.MQTT_PORT)
            self.client.subscribe(config.MQTT_TOPIC)
            print("Listening for MQTT messages...")
            self.client.loop_forever()
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")

    def disconnect(self):
        """
        Disconnects from the MQTT broker gracefully.
        """
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker.")

    def on_message(self, client, userdata, msg):
        """
        Callback function triggered when a message is received.
        Parses the payload and writes data to InfluxDB.
        """
        try:
            # Step 1: Extract relevant data from MQTT message
            mqtt_payload = json.loads(msg.payload.decode("utf-8"))
            device_id = mqtt_payload.get("end_device_ids", {}).get("device_id") # equals uuid of sensor node
            timestamp = mqtt_payload.get("received_at")
            frm_payload_b64 = mqtt_payload.get("uplink_message", {}).get("frm_payload")

            if not frm_payload_b64:
                print("No 'frm_payload' found!")
                return

            frm_payload = base64.b64decode(frm_payload_b64)
            
            # Step 2: Get current File Descriptor from Fuseki
            file_descriptor: bytes = self.fuseki_client.read_filedescriptor()
            if not file_descriptor:
                raise RuntimeError("No file descriptor found in Fuseki.")
            
            # Step 3: Query matching message name from Fuseki 
            message_name = self.fuseki_client.find_message_name(device_id)
            
            # Step 4: Parse the protobuf payload by applying the File Descriptor
            sensor_data = self.proto_parser.parse_payload(payload=frm_payload, file_descriptor=file_descriptor, message_name=message_name)
            
            # Step 5: Gather all fields and write them into the triplestore and tsdb
            fields = {field.name: value for field, value in sensor_data.ListFields()}
            if fields:
                self.influx_client.write_sensor_data(device_id, timestamp, fields)
                self.fuseki_client.insert_sensor_data(device_id, timestamp, fields)

        except Exception as e:
            print(f"Error processing MQTT message: {e}")



class ProtobufParser():
    """
    Parses protobuf payloads using FileDescriptors to dynamically reflect required Python classes.
    """

    def parse_payload(self, payload: bytes, file_descriptor: bytes, message_name: str):
        try:
            parsed_message = self._parse_payload_with_dynamic_schema(file_descriptor, message_name, payload)
            return parsed_message
        except Exception as e:
            print(f"Protobuf Parsing Error: {e}")
            return None

    def _parse_payload_with_dynamic_schema(self, descriptor_bytes, message_full_name, payload_bytes):
        """
        Parses a protobuf payload dynamically using a schema loaded at runtime.

        :param descriptor_bytes: Byte data of the FileDescriptorSet
        :param message_full_name: Fully qualified name of the message (e.g., "mypackage.SensorData")
        :param payload_bytes: Raw protobuf payload as bytes
        :return: An instance of the parsed protobuf message object.
        """
        pool = self._load_schema_from_bytes(descriptor_bytes)
        MessageClass = self._get_message_class(pool, message_full_name)

        message_instance = MessageClass()
        message_instance.ParseFromString(payload_bytes)
        return message_instance

    def _load_schema_from_bytes(self, descriptor_bytes):
        """
        Loads a FileDescriptorSet from the given bytes
        and adds the contained FileDescriptorProtos to a DescriptorPool.
        """
        # FileDescriptorSet represents serialized collection of .proto files
        file_desc_set = descriptor_pb2.FileDescriptorSet()
        file_desc_set.ParseFromString(descriptor_bytes)

        # DescriptorPool acts as a container for all loaded message types
        pool = descriptor_pool.DescriptorPool()
        for file_descriptor_proto in file_desc_set.file:
            pool.Add(file_descriptor_proto)
        return pool

    def _get_message_class(self, pool, message_full_name):
        """
        Retrieves the corresponding message class from the DescriptorPool
        based on the fully qualified message name (e.g., "mypackage.SensorData").
        """
        # Use python reflection to produce runtime class for specified message
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
        self.sparql.setReturnFormat(JSON)
        
    def read_filedescriptor(self) -> bytes:
        query = """
        PREFIX bfh: <http://data.bfh.ch/>
        PREFIX schema: <http://data.bfh.ch/schema/>
        
        SELECT ?content
        WHERE {{
            ?fileDescriptor a bfh:ProtobufFileDescriptor ;
                bfh:binaryContent ?content .
        }} 
        """
        
        results = self._execucte_query(query)
        bindings = results['results']['bindings']
        if not bindings:
            raise RuntimeError('No file descriptor found in Fuseki.')
        
        base64_content = bindings[0]['content']['value']
        binary_content = base64.b64decode(base64_content)
        return binary_content
    
    def find_message_name(self, sensor_node_uuid: str) -> str:
        query = f"""
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?messageName WHERE {{
            ?sensorNode a bfh:SensorNode ;
                bfh:identifier "{sensor_node_uuid}" ;
                bfh:usesNodeTemplate ?nodeTemplate .
            ?nodeTemplate a bfh:NodeTemplate ;
                bfh:protobufMessageName ?messageName .
        }}
        """
        results = self._execucte_query(query)
        bindings = results['results']['bindings']
        if not bindings:
            raise RuntimeError('Message name not found for sensor node UUID: ' + str(sensor_node_uuid))

        return bindings[0]['messageName']['value']        

    def insert_sensor_data(self, device_id, timestamp, sensor_values):
        time_str = datetime.fromisoformat(timestamp).isoformat()
        observation_id = str(uuid4())
            
        g = Graph()
        g.bind("sosa", SOSA)
        g.bind("xsd", XSD)
        bfh = Namespace("http://data.bfh.ch/")
        g.bind("bfh", bfh)
        
        observation_uri = URIRef(f"http://data.bfh.ch/observations/{observation_id}")
        
        g.add((observation_uri, RDF.type, URIRef(SOSA.Observation)))
        g.add((observation_uri, SOSA.madeBySensor, URIRef(f"http://data.bfh.ch/sensorNodes/{device_id}")))
        g.add((observation_uri, SOSA.resultTime, Literal(time_str, datatype=XSD.dateTime)))
        
        for key, value in sensor_values.items():
            result_uri = URIRef(f"http://data.bfh.ch/results/{observation_id}_{key}")
            g.add((observation_uri, SOSA.hasResult, result_uri))
            g.add((result_uri, RDF.type, URIRef(SOSA.Result)))
            g.add((result_uri, bfh.fieldName, Literal(key)))
            g.add((result_uri, SOSA.hasSimpleResult, Literal(value)))
        
        query = f"""INSERT DATA {{ {g.serialize(format='nt')} }}"""
        self._execute_update(query)

    def _execute_update(self, query):
        """
        Executes a SPARQL UPDATE query.
        """
        try:
            self.sparql.setQuery(query)
            self.sparql.setMethod(POST)
            self.sparql.query()
        except Exception as e:
            print(f"Error inserting data into Fuseki: {e}")
            
    def _execucte_query(self, query) -> dict:
        """
        Executes a SPARQL SELECT query.
        """
        try:
            self.sparql.setQuery(query)
            return self.sparql.query().convert()
        except Exception as e:
            print(f"Error executing query in Fuseki: {e}")



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
        print("InfluxDB connection closed.")



def main():
    parser = ProtobufParser()
    fuseki = FusekiClient()
    influxdb = InfluxDBHandler()
    mqtt_client = MQTTClient(parser, fuseki, influxdb)

    try:
        mqtt_client.connect()
    except KeyboardInterrupt:
        print("Application terminated by user.")
    finally:
        mqtt_client.disconnect()
        influxdb.close()

if __name__ == "__main__":
    main()
