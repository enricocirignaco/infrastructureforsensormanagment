# Documentation Draft
## Project Milestones
1. Konzept Phase (3 Wochen)
    - Lösungsvorschläge erstellen
    - Detailreiches Systemdiagramm
    - PoC gewisser Technologien
    - Datendiagramm
2. Infrastruktur (3 Wochen)
    - Dev Umgebung einrichten (Docker Infrastruktur)
    - Live-Daten von Sensorknoten bis in den Triplestore mit Flatbuffers
    - Kompilieren und und Flashen der Firmware über Browser
3. Frontend & Backend (4 Wochen)
    - User-Auth
    - Frontend Masken zur Erfassung und Anzeige der Daten
    - Backend als Middleware zwischen den Services
    - Implementation REST-Schittstelle
4. End-to-End Testing (2 Wochen)
    - Integration aller Systemteile, Services wie Grafana, Sparnatural etc.
    - Deployment in produktiver Umgebung
    - Testing des Systems durch Stakeholders
5. Feedback-Integration, Optionale Features (2 Wochen)
    - Implementation/Anpassung gewisser Systemkomponenten aufgrund Rückmeldung
    - Technischer Abschluss
6. Projekt Deadline (2 Wochen)
    - Fokus auf Abschluss der Dokumentation
    - Plakat, Bucheintrag, Präsentation, Film abschliessen

# Ursprüngliche Milestones

| SW    | KW    | Phase                                    |
|-------|-------|------------------------------------------|
| 1-3   | 8-10  | Konzept Phase                            |
| 4-6   | 11-13 | Infrastruktur, Live-Daten, Firmware      |
| 7-8   | 14-15 | Frontend & Backend                       |
| 9     | 16    | *Ferien*                                 |
| 10-11 | 17-18 | Frontend & Backend                       |
| 12-13 | 19-20 | End-to-End                               |
| 14-15 | 21-22 | Feedback-Integration, Optionale Features |
| 16-17 | 23-24 | Projekt Deadline                         |


# Sprint Planing

| Sprint   | SW           | KW    | Phase                                                                  |
|----------|--------------|-------|------------------------------------------------------------------------|
| Sprint 1 | 1,2,3        |       | Konzept Phase, Toolchain, Systemdiagram, Requirements                  |
| Sprint 2 | (3),4,5,6,7? |       | Container-Infrastruktur, Timeseries-Parser, Compile-Engine             |
| Sprint 3 | 8,9          |       | Project, Sensor, Security, Groundwork                                  |
| Sprint 4 | 10,11        |       | Sensor-Node Template, Sensor Nodes                                     |
| Sprint 5 | 12,13        |       | Webserial/Script, Anbindung Compile-Engine / TTN, Protbuf-Service      |
| Sprint 6 | 14,15        |       |                                                                        |
| Sprint 7 | 16,17        |       |                                                                        |


# Sprints tatsächlich

| Sprint   | SW           | KW    | Phase                                                                  |
|----------|--------------|-------|------------------------------------------------------------------------|
| Sprint 1 | 1,2,3        |       | Konzept Phase, Toolchain, Systemdiagram, Requirements                  |
| Sprint 2 | 4,5,6,7      |       | Container-Infrastruktur, Timeseries-Parser, Compile-Engine             |
| Sprint 3 | 8,9,10       |       | Project, Sensor, Security, Groundwork                                  |
| Sprint 4 | 11,12        |       | Sensor-Node Template, Sensor Nodes                                     |
| Sprint 5 | 13,14        |       | Webserial/Script, Anbindung Compile-Engine / TTN, Protbuf-Service      |
| Sprint 6 | 15,16        |       |                                                                        |
| Sprint 7 | 17           |       | **Keine Features mehr -> Film, Doku**  Nur noch Mo-Do                  |


## Deadlines
- **Abgabe Book-Eintrag noch unklar**
- 26.05.25 12:00 Abgabe Poster
- 12.06.25 18:00 Abgabe Film
- 12.06.25 18:00 Abgabe Dokumentation
## Requirements
### Funktionale Anforderungen
Prioritäten:
- Hoch
- Mittel
- Niedrig
- Optional

