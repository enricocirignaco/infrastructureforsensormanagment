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

## Development
### Compile Engine
The job of the compile engine is to take the source code from a git repository, enrich the source code with additional informations gathered from the user and build the firmware. The firmware is then returned to the user in form of a binary. Additionally if requested by the user a compilation log and the enriched source code will also be provided by the compiler engine. The compiler engine is a dockerized standalone service that can be used through its REST api. The main puspose of this service is to compile arduino source code, but was designed to be able to compile source code with other toolchains as well. The idea is to dokcerize the toolchain needed to compile the source code. Then images for specific toolchains can be built and given over to the compiler engine. This way the compiler engine can be used to compile soource code for many differet projects, like for example, STM32, ESP32, Microchip, etc. Another key feature of this service is that that stores the built binaries for the user to request for them eliminating the need for webhooks or some other sort of asyncronous commuication. At the same time a garbage collector is implemented to delete old binaries that are too old.

#### Service Architecture
The system is comprised of two always running dokcer containers and a third dokcer container responsible for the compilation. The main service is responsible for providing a REST API with which an user or an external service can communicate with the compile engine and for example start a new build job. The main service must also be able to download the source code from a gitlab repository given the repository link and a valid access token. Also the main serice must be able to enrich the source code via variables provided via the REST request. Finally the main service is responsible for starting the build process in a separate container. By default arduino code must be able to be compiled but there must also be the possibily to interchange the compiler image. The main service is also responsible for storing the compiled binaries and the logs of the compilation process. 
The second service is the Volume cleaner. This service service starts togehter with the main service and is responsible for deleting old generated and downloaded files. Finally the third container is the compiler toolchain itself. This container is started by the main service and is responsible for compiling the source code. The compiler container is started with a docker command that is provided by the main service. This way the main service can use different compiler images for different projects without having to be modified. 
![Service Architecture](./images/compile_engine_architecture.svg)
#### Arduino toolchain
The main focus of this service is to be able to compile arduino sketches (source code), for this purpose a specific toolchain is needed. An evaluation of the different methods to build arduino sketches into binary files was conducted. The following requirements were identified:
- **Headless**: The toolchain should be able to run without a GUI and be easyly automated
- **Docker** compatibility: The toolchain should be able to run inside a docker container
- **Libraries support**: The toolchain should be able to install libraries from the arduino library manager
- **Board support**: The toolchain should be able to compile for different boards
- **Open Source**: If possible the software used be open source and free to use

Several toolchains were considered for compiling Arduino sketches, evaluated based on the previously defined requirements.
##### Arduino IDE  
**Pros**:  
- Official support  
- Compatible with all Arduino boards and libraries  
**Cons**:  
- GUI-based  
- Not suitable for automation or Docker environments [1]  

##### PlatformIO  
**Pros**:  
- Powerful and cross-platform  
- Supports many boards and frameworks beyond Arduino  
**Cons**:  
- Primarily designed for interactive development  
- Complex setup  
- Limited headless and Docker support without workarounds [2]  

##### Arduino CLI  
**Pros**:  
- Official headless toolchain  
- Designed for automation  
- Supports board and library management  
- Easy Docker integration [3]  
**Cons**:  
- Limited advanced build customization compared to PlatformIO  

##### Makefile-based Toolchains (e.g., Arduino-Makefile)  
**Pros**:  
- Lightweight  
- Fully customizable  
- Docker-friendly [4]  
**Cons**:  
- Manual setup for boards and libraries  
- Lacks official support  
- Higher maintenance  

##### References
[1] Arduino, “Arduino IDE,” [Online]. Available: https://www.arduino.cc/en/software  
[2] PlatformIO, “PlatformIO Documentation,” [Online]. Available: https://docs.platformio.org  
[3] Arduino, “Arduino CLI,” [Online]. Available: https://arduino.github.io/arduino-cli  
[4] Sudar, “Arduino Makefile,” [Online]. Available: https://github.com/sudar/Arduino-Makefile  

Arduino-cli was choosen because of its official support, easy docker integration and the support for board and library management. The limited support advanced features are not needed for the scope of this project. Once that the main toolchain was definted a research had to be made to look into the best way to dockerize the toolchain. After a brief search on docker hub and github several images for arduino-cli were found. Saddly non of them were akltively mantained. The best maintained project found by the research was the solarbotics/arduino-cli on dokcer hub that was not updated for more than 2 years. This was unaccettable and thus was decided to build a new image from scratch. This move also enabled the developers to ensure compability and control over the enviroment.

