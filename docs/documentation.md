# Documentation Draft
---
## Project Management
Project members:
- Linus Deggen - Developer
- Enrico Cirignaco - Developer - Scrum Master
- Pascal Mainini - Project Supervisor
- Nikita Aigner - Product Owner
Stakeholders:
- Berner Fachhochschule BFH, Architektur, Holz und Bau
- Hochschule für Agrar-, Forst- und Lebensmittelwissenschaften HAFL

The project is managed using the Scrum methodology. The project is divided into sprints, each sprint is around 2 weeks long. A fixed sprint lenght is not fisible because supervisor and stakeholder are not always available. The project is managed using the gitlab project management tool. Not all aspect of the Scrum methodology are used, because deemed unnecessary for such small project. Issue are categorized with a priority label. 
Scrum board consists of six columns:
- Product Backlog
- Sprint Backlog
- In Progress
- Waiting
- In Review
- Done
The idea is to create issues throught the project and put it in the product backlog. During the spring planing sessions some issues can be picked from the product backlog and assigned to the sprint. The issues are then moved to the sprint backlog. Before a task can be set as done, it has to be reviewed by another team member and the changes has to be merged into the main branch.   
### Scrum events
- Sprint Planning
- Weekly Scrum Meeting
- Sprint Review
- Sprint Retrospective

Sprint planing, review and retrospective are not done as separate meetings but are executed in a customized form. The following workflow will be used: At the end of each sprint short before the Sprint review with the Supervisor and Product Owner the team will do a short review so that everyone is informed of the progress of the team. The Progress made in the last spring is then shared with the Supervisor and Product Owner in a dedicated meeting. Here can both stakeholder give a feedback and the team can start discussing what has to be done in the next spring. In this meeting the date for the next Sprint review must be set. Afterwards the developer team can summarize the decision made and concretely plan the next sprint. Every week the dev team meetings to discuss the progress, probles encountered and design decisions.
### Git
Direct push into the main branch are forbidden. Exception can be made for minor modification to markdown files. The rest of the changes have to be made in a "issue-brnach" and after completation the branch can be merged into the main branch with a merge request. A new branch and a merge request for a specific issue can be created directly from the issues page in gitlab.

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
| Mittel    | Sensorknoten-Vorlagen sollen die einheitliche Erfassung von Sensorknoten gewährleisten und bieten die Möglichkeit Sensorknoten-spezifischen Konfiguration. |
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
| Mittel    | Relevante Projektdaten sollen in einem Linked Data Triple Store gespeichert werden. |
| Mittel    | Sensordaten sollen weiterhin zusätzlich in einer InfluxDB gespeichert werden. |
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

## Development
### Compiler Engine
The job of the compiler engine is to take the source code from a git repository, enrich the source code with additional informations gathered from the user and build the firmware. The firmware is then returned to the user in form of a binary. Additionally if requested by the user a compilation log and the enriched source code will also be provided by the compiler engine. The compiler engine is a dockerized standalone service that can be used through its REST api. The main puspose of this service is to compile arduino source code, but was designed to be able to compile source code with other toolchains as well. The idea is to dokcerize the toolchain needed to compile the source code. Then images for specific toolchains can be built and given over to the compiler engine. This way the compiler engine can be used to compile soource code for many differet projects, like for example, STM32, ESP32, Microchip, etc. Another key feature of this service is that that stores the built binaries for the user to request for them eliminating the need for webhooks or some other sort of asyncronous commuication. At the same time a garbage collector is implemented to delete old binaries that are too old.

<!-- #### Container Architecture
Docker in Docker vs multiple containers approach
- Docker in Docker: The compiler engine is running inside a docker container and the docker daemon is running inside this container. This approach is not recommended because of security reasons and the complexity of the setup.
- Multiple containers: The compiler engine is running inside a docker container and the docker daemon is running on the host machine. The docker socket is mounted into the compiler container. This approach is recommended because of the security and the simplicity of the setup. -->
#### Arduino toolchain image
The main focus of this service is to be able to compile arduino sketches (source code), for this purpose a specific toolchain is needed. An evaluation of the different methods to build arduino sketches into binary files was conducted. The following requirements were identified:
- **Headless**: The toolchain should be able to run without a GUI and be easyly automated
- **Docker** compatibility: The toolchain should be able to run inside a docker container
- **Libraries support**: The toolchain should be able to install libraries from the arduino library manager
- **Board support**: The toolchain should be able to compile for different boards
- **Open Source**: If possible the software used be open source and free to use

Several toolchains were considered for compiling Arduino sketches, evaluated based on the previously defined requirements.
### Arduino IDE  
**Pros**:  
- Official support  
- Compatible with all Arduino boards and libraries  
**Cons**:  
- GUI-based  
- Not suitable for automation or Docker environments [1]  