| Priorität | Requirement |
|-----------|------------|
|           | **Verwaltung und Darstellung von Sensorknoten und Projekten** |
| Hoch      | Die Webapplikation soll eine zentrale Verwaltung der Sensorknoten und Projekte ermöglichen und diese übersichtlich darstellen. |
| Mittel    | Projekte sollen als zentrale Organisationseinheit für Sensorknoten und Vorlagen verwendet werden. |
| Hoch      | Sensorknoten-Vorlagen sollen die einheitliche Erfassung von Sensorknoten gewährleisten und bieten die Möglichkeit Sensorknoten-spezifischen Konfiguration. |
| Hoch      | Sensorknoten sollen anhand von Vorlagen erstellt und mit relevanten Informationen verwaltet werden (z.B. Standort, Kalibrationsdaten). |
| Optional  | Sensordaten sollen in der Webapplikation visualisiert werden und als CSV exportiert werden können. |
|           | **Benutzer- und Zugriffsverwaltung** |
| Mittel    | In der Webapplikation werden zwischen drei verschiedenen Rollen unterschieden: <ul><li><i>Admin</i>: Kann neue Benutzer erfassen, Passwörter von Benutzern setzen und Rollen den Benutzern zuweisen.</li><li><i>Technician</i>: Write-Access, kann Sensorknoten und Projekte erstellen und bearbeiten.</li><li><i>Researcher</i>: Read-Access, kann die erstellten Daten nur lesen.</li></ul> |
| Mittel    | Die Nutzung der Webapplikation und der unterliegenden REST-Schnittstelle erfordert eine Authentifizierung. |
| Niedrig   | Ein Authentifizierungs- und Autorisierungskonzept soll implementiert werden. |
| Niedrig   | Benutzer sollen ihre Passwörter ändern können. |
|           | **Firmware-Management und Deployment** |
| Hoch      | Firmware für die Sensorknoten soll serverseitig parametrisiert und kompiliert werden. |
| Niedrig   | Die Compile-Engine soll auch für das Kompilieren von Firmware mit anderen Toolchains eingesetzt werden können. Das generische Kompilieren erfolgt über die Angabe eines konkreten Dockerbefehls. |
| Niedrig   | Die projektspezifische und die generische Kompilationsvarianten werden über separate Endpoints angesprochen. |
| Hoch      | Benutzer sollen Firmware über die Webapplikation direkt auf den Sensorknoten flashen können (WebSerial API). |
| Mittel    | Alternativ soll die parametrisierte Firmware heruntergeladen (Arduino-Code und Binary) und später manuell über die Arduino IDE geflasht werden können (z.B. bei fehlender Internetverbindung). |
| Hoch      | Beim Erfassen einer neuen Sensorknoten-Vorlage muss ein GitLab-Repository, sowie ein spezifischer Git-Tag als Default angegeben werden. Der Sourcecode soll vor dem Kompilieren aus diesem Repository bezogen werden. |
| Niedrig   | Beim Erfassen eines Sensorknoten kann die Version der Firmware (Git-Tag in der Vorlage) übersteuert werden. |
| Optional  | Ein Sensorknoten kann ein Update auf eine neue Firmware-Version erhalten. Die Messdaten sind an eine bestimmte Firmware-Version gebunden. |
|           | **Schnittstelle zu The Things Network (TTN)** |
| Hoch      | Projekte (Applikationen) und Sensorknoten (End Devices) sollen automatisch über die REST API von TTN provisioniert werden. |
| Hoch      | Erfasste Sensordaten sollen über LoRaWAN und TTN übertragen und per MQTT an das System übertragen werden. |
| Optional  | Sensordaten sollen nicht nur über MQTT, sondern auch über Webhooks an das Backend gesendet werden können. |
|           | **Datenpersistenz und -verarbeitung** |
| Hoch      | Relevante Projektdaten sollen in einem Linked Data Triple Store gespeichert werden. |
| Hoch      | Sensordaten sollen weiterhin zusätzlich in einer InfluxDB gespeichert werden. |
| Mittel    | Die Webapplikation soll eine REST API bereitstellen, die CRUD-Operationen für Projekte und Sensorknoten ermöglicht. |
| Optional  | Änderungen von Entitäten werden mit Zeitpunkt und Benutzer in einem Logbook im Triple Store gespeichert. |