The main compiler container is based on the arduino-cli software and its used to comppile arduino sketches. This container/image should be interchangeable with other toolchain images. For this reason the docker command used to start the compilation should follow a specified structure so that those images can be interchanged and compiler engine itself will still works correctly.
##### Docker Image
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
If a custom image for another toolchain has to be made it has to follow this command structure. This allow the main service to use different toolchains for different projects without having to to be modified.
##### Docker Compile Command
A dockerized arduino-cli enviroment was succeffully built, but at the moment can only return the version of the arduino-cli programm. The next step is to build the docker command that will be used to compile the source code. Variables should be used extensively to be able to integrate this command in the main service and compile all possible source code.
**Example command to compile arduino source code**:
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
#### Main Compiler Engine Service
After source code could successfully be built using the toolchain image made available in the gitlab registry of the project, a main service responsible for managing the compilation process was developed. The service consists of a docker container running two python script. One is used as garbage collector to delete old generated files and the other is the main service implementing a REST API that enable the user or another service to interface with the compiler engine service.
##### REST Frameworks Evaluation
To implement a simple REST service, several technologies were evaluated, focusing on performance, ease of use, community support, and Docker compatibility. While the programming language was not a strict requirement, the development team is comfortable with Python, Java, Rust, and JavaScript. The following frameworks were considered:

###### Express.js (JavaScript)  
**Pros**:
- Lightweight and minimalistic  
- Large ecosystem and community  
- Fast prototyping  
**Cons**:
- Lacks built-in type safety  
- Requires manual setup for validation and documentation [1]

###### Spring Boot (Java)  
**Pros**:
- Enterprise-grade features  
- Mature ecosystem and tooling  
- Built-in validation and dependency injection  
**Cons**:
- Heavy for simple services  
- Slower startup time [2]

###### Actix-Web (Rust)  
**Pros**:
- High performance and low memory usage  
- Strong type safety  
**Cons**:
- Steep learning curve  
- Smaller ecosystem  
- Tooling not as mature [3]

###### FastAPI (Python)  
**Pros**:
- Simple and clean syntax  
- Automatic OpenAPI documentation  
- Asynchronous by default  
- Strong typing with Pydantic  
- Fast development cycle  
**Cons**:
- Slightly slower than Actix or Spring in raw performance [4]

FastAPI was ultimately chosen due to its excellent balance of developer ergonomics, async support, built-in documentation, and suitability for quick iteration. It aligned well with the team's Python experience and the simplicity of the service.
###### References
[1] Express, “Express - Node.js web application framework,” [Online]. Available: https://expressjs.com  
[2] Spring, “Spring Boot,” [Online]. Available: https://spring.io/projects/spring-boot  
[3] Actix Project, “Actix Web,” [Online]. Available: https://actix.rs  
[4] FastAPI, “FastAPI - The modern Python web framework,” [Online]. Available: https://fastapi.tiangolo.com  