### PlatformIO  
**Pros**:  
- Powerful and cross-platform  
- Supports many boards and frameworks beyond Arduino  
**Cons**:  
- Primarily designed for interactive development  
- Complex setup  
- Limited headless and Docker support without workarounds [2]  

### Arduino CLI  
**Pros**:  
- Official headless toolchain  
- Designed for automation  
- Supports board and library management  
- Easy Docker integration [3]  
**Cons**:  
- Limited advanced build customization compared to PlatformIO  

### Makefile-based Toolchains (e.g., Arduino-Makefile)  
**Pros**:  
- Lightweight  
- Fully customizable  
- Docker-friendly [4]  
**Cons**:  
- Manual setup for boards and libraries  
- Lacks official support  
- Higher maintenance  

## References
[1] Arduino, “Arduino IDE,” [Online]. Available: https://www.arduino.cc/en/software  
[2] PlatformIO, “PlatformIO Documentation,” [Online]. Available: https://docs.platformio.org  
[3] Arduino, “Arduino CLI,” [Online]. Available: https://arduino.github.io/arduino-cli  
[4] Sudar, “Arduino Makefile,” [Online]. Available: https://github.com/sudar/Arduino-Makefile  

Arduino-cli was choosen because of its official support, easy docker integration and the support for board and library management. The limited support advanced features are not needed for the scope of this project. Once that the main toolchain was definted a research had to be made to look into the best way to dockerize the toolchain. After a brief search on docker hub and github several images for arduino-cli were found. Saddly non of them were akltively mantained. The best maintained project found by the research was the solarbotics/arduino-cli on dokcer hub that was not updated for more than 2 years. This was unaccettable and thus was decided to build a new image from scratch. This move also enabled the developers to ensure compability and control over the enviroment.