### Nicht-funktionale Anforderungen
- Die Webapplikation soll als moderne *Single Page Application (SPA)* aufgebaut werden.
- Die REST API soll unabhängig von der Webapplikation entwickelt und nach RESTful-Prinzipien gestaltet werden.
- Beim Einsatz von Linked Data sollen geeignete Ontologien und Schemas verwendet werden.

### Abgrenzung
- Hardware-Identifikation von einzelnen Sensoren um Error-History zu verfolgen
- Daten-Löschung von nicht gebrauchten Entitäten / Fälschlicherweise erstellt
---


## TTN-Mock

For easier and more rapid development, we decided to create an additional microservice that mocks the timeseries data that would usually come from The Things Network over MQTT. There are multiple reasons why the use of "real data" that was sent from a microcontroller over LoraWAN is not really pratical during development:
- The hardware has always to be carried around and installed at a place that offers stable radio connection to a nearby LoRaWAN Gateway. Depending were the team members currently work, this condition might either be satisfied or not
- The duty cycle of *The Things Network* regulates how much airtime each device is allowed to occupy during a given time period. In most regions, the duty cycle is commonly defined as 1%. On top of that, there's also a fair use policy that limits the uplink airtime even further to **30 seconds per day and per node** [18]. During development the desired cadence of messages is about once per minutes as this allows to quickly adapt changes without flooding the system with messages. This frequency would violate the mentioned policies by far.
- The configuration of such a microservice can be adapted on the fly and is much faster compared to flashing the hardware with new firmware and waiting until the connection to TTN is working again

To follow the tech-stack that was already used in other microservices in this project, the TTN-Mock was developed with python, which enabled fast development of a first version. The idea of this microservice was to emulate a payload that is congruent to the one that the MQTT broker of TTN would provide. To achieve this, an actual uplink message, sent from our microcontroller, was extracted and slightly adapted. Specifically, the fields that later would be populated in the script were emptied (device_id, received_at and frm_payload) and the keys identifying the node were replaced with meaningless strings. The official documentation of TTN also states, that an additional field ``"simulated": true`` can be set to mark the message accordingly [19]. This message was then saved into a file called *template.json* to later get loaded by the python script.

To publish over the MQTT protocol, the widespread library *paho-mqtt* was used. It offers an easy-to-use client to authenticate and communicate with a broker. The service is fully configurable, meaning which broker and what topic the microservice should publish to can be set over environment variables at runtime.

notes:
- python dependencies
- protoc generated schema
- Dockerfile, Deployment


### References
[18] https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/  
[19] https://www.thethingsindustries.com/docs/integrations/data-formats/  

## Binary serialization
Instead of writing your own byte array or using JSON, for example, a binary serialization format should be used.
This has several clear advantages:
- Efficiency, serializing and deserializing data is significantly faster than with JSON, for example
- Development speed: As soon as the schema is defined, source code can be generated for various languages that handle reading and writing the data.
- Strongly Typed: Errors in the code can already be detected during compilation, as types are clearly defined.
- Schema: The clearly defined schema shows which data is available in which format. The schemas can be extended with defined mechanisms and are therefore versionable.

### Comparison

#### Protobufs
The older standard (originally from the 2000s), set in 2008 as an open source standard. Therefore also a very broad community and extensive tooling support. Established standard. The schema evolution is relatively simple, so adjustments to the data format can be made easily. The entire message is always read. Works best with small amounts of data (few MBs). Compared to FlatBuffers, it should be much more user-friendly (simple installation of the compiler, tutorials etc.). It is somewhat slower than FlatBuffers.

#### Nanopb
Is a very narrow, C implementation of Protobufs. It is optimized for 32-bit embedded systems with very few resources (<1kB RAM). It is optimized for low memory requirements and resource consumption. The schema definition of Protobufs can be adopted directly.

#### FlatBuffers
Also efficient with large amounts of data. The messages are read-only and can no longer be changed. If desired, only part of the data set can be deserialized. Often used in mobile gaming, where performance is very important and limited resources are available. More code is required to build a dataset compared to protobufs. Definitely one of the best libraries if the focus is on efficiency.