FastAPI is very straightforward to use, a simple dockerfile was written that used python:3.10-slim as a base image and then fast api dependencies were installed with pip and filally the main script was copied into the image. Note that is not advised to use the *latest* when choosing the base image because new versions can introduce braking changes to the system. Before an API specification could be written using the OpenAPI stadard, some experimenting had to be done to understand how the FastAPI framework works and how this could be integrated with the compiler toolchain.
##### DinD vs Docker Socket Binding
To enable the main Python script to spawn a Docker container for the compiler engine, two primary approaches were considered: Docker-in-Docker (DinD) and Docker socket binding. DinD runs a full Docker daemon inside a container, allowing full isolation and independence from the host’s Docker engine. However, it introduces significant complexity, requires privileged mode, and suffers from stability issues in production environments. In contrast, Docker socket binding mounts the host’s Docker socket (/var/run/docker.sock) into the container, allowing it to control the host Docker daemon directly. While this approach is simpler and more performant, it poses serious security risks: any process inside the container can fully control the host Docker engine, effectively granting root access to the host. Given these trade-offs, Docker socket binding was chosen for its simplicity and lower resource overhead, with the understanding that it must only be exposed to trusted code and isolated carefully from untrusted input. In a later phase of the project, a detailed risk assessment should be conducted to fully evaluate and mitigate the risk of infrastructure compromise. This security analysis is considered out of scope for the current implementation.
##### What is Docker Socket Binding?
Docker exposes its API via a Unix domain socket located at `/var/run/docker.sock`. By **binding** this socket (i.e., mounting it into a container or making it accessible to a local script), an application can communicate directly with the Docker daemon on the host.
This allows any client with access to the socket to perform operations such as:
- Running new containers  
- Stopping or removing containers  
- Building images  
- Accessing container logs  
This is the same interface used by the `docker` CLI and the official Docker SDKs.
Using the official Docker SDK for Python (docker-py), the script can create a new container on the host system as follows:
``` python
import docker

client = docker.from_env()
client.containers.run("alpine", ["echo", "hello world"])
```
###### Open API Specification
After the experimental phase was completed and a profe of concept was developed, the next step was to write the OpenAPI specification for the REST API. The OpenAPI specification is a standard for defining RESTful APIs, providing a machine-readable description of the API's endpoints, request/response formats, and authentication requirements. This specification can be used to generate documentation, client libraries, and server stubs automatically. The FastAPI framework natively supports OpenAPI, automatically generating code and documentation based on the specification. Great care was taken to ensure the specification was accurate and complete, as it would serve as the primary reference for the API's behavior and capabilities. Several iterations were needed in order to define a capable and user-friendly API that met the project's requirements. The following endpoints were defined in the OpenAPI specification:
- POST /build: initiate a standard build job
- POST /generic-build: initiate a custom build job
- GET /job/{job_id}/status: retrieve the status of a build job
- GET /job/{job_id}/artifacts: retrieve the artifacts of a build job
After the specification was written a FastAPI basic framework was generated from the specification. Of course the business logic and additional functions had to be written manually by the developers.
Pydantic played a key role in defining the request and response schemas used by the REST API. It is a data validation and parsing library that uses Python type hints to enforce strict structure and types for incoming and outgoing data. FastAPI integrates Pydantic natively, allowing developers to define models that serve as both documentation and validation logic. This significantly reduced the risk of inconsistent or ambiguous API behavior, as each endpoint's inputs and outputs were explicitly defined and validated at runtime. Additionally, Pydantic models are automatically included in the OpenAPI schema, ensuring that the documentation and actual implementation remain synchronized. This helped streamline the development process and allowed for faster iteration on the API design.
##### Source code download from Gitlab
The source code to compile should be automatically gathererd by the compile service from gitlab using the gitlab API. The main service can access the source code using an access token. The *archive* endpoint was used to return a zip file of only the specific folder in which the source code is located. This avoid cloning the whole repository with its history and reduce the time needed to download the source code. This endpoint of the gitlab api also supports specifying a specific version of the code by specifynig a *sha* value. The *sha* value can be a commit hash, a branch name or a tag name. GitLab’s archive endpoint doesn’t necessarily validate the sha strictly. If you provide an invalid sha, GitLab will often default to the repository’s default branch when generating the archive. This can lead to confusion and should be taken into account when using the compile service.
The main service use a group access token to access source code and the docker registry. This means that all repositories in the group can be accessed by the service and thus all project that have to be compile with the default compiler must be in the same group as this project: **InternetOfSoils**. To compile source code that is not part of this group the custom endpoint should be used. With this enpoint the access token can be specified along with the repository url.
##### Integration of additional metadata
A key requirement of the compiler engine is to enrich the source code with additional metadata before compilation. This metadata includes but should not be limited to TNN identification values and Firmware UUID. The idea is that body of compile endpoint has an optional *config* parameter. This is an array of key value pairs. The key is the name of the variable that has to be replaced in the source code and the value is the value of the variable. This way maximum flexibility is achieved if the more variables need to be set dynamically at compile time. The json body of the REST request is then parsed and a *config.h* file is generated. This file is then copied into the source code folder and its included in the main source file by  adding the line at the beginning of the file:
```c
#include "config.h"
```
This changes are not saved back into the repository but the source code with the changes can be downloaded using the right REST endpoint.
#### Volume cleaner service
The generated data should be provided for a give period by the Compiler Service. When this period has ellapsed it can't be garantied anymore by the service that the data is still available. For the purpose of deleting old generated data the volume cleaner service was developed. This is a simple python script running in a docker container that is started when the main service is started. This service run a check on all the following vomus once an hour: *output*, *logs* and *cache*. If the files in the volume are older than the specified time the files are deleted. A logfile is created in the logs volume to keep track of the deleted files and abviously it ignored by the cleaning service. The time after which the files are deleted and the check interval can be set with enviroment variables.
### Firmware Flashing
A strategy for flashing the compiled firmware on the hardware should be developed. The hardware used thougout the project is the CubeCell – AB01 Dev-Board (V2) based on the ASR6502 Chip made by the cinese company heltec.[9] The board can act as a LoRa Node and it is fully arduino compatible. The board comes with a bootloader preinstalled so that it can be programmed via USB/Serial interface just like an arduino board.
#### Requirements
- The compilation process should be as straightforward as possible because the user most likely has no technical experience.
- **If possible**:The firmware should be flashed on the hardware without the need of any additional software. (irectly over the browser).
- In case the adopted solution (via browser) requires internet connection, an alternative solution that works offline should be also provided.
#### Research
After reading the poorly documented documentation of the CubeCell board if was discovered that neigher the bootloader that works with the arduino enviroment nor the utility to flash the arduino code on the board are open source. Only their binaries are provided. This complicate the work of the developers a lot.
As described here [10] the Cubecell in question supports two different bootloaders, one of them is arduino compatible but as can be seen from the screenshoot on the same page this bootloader is closed source and it's not avalable to the public. Different issues on the matter were already started on github like this [11]. In this gitlab issue[12] someone is even accusing Heltec of misusing the GCC compiler that is under GPL license. So it's clear that this company is not interrested in open sourcing it's development tools and thus aworkaround should be found.
To better understand what exactly it's missing to be able to flash a firmware on the cubecell board the compilation and flashing process via the arduino IDE was closely investigated. Before any code can be compiled for this board the Hardware-specific files must be installed to the Arduino IDE using its board manager. The Board manange does nothing else than downloading the content of the following gitlab repository [13]. By getting a look at the get.py file in the tools folder the following line can be seen:
```python
tools_to_download = load_tools_list(current_dir + '/../package/package_CubeCell_index.template.json', identified_platform)
```
This hints that the links to the files to be downloaded are in the package_CubeCell_index.template.json file.
In this json file multiple url pointing to a download server hosted by heltec automation can be found. As for example:
```json
    "url": "https://resource.heltec.cn/download/ASR650x-Arduino-1.2.0-BoardManager.zip",
```
This file server reveal interesting findings over what's available for download for the users. Not only that by multiple PDFs are scattered all over the place with maybe usefull information.