The main compiler container is based on the arduino-cli software and its used to comppile arduino sketches. This container/image should be interchangeable with other toolchain images. For this reason the docker command used to start the compilation should follow a specified structure so that those images can be interchanged and compiler engine itself will still works correctly.
### Docker Image
As base image **debian:stable-slim** was choosen because the developers have already experience with debian and the stable-slim tag offers a good compromise between size and stability. To install arduino-cli the official documentation was followed.[Docs](https://docs.arduino.cc/arduino-cli/installation/). The steps described in the official documentation made use of the linux utility *curl*. This utility is not available in the slim version of debian and thus instructions to install *curl* before installing arduino-cli had to be added to the Dockerfile.
After the installation the apt repositories and also curl were deleted to keep the size of the image to a minimum. Folders where while using the image volumes are mounted were created and the entrypoint was set to return the arduino-cli version. The entrypoint can be overwritten by the user to run the right arduino-cli command.
Lastly a minimal toolchain configuration was done. This was done after studying the COnfiguration keys described in the [official documentation](https://docs.arduino.cc/arduino-cli/configuration/). The exact configuration can be directly read from the Dockerfile.
At first the image was built locally and tested. After the tests were successful a gitlab ci/cd pipeline was created to use a gitlab runner to build the image and push it to the gitlab registry. The image is then pulled from the registry by the compiler engine service using a dedicated token. By doing so an up-to-date image is always available in the gilab registry of the project. The dokcer image can be used with the following command structure:
```bash
docker run --rm \
  -v <path_to_source_code>:/source \
  -v <path_to_output_folder>:/output \
  -v <path_to_logs>:/logs \
  -v <path_to_cache>:/cache \
  image:tag \
  compile_command
```
- source code folder: is the folder where the source code is located
- output folder: is the folder where the compiled binaries will be stored
- logs folder: is the folder where the logs of the compilation process are stored
- cache folder: is the folder where the cache of the toolchain is stored to allow faster repeated compilation
#### Docker Compile Command
A dockerized arduino-cli enviroment was succeffully built, but at the moment can only return the version of the arduino-cli programm. The next step is to build the docker command that will be used to compile the source code. Variables shpuld be used extensively to be able to integrate this command in the main service and compile all possible source code. Note that the syntax of this variable injection is python because the main service is written in python.
**Arduino cli commands needed to compile**:
```bash
mkdir -p /cache/boards /cache/arduino && \
arduino-cli core install $BOARD_CORE && \
arduino-cli lib install $LIBRARY_LIST && \
arduino-cli core update-index && \
arduino-cli compile \
  --fqbn $BOARD_CORE:$BOARD \
  --output-dir $OUTPUT_FOLDER \
  --log $LOG_FOLDER \
  --verbose \
  $SOURCE_FOLDER
```

The following variables are used:
- BOARD_CORE: The core of the board that the firmware is for (need to be installed beforehand). FOr example arduino:avr or esp32:esp32.
- LIBRARY_LIST: A list of libraries that are used in the source code and need to be installed beforehand.
- BOARD: The board that the firmware is for. For example uno or nodemcu.
- OUTPUT_FOLDER: The folder where the compiled binaries will be stored.
- LOG_FOLDER: The folder where the logs of the compilation process are stored.
- SOURCE_FOLDER: The folder where the source code is located.
The command above can be used to compile arduino source code manually but in a cli enviroment. The next step is to be able to use this command from within the main application.

# TODO
# custom images
# rest api
# Running the command inside the Docker container
container_output = client.containers.run(
            "registry.gitlab.ti.bfh.ch/internetofsoils/infrastructureforsensormanagment/arduino-compiler:latest",
            compile_command,
            volumes={
                "compiler-engine-source": {"bind": "/source", "mode": "rw"},
                "compiler-engine-output": {"bind": "/output", "mode": "rw"},
                "compiler-engine-logs": {"bind": "/logs", "mode": "rw"},
                "compiler-engine-cache": {"bind": "/root/.arduino15", "mode": "rw"}
            },
            remove=True,
            detach=False
        )
```

- logs folder: is the folder where the logs of the compilation process are stored, this logs can be returned in case of an error instead of the binaries

GitLab’s archive endpoint doesn’t necessarily validate the ref strictly. If you provide an invalid ref, GitLab will often default to the repository’s default branch when generating the archive. That’s why you still get back a ZIP file even if the ref you provided (e.g., maidgdgbensss) doesn’t exist.

---
# Evaluation

## Binäre Serialisierung
Statt ein eigenes Byte-array zu schreiben oder beispielsweise JSON anzuwenden, sollte ein binäres Serialisierungsformat verwendet werden.
Dies hat einige klare Vorteile:
- Effizienz, das Serialisieren und Deserialisieren von Daten ist deutlich schneller als z.B. bei JSON
- Entwicklungsgeschwindigkeit: Sobald das Schema definiert ist, kann Sourcecode für diverse Sprachen generiert werden, welche das lesen und schreiben der Daten handhabt.
- Strongly Typed: Bereits bei der Kompilierung können Fehler im Code erkannt werden, da Typen klar definiert sind.
- Schema: Das klar definierte Schema zeigt auf, welche Daten in welchem Format vorliegen. Die Schemas können mit definierten Mechanismen erweitert werden, sind also versionerbar.

### Protobufs
Der ältere Standard (ursprünglich aus den 2000er Jahren), set 2008 als Open-Source-Standard. Darum auch eine sehr breite Community und umfangreiche Tooling-Unterstützung. Etablierter Standard. Die Schema-Evoluation ist relativ einfach, Anpassungen am Datenformat können also leicht gemacht werden. Es wird immer die ganze Nachricht ausgelesen. Funktioniert am besten mit kleinen Datenmengen (wenig MBs). Es soll verglichen zu FlatBuffers deutlich benutzerfreundlicher sein (Einfache Installation des Compilers, Tutorials etc.). Es ist etwas langsamer als Flatbuffers.

### Nanopb
Ist eine sehr schmale, C-Implementation von Protobufs. Es ist optimiert für 32-bit embedded systeme mit sehr wenig resourcen (<1kB RAM). Es ist optimiert für wenig Speicherbedarf und Resourcenverbrauch. Die Schema-Definition von Protobufs kann direkt übernommen werden.

### FlatBuffers
Auch effizient bei grösseren Datenmengen. Die Nachrichten sind read-only, können nicht mehr geändert werden. Es kann bei Wunsch nur ein Teil des Datensets deserialisiert werden. Wird oft bei Mobile Gaming eingesetzt, wo performance sehr wichtig ist und begrenzte Resourcen zur Verfügung stehen. Für das Bauen eines Datenset wird mehr Code als im Vergleich zu Protobufs benötigt. Defintiv eine der besten Bibliotheken wenn der Fokus auf Effizienz liegt.

### Weitere Optionen
- Apache Avro: JSON-basiertes Schema. Zentraler Einsatz im Big Data Gebiet, bietet jedoch native Funktionalität für Datenversionierung. Nicht für IoT optimiert, kann zu grösserem Overhead führen und Integration auf ressourcenbeschränkte Umgebungen mühsam.
- MessagePack: Sehr einfaches Protokoll. Es basiert nicht auf einem externen Schema, was die Definition anhand von Datentypen erschweren würde. Sehr JSON-ähnlich, würde sich also in vielen Programmiersprachen integrieren lassen. Aufgrund des fehlenden Schemas wäre die Validierung und Versionierung der Daten schwierig, auch die Evoluation des Schemas wäre mühsam.

### Resultat
Es wird Protobufs (und Nanopb auf dem Board) eingesetzt. Der Standard wir gut unterstützt und die Code-Integration sollte einfach sein. Das Schema liegt in einem textuellen Format vor, welches einfach generiert werden kann. Es ist darauf ausgelegt mit wenig Overhead kleine Mengen an Daten zu übermitteln und der Einhaltung eines Schemas. Das ist genau unser Use-Case.