#### Further options
- Apache Avro: JSON-based schema. Central use in the Big Data area, but offers native functionality for data versioning. Not optimized for IoT, can lead to higher overhead and integration into resource-constrained environments can be cumbersome.
- MessagePack: Very simple protocol. It is not based on an external schema, which would make it difficult to define using data types. Very JSON-like, so would integrate with many programming languages. Due to the lack of a schema, validation and versioning of the data would be difficult, and the evolution of the schema would also be laborious.

#### Result
Protobufs (and Nanopb on the board) is used. The standard is well supported and code integration should be simple. The schema is in a textual format that can be easily generated. It is designed to transmit small amounts of data with little overhead and to comply with a schema. This is exactly our use case.

### Protobufs

### Protoc

The protobuf compiler (protoc) is mostly used to read `.proto` files and generating specific source code in various programming languages to either encode or decode protobuf messages. It is written in C++ an can either be manually compiled or be downloaded as a pre-built binary from the Github release page. [20]

Once the compiler is installed, it can be used to generate for example python code as following:

```bash
protoc --python_out=schema/ schema.proto
```

In this case, the generated file with the name *schema/schema_pb2.py*, 

The compiler will create a new file in the defined subfolder *schema/*, in this case with the name *schema_pb2.py*. Inside this newly created source file, the compiler will generate a module with static descriptors for each defined message type. With the help of python reflection / metaclasses, this will then provide a Python data access class at runtime. [21]  
More precisely, the .proto file lives as a binary string inside the generated module.

```python
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cschema.proto\....)
```

Therefore, the schema itself is not needed at runtime. But of course it should be kept because changing requirements may require adapting the message format and regenerating the python code.



```python
from schema import schema_pb2

sensor_data = schema_pb2.SensorData()
```


```bash
protoc --proto_path=. --descriptor_set_out=schema.desc schema1.proto schema2.proto
```

### Version
Add chapter about backwards compatibility of messages


### References
[20] https://github.com/protocolbuffers/protobuf
[21] https://protobuf.dev/programming-guides/editions/



## Provisioning over The Things Network API

Another responsibility of the backend service is to handle the communication with the TTN REST-API. Compared to the MQTT interface, which is used by the timeseries-parser to receive measured data, this API allows to programatically send CRUD (create, read, update, delete) actions which the user normally would do by hand over the web-console of TTN. A quick summary of the different data-entities on TTN helps to understand parallels between the webapplication and the LoRaWAN backbone. As the highest entity, *organizations* are responsible for user management and allow working together as a team. They can be used to group mutliple so called *applications*. An *application* is a lower-level logical entity which unites deployed hardware, handles incoming data and offers interfaces for external services to subscribe to this data flow. The lowest entities in this hierarchy are called *end devices* as they resemble the digital version of 

An initial design would have proposed to initialize a new application on TTN for each created project in the webapplication. This way, end-devices could have been logically grouped respecitvely separated from others that are part of another context. Naturally, this would only be visible when inspecting the initialzed end-devices directly over the web-console. However there exists one big drawback when creating multiple applications that would break the current architecture 

# Possible imporoovements
retrofit docker images with helatcheks
eindeutige identifikation vom firmaware in jede messpunkt. (compile engine hinzufügt git hash in config file und diese wird mit jede messpunkt mitgeschickt.)



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



#### References
[9]  https://heltec.org/project/htcc-ab01-v2/
Arduino, “arduino-create-agent,” GitHub repository, [Online]. Available: https://github.com/arduino/arduino-create-agent
Heltec Automation, “CubeCell-Arduino,” GitHub repository, [Online]. Available: https://github.com/HelTecAutomation/CubeCell-Arduino
Kaelhem, “AVRBRO – Web-based AVR Flasher,” GitHub repository, [Online]. Available: https://github.com/kaelhem/avrbro
Heltec Automation, “Downloads,” [Online]. Available: https://resource.heltec.cn/download/
Arduino, “Issue #150: Web Serial Conflicts,” GitHub, [Online]. Available: https://github.com/arduino/arduino-create-agent/issues/150

[27] Arduino, “Arduino Cloud Agent,” [Online]. Available: https://docs.arduino.cc/arduino-cloud/hardware/cloud-agent/