As far as understood ( not official documentation was found) there are three propetary tools that are used by the arduino IDE to compile and flash the firmware on the board:
- **CubeCellelftool**: it's used to convert the hex file compiled by the gcc / arduino IDE to a 
- **CubeCellflash**: This tool is usedd to flash boards with a ASR650x series chip [14]
- **flash6601**: This tool is used to flash boards with a ASR6601 series chip [14]
Those tools are provided as binaries for linux and macos and as exe for windows but only for x86 CPU architecture. Additionally a arm binary compatible with raspberry Pi is provided for the CubeCellflash utility.
There is some sparse informations on how to use those tools in different forum posts like this[15] and this [16] but no official documentation was found. The exact usage can be reverse engineered by looking enabling verbose logging in the arduino IDE and trying to compile and flash a test firmware on the board.
<!-- write here your findings with arduino ide -->

Because of the closed source nature and the lack of ready to use tools it's unlikely that upload-via-browser functionality can be implemented. The only way to flash the firmware on the board is to use the provided binaries, either directly of via arduino toolchain.

Another interesting software is the arduino create agent (also named arduino cloud agent). This is an utility that needs to be locally installed on the host machine that can communicate with the arduino cloud (browser based arduino IDE) and practically giving the possibility to program and debug arduino boards via browser[17]. It's unclear if this software can be used to flash the firmware on the Heltec boards. 
If the arduino create agent can be used for our project, it would simply and speed up the development process. Otherwise a custom solution with a similar approach as the arduino create agent has to be developed.

The idea would be to create an application that exposes a rest api that can be used by the webapplication to send the binary and integrates the propetary flashing tools of heltec to be able to flash the binary on the board. The application should be packaged in a single executable for easy installation.



#### References
[9]  https://heltec.org/project/htcc-ab01-v2/
[10] https://docs.heltec.org/en/node/asr650x/htcc_am01/programming_cubecell.html
[11] https://github.com/HelTecAutomation/CubeCell-Arduino/issues/80
[12] https://github.com/HelTecAutomation/CubeCell-Arduino/issues/281
[13] https://github.com/HelTecAutomation/CubeCell-Arduino/tree/master
[14] http://community.heltec.cn/t/cubecell-download-tool-for-raspberry-pi/2522/12
[15] http://community.heltec.cn/t/cubecellflash-tool/1953/3
[16] http://community.heltec.cn/t/cubecell-firmware-upload/1063
[17] https://docs.arduino.cc/arduino-cloud/hardware/cloud-agent/

https://github.com/arduino/arduino-create-agent
https://github.com/HelTecAutomation/CubeCell-Arduino
https://github.com/kaelhem/avrbro
https://resource.heltec.cn/download/
https://github.com/arduino/arduino-create-agent/issues/150
### Frontend webserver and reverse proxy
It's generally a good idea to separate the frontentend webserver handling the delivery of static content (html, css, JS) and the backend webserver, handling the REST API. This common practice helps scalability, security, and maintainability of the application. Thus is was decided to separate this two components. This chapter will explain how the frontend webserver work. Common static webservers are nginx, caddy and apache. Nginx and Caddy can also be used as Reverse Proxy so instead of having two different servers, one serving static content and on front handling reverse proxy, both functionalities can be handled by the same server. This is a good solution for small projects where the overhead of having two different servers is not justified. Caddy is a very good canditate because it also offers tls encryption out of the box and is very easy to configure, also the developers already had some experience deploying caddy.
After the caddy service was added to the compose file, the caddyfile was created. The caddyfile is the configuration file for caddy and it defines how the server should behave. The caddyfile is very easy to read and understand. For testing purposes an index.html file was created and served by caddy. Afterward the reverse proxy rules could be added. This rules just describe which subdomain or path should be routed to which service. Additionally tls with self signed certificates was enabled. The CA had to be self signed because we don't own a public domain. For development purposes some aliases were created so that the services are also available via vpn at a readable hostname.
#### Frontend Framework
It was clear from the beginning that a frontend framework should be used for the development of the web application. Modern frameworks are:
- React: 
    - upsides: popular, large community, many libraries and tools available, good documentation
    - downsides: large bundle size, complex state management, steep learning curve
- Vue: 
    - upsides: easy to learn, good documentation, small bundle size, good performance
    - downsides: smaller community than React, less libraries and tools available
- Angular:
    - upsides: large community, good documentation, many libraries and tools available, good performance
    - downsides: large bundle size, complex state management, steep learning curve

The team was already leaning toward Vue but the fact than one team member cover Vue in the "Javascript Frameworks" class made the decision easier. Vue can be developed an deployed using the **NPM** utility. A new application can be easly created with this command:``npm create vue@latest``. As for the development enviroment it was choosen to take advantage of the *devcontainer* feature of VSCode. This  ensure a consistent and reproducible development environment. A Dev Container is a Docker-based workspace that includes all the necessary tools, runtimes, and configurations required to build and run the application. The configuration is defined in .devcontainer/ folder, where the devcontainer.json specifies the image, extensions, and workspace setup. When opened in a compatible editor like Visual Studio Code, the project automatically runs inside the container, allowing development to happen in a clean and isolated environment. This approach reduces system dependency issues and makes onboarding new developers easier, as no manual setup is required beyond Docker and VS Code. Additionally multiple configuration files can be added for developing different parts of the project. For example a devcontainer.json for the frontend and one for the backend. This way the developers can choose which part of the project they want to work on and the IDE will automatically set up the right environment. This development enviroment also allow for hot reloading of the code. This means that when the code is changed, the changes are automatically reflected in the browser without the need to refresh the page. This is a very useful feature for development and speeds up the development process a lot.
#### Deployment
The application can be built with the following command: `npm run build`. This will create a new folder called *dist* in the root of the project. This folder contains all the files needed to run the application. The location where the project is exported can be manually set in the vite.config.js file like that:
```javascript
  build: {
    outDir: '../www',
  },
```
For deployment a 2 stages Dockefile was written that in the first stage gets the source code and build it using the node image. The second stage build the final image based on the caddy image. The dist folder generated in the previous stage together with the Caddyfile are copied into the image.
The compose file will automatically build the image and start the container. In a second phase the image will be automatically built using a gitlab ci/cd pipeline. 
## Info vue
- main.js: is only for adding plugins
- App.vue: is the main component of the application. can be used for addding global parts of the application like nav bar, header or footer. Routerview should be present (this is then replaced with the content of different components by the router).
router/index.js: is the file where the routes are defined. The routes are then used by the router to display the right component.
- views are special type of components that rappresets a whole page. views can be constructed using multiple components. views are loaded by the router and are displayed in the routerview.










# Evaluation

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