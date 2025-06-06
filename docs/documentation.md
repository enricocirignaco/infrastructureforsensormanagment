# Abstract 

# Introduction --> Linus
## Context & Background --> Linus
Such a typical IoT system consists of several core components that together enable the continuous collection, transmission, and utilization of data from distributed edge devices. At its foundation lies the ability to gather time-based data remotely. Sensor nodes are deployed in environments where manual data collection would be impractical or inefficient, and they measure physical phenomena such as temperature or humidity at regular intervals. The gathered data is transmitted via wireless technologies like WiFi, LoRaWAN, or cellular networks, each with different trade-offs regarding range, energy usage, and bandwidth. Once received by a central system, the data is stored—often in time-series databases—for later analysis, visualization, or integration into other systems.




## Goal of the Project --> Linus
The goal of this thesis is to design and implement a generic infrastructure that streamlines the processes involved in managing distributed sensor nodes. While the system is initially developed in the context of academic environmental monitoring projects, its intended scope is much broader. The underlying concepts and components are designed to be flexible and reusable across a wide range of applications that rely on sensor-based data collection, regardless of domain or deployment scale. In particular, the previously discussed issues such as fragmented metadata, manual provisioning steps, and the lack of a defined data format are targeted with concrete technical solutions.

To ensure accessibility and usability, the developed infrastructure is intended to be operated through a web-based user interface. This interface follows established usability principles and aims to make the various workflows intuitive, reducing the technical overhead for researchers and project stakeholders. By providing an integrated and user-friendly platform, the project seeks to simplify day-to-day operations while increasing the reliability and scalability of sensor deployments.

A central aspect of the planned infrastructure is the structured management of metadata related to sensor deployments, including all entities and relationships required to describe such systems comprehensively. 
*Projects* serve as top-level containers that group deployments with shared context, enabling the management of multiple independent setups across different locations, time frames, or application domains. Each *sensor node* should be associated with a set of attributes, including hardware type, firmware version, deployment location, and optional metadata such as documentation links. To improve efficiency and consistency, reusable *templates* should support the creation of similar sensor nodes across different projects.

Once a sensor node is defined within the system, it should be automatically provisioned on The Things Network (TTN), which serves as the communication backend for LoRaWAN-based data transmission. During this process, essential credentials such as *DevEUI* or *AppKey* should be generated and stored securely within the system. The goal is to eliminate the need for manual registration steps in the TTN console, reducing the likelihood of errors and ensuring that each node can be uniquely and reliably identified once deployed.

Based on the metadata and provisioning information stored in the system, a tailored firmware should be compiled for each sensor node. The appropriate source code is retrieved from a central GitLab repository, where different firmware variants are maintained. Node-specific configuration values, such as communication keys or feature flags, are injected during the build process using templating techniques. The result of this process should include a ready-to-flash binary file, with compilation logs and generated source code optionally provided for debugging and development purposes. Automating this step helps ensure consistency across firmware builds and minimizes manual intervention during node setup.

Once the firmware has been compiled, it should be transferred onto the physical sensor hardware. This flashing process should be as automated as possible. If supported by the connected hardware and system environment, the flashing could ideally be initiated directly through the developed web application. In cases where full automation is not feasible, a command-line script should be provided as an alternative to manually performing the process in a development environment. The goal is to eliminate the need for tools such as the Arduino IDE and to streamline the setup of new sensor nodes across different platforms.

After deployment, each sensor node should begin transmitting time-series data to the system using LoRaWAN. Since the data format may vary across projects or depending on the number and type of measured values, the system should include a centralized parsing mechanism that interprets incoming payloads and transforms them into a standardized internal structure. Parsed data should then be stored in an InfluxDB instance, which is a time-series database well suited for handling high-frequency data streams and is already used in existing research projects. It provides powerful tools for querying, filtering, and visualizing time-series data, making it a practical choice for both development and monitoring purposes.

In addition, all parsed data points should also be persisted in a triplestore, which serves as the primary data storage within the system. These data are represented as Linked Data using the RDF model, and where possible, suitable schemas and ontologies should be applied to support semantic structure and interoperability. This semantic store enables flexible linking of data and metadata, and ensures long-term extensibility across different parts of the project. This dual-storage approach allows both technical users and non-technical stakeholders to access and interpret the data in ways that suit their respective needs.

## Value Proposition for Stakeholder --> Linus

# State of Research
This chapter provides an overview of research carried out and available technologies relevant to the project. The focus lies on niche or emerging tools and methods that appeared promising but required feasibility evaluation before adoption. Most of the research was conducted during the conceptual phase, where assessing the practicality and integration potential of such technologies was critical for planning and system design.
## Retrospect Project2 --> Linus
## Programming and Toolchain Analysis for CubeCell
A key requirement of the project was the reuse of existing hardware from previous initiatives. Specifically, the board selected was the Heltec HTCC-AB01, which integrates the ASR6501 chip. The board comes preloaded with an Arduino-compatible bootloader that allows firmware flashing via the Arduino IDE. However, another important requirement was to enable future programming of the board without relying on the Arduino IDE. This made it necessary to find a method for flashing compiled binaries to the board via USB using the original bootloader. As a result, research was conducted into the Heltec CubeCell board, its bootloader behavior, and its available toolchain options.

As described in the official documentation[20], the CubeCell board supports two different bootloaders, one of which is Arduino-compatible. However, as visible in the screenshots provided on the same page, this bootloader is closed-source and not publicly available. Several related issues have already been opened on GitHub, such as [21], where users express concerns about the lack of transparency. In another thread [22], a user even accuses Heltec of violating the GPL license by misusing the GCC compiler. These concerns indicate that Heltec is not interested in open-sourcing its development tools, making it necessary to find a workaround.

To better understand the programming process, the behavior of the Arduino IDE must first be analyzed. Before any code can be compiled for the CubeCell board, the hardware-specific configuration must be installed via the Arduino Board Manager. This manager downloads configuration files from the Heltec GitHub repository [23]. In particular, the get.py script in the tools folder contains the following line:
```python
tools_to_download = load_tools_list(current_dir + '/../package/package_CubeCell_index.template.json', identified_platform)
```
This suggests that the actual download URLs are listed in the package_CubeCell_index.template.json file. Indeed, the json file contains multiple links pointing to Heltec’s download server, such as:
```json
    "url": "https://resource.heltec.cn/download/ASR650x-Arduino-1.2.0-BoardManager.zip",
```
Browsing this file server reveals not only the expected binaries, but also scattered PDF documents, some of which may contain useful technical information.

As far as could be determined—since no official documentation was found—the Arduino IDE relies on three proprietary tools for compiling and flashing firmware onto the board:
- **CubeCellElfTool**: Likely used to convert the compiled hex file into an intermediate format.
- **CubeCellFlash**: Used to flash boards with ASR650x-series chips [24].
- **flash6601**: Used to flash boards with ASR6601-series chips [24].

These tools are provided as binaries for Windows (EXE), macOS, and Linux—but only for x86 CPU architectures. One notable exception is a Raspberry Pi-compatible ARM binary available for the CubeCellFlash tool.
Some fragmented usage instructions can be found in forum posts such as [25] and [26], but no comprehensive official documentation is currently available.

To confirm that the proprietary utilities mentioned earlier are indeed used by the Arduino IDE for compiling and flashing the firmware—and to better understand their function—a test was conducted using the IDE’s verbose logging mode.
![arduino ideverbose settings](./images/arduino_verbose_settings.png)
A firmware upload was performed with verbose output enabled. The following snippet was extracted from the build log, immediately after the compiled binaries were generated. The output has been trimmed to highlight only the relevant portions of the flashing process:
```
/Users/macbook/Library/Arduino15/packages/CubeCell/tools/CubeCellelftool/0.0.1/CubeCellelftool /Users/macbook/Library/Arduino15/packages/CubeCell/tools/gcc-arm-none-eabi/8-2019-q3/bin/arm-none-eabi-objcopy /Users/macbook/Library/Caches/arduino/sketches/C0F716AC671CF6A6916D9A86A1AFEBF5/sketch_jun6a.ino.elf /Users/macbook/Library/Caches/arduino/sketches/C0F716AC671CF6A6916D9A86A1AFEBF5/sketch_jun6a.ino.hex /Users/macbook/Library/Caches/arduino/sketches/C0F716AC671CF6A6916D9A86A1AFEBF5/CubeCell_Board_REGION_AS923_AS1_RGB_1.cyacd
/Users/macbook/Library/Arduino15/packages/CubeCell/tools/gcc-arm-none-eabi/8-2019-q3/bin/arm-none-eabi-size -A /Users/macbook/Library/Caches/arduino/sketches/C0F716AC671CF6A6916D9A86A1AFEBF5/sketch_jun6a.ino.elf
Sketch uses 23380 bytes (17%) of program storage space. Maximum is 131072 bytes.
"/Users/macbook/Library/Arduino15/packages/CubeCell/tools/CubeCellflash/0.0.1/CubeCellflash" -serial "/dev/cu.usbserial-0001" "/Users/macbook/Library/Caches/arduino/sketches/C0F716AC671CF6A6916D9A86A1AFEBF5/CubeCell_Board_REGION_AS923_AS1_RGB_1.cyacd"
Initialising bootloader.
Silicon ID 0x256a11b5, revision 0.
Verifying rows.
Array 0: first row 34, last row 511.
Starting upload.
Uploading  ( 10 / 100 )
Uploading  ( 20 / 100 )
Uploading  ( 30 / 100 )
Uploading  ( 40 / 100 )
Uploading  ( 50 / 100 )
Uploading  ( 60 / 100 )
Uploading  ( 70 / 100 )
Uploading  ( 80 / 100 )
Uploading  ( 90 / 100 )
Uploading  ( 100 / 100 )
Checksum verifies OK.
Rebooting.
Total upload time 3.07s
```
A more detailed analysis of the build logs revealed that a utility called **CubeCellElfTool** is used to merge the ELF and HEX files into a .cyacd file. Its usage appears to follow the syntax:
```bash
CubeCellelftool <path_to_objcopy> <path_to_elf_file> <path_to_hex_file> <output_cyacd_file>
```
The objcopy utility, part of the GCC toolchain, converts the ELF file into a HEX file, which is then combined with additional metadata into the .cyacd format. Further research indicated that .cyacd stands for Cypress Application Code, a firmware update format originally developed by Cypress (now part of Infineon) for their PSoC (Programmable System-on-Chip) devices. It includes both application code and metadata required by the bootloader for programming flash memory [32]. This suggests that the Heltec CubeCell board might rely on a variant of a Cypress bootloader.

In the second part of the logs, the CubeCellFlash utility was identified as the tool responsible for flashing the generated .cyacd file to the board. Its usage follows the pattern:
```bash
CubeCellflash -serial <serial_port> <path_to_cyacd_file>
```

These findings confirm that CubeCellFlash is the primary flashing utility used in the Arduino toolchain and reveal its exact usage syntax.

With these insights, the team was faced with three options:
	•	Investigate the bootloader further to determine if it conforms to Cypress standards and whether third-party tools could be used for flashing.
	•	Reverse engineer the CubeCell utilities to understand their internal workings and re-implement them as open-source tools.
	•	Use the provided proprietary binaries and integrate them into a custom flashing solution.

The first option was discarded due to the time required for in-depth bootloader analysis. The second option was also initially rejected, but later reconsidered after an accidental misuse of the **CubeCellelftool** triggered a Python traceback, suggesting that the CubeCell utilities are likely packaged Python scripts. A partial decompilation confirmed this, and some source code was recovered. However, fully reverse engineering and integrating the tools into the project was deemed too time-consuming and ultimately abandoned.

The third option was selected as the most practical and time-efficient solution. Despite the drawback of relying on closed-source binaries, raising concerns about transparency and security, it enabled the team to proceed without blocking other parts of the project.


## Heltec
### Webserial ESP32-S3
Although this is the task with a lower priority, it was decided to research the feasibility of this solution first because this will have a great impact on to what extens the specific solution for the heltec will be delevoped and refined.
#### Research - Browser Serial APIs
A brief research was conducted to find out if the webserial thecnology is the only and best candidate for this task. While Web Serial (supported only in Chromium-based browsers like Chrome, Edge, and Brave) is currently the most practical way to flash ESP32 devices directly via the browser [28], there are a few alternative Web APIs worth noting. WebUSB allows direct USB access but requires custom USB descriptors and is only available in Chromium-based browsers — not Firefox or Safari [29]. WebHID, designed for HID-class devices, is unsuitable for flashing and also lacks cross-browser support [20]. WebBluetooth is supported in Firefox and Chromium but does not support full firmware flashing due to BLE’s limited data rates and payload sizes [21]. Thus, for full browser-based flashing without extra software, Web Serial remains the most viable option, albeit limited to Chromium environments. Cross-browser support is currently not achievable due to the lack of Web Serial and WebUSB support in Firefox and Safari.
#### Research - ESP32 compatible Webserial libraries
After a thorough research several javascrip tools for browser-baser flasing of esp32 devices were found. These tools leverage the [Web Serial API][28], allowing direct communication with ESP32 boards through a USB connection and without requiring any locally installed software.

##### Adafruit WebSerial ESPTool
Adafruit_WebSerial_ESPTool is a polished, browser-based firmware flasher developed by Adafruit. It provides a complete graphical interface that supports multiple ESP32 variants, with convenient features such as automatic chip detection and baud rate configuration. This project is actively maintained and designed for users who prefer an out-of-the-box solution without needing to write custom code. However, because it wraps around an existing library, it is less suitable if you require a deeply customized flashing UI for integration into a larger application.

##### esptool.js (from tiware)
esptool.js was one of the first projects to bring ESP32 flashing to the web by porting functionality from the Python-based esptool. Its main advantage lies in its minimal design, which makes it easy to embed into simple web applications. However, the project has not seen updates in over four years, and it lacks support for more recent ESP32 variants such as the ESP32-S3. In addition, documentation is sparse, and integration into modern toolchains may be cumbersome. Given the lack of maintenance, it is not recommended for new projects.

##### esptool-js (Espressif)
The official esptool-js project from Espressif is actively maintained and well documented. It brings most of the functionality of the widely used esptool.py to the browser and is designed specifically for modern Web Serial integration. Unlike older projects, this version keeps pace with new chip variants and is the basis for tools like ESP Web Tools. It offers lower-level control over the flashing process and is intended for developers who want to integrate ESP32 flashing directly into their custom interfaces. While it does not include a graphical interface, it is a solid foundation for building one.

The candidate that best fits the requirements of this project is the official esptool-js from Espressif. It is actively maintained, well documented, and designed for modern Web Serial integration.


## Linked Data --> Linus
## Protobuf --> Linus

# Methods
This chapter describes the methods used to organize and execute the project, including the project methodology, team structure, and chosen technologies. Since the project was carried out in a team of two, a structured approach was essential to avoid blocking progress due to interdependencies. Given the broad scope and limited timeframe, the project followed an iterative, practice-oriented methodology to maximize productivity. This approach allowed for continuous refinements based on supervisor feedback and evolving technical requirements.
## Team Organisation
The project was carried out by a two-person team, which required proactive planning and a clear division of tasks to avoid mutual blocking. The nature of the project allowed for largely independent work streams, which were divided into two main domains: (1) data acquisition and management, and (2) device provisioning, flashing, and monitoring. Additionally, the development of the web application was split between frontend and backend responsibilities, with each team member focusing on one of the two.

After a joint planning and conceptualization phase, where the system architecture and project requirements were defined, each team member assumed roles aligned with their strengths and interests. Tasks were managed using Git branches, with each feature developed independently and later merged into the main branch upon completion. This workflow enabled parallel progress without conflicts.

To maintain alignment, the team held regular internal meetings to discuss progress and synchronize development. A recurring practice called the “marriage” ensured that frontend and backend components were periodically integrated and tested together. Approximately every two weeks, the team also met with the project supervisor and stakeholder to demonstrate the current state of the system and gather feedback. Before these sessions, the latest features were merged, tested, and deployed to the server to provide a working prototype for review. This iterative process supported rapid, incremental improvements.

## Project Management Methodology
Given the complexity and time limitations of the project, a structured yet adaptable project management approach was required. The team followed an iterative, practice-oriented methodology inspired by agile principles, with particular reference to SCRUM [2]. While SCRUM provided a useful framework for organizing work and integrating feedback, it was adapted to fit the context of a small, part-time team.

The project was planned using a combination of milestones and sprints. During the initial conceptual phase, the team gathered and defined the system requirements. Based on those requirements, the team outlined rough milestones representing major project components and their estimated durations. These high-level goals helped assess the feasibility of planned features within the available timeframe. Although flexible, they provided structure and helped maintain overall direction throughout the project.

For short-term planning, the team relied on two-week sprints. At the start of each sprint, the team met to define and assign tasks based on priorities, individual strengths, and workload. A shared Kanban board was used to track progress. New issues, whether created by team members or suggested by stakeholders, were added to the backlog and reviewed during sprint planning. Tasks were labeled and updated throughout the sprint to reflect their current status. This lightweight adaptation of SCRUM enabled steady progress while maintaining flexibility.
![screenshot of kanban board](./images/kanban_board.png)

A review strategy was also established to ensure that all code changes were peer-reviewed before being merged into the main branch. This practice improved code quality, facilitated knowledge sharing, and helped both team members stay familiar with all parts of the system. Once a developer completed a task, a merge request was created. The merge request could only be merged after review and approval by the other team member. This enforced a clear quality standard and maintained shared ownership of the codebase.

In addition to tracking technical progress, the team implemented simple but effective controlling measures to ensure the project was properly documented. Meeting protocols were maintained to record key decisions and discussions. A shared work journal was used to log who worked on what, when, and how—providing transparency, traceability, and a basis for workload reflection. Both the protocols and the journal can be found in the appendix of this document.

### Milestones

| Milestone                                 | Duration         | Key Objectives                                                                 |
|-------------------------------------------|------------------|--------------------------------------------------------------------------------|
| Concept Phase                          | 3 weeks          | - Propose solution ideas  <br> - Detailed system diagram  <br> - PoC of key technologies  <br> - Data model diagram |
| Infrastructure Setup & Proof of Concept                   | 3 weeks          | - Set up development and production environment  <br> - Live data flow from sensor nodes to triplestore via Flatbuffers  <br> - PoC Compile and flash firmware via browser |
| Webapp Frontend & Backend                     | 4 weeks          | - User authentication  <br> - Frontend UI for data entry and visualization  <br> - Backend as middleware between services  <br> - Implement REST interface |
| End-to-End Testing                     | 2 weeks          | - Integrate all system components and services  <br> - Deployment of the v1 system  <br> - Stakeholder testing |
| Feedback Integration & Optional Features | 2 weeks        | - Adjust or implement components based on feedback  <br> - Technical wrap-up |
| Project Finalization                      | 2 weeks          | - Finalize documentation  <br> - Poster, project book entry, presentation, and video |

## Modern Application Methods
The project followed modern application development principles, drawing inspiration from the Twelve-Factor App methodology [3]. The goal was to build a modular, portable, and maintainable system that could easily be extended or adapted by future organizations. These principles ensured a clean separation of concerns, environment-agnostic deployment, and a consistent developer experience across all components. The following sections describe the key practices adopted during implementation.
### Version Control with Git
The codebase was managed using Git, with a single project repository hosted on BFH’s GitLab instance. This enabled effective version control, collaborative development, and reduced the risk of code loss. Each feature was developed in a dedicated branch and merged into the main branch only after review and approval by the other team member.

Not only the source code, but also all project-related documents—such as documentation, diagrams, and presentation materials—were versioned in the same repository. Non-code files were allowed to be pushed directly to the main branch.

Git tags were used to mark key integration points in the project timeline, especially when the system was successfully deployed to the production server. This tagging allowed for easy rollback if needed. A three-part versioning scheme was adopted:
- The first number indicated major versions (e.g., 0.x.x during development, incremented to 1.0.0 for the first alpha release),
- The second number for minor releases (typically used for new deployments to production), and
- The third number for bugfixes and small patches.

These tags also served as triggers for the CI pipeline, which is discussed in detail in the section [Multistaged GitHub CI Pipeline](#multistaged-github-ci-pipeline).
### Containerized Microservice Architecture
The system was built using a microservice architecture, where each service is dedicated to a specific responsibility within the overall system. This approach promotes modularity, simplifies maintenance, and enables independent development, testing, and deployment of individual components.

Each microservice includes its own configuration and dependencies, allowing it to run in isolation. Services expose RESTful interfaces for communication, making them easy to integrate or replace without affecting the rest of the system. A reverse proxy handles internal routing and load balancing, enabling flexibility in scaling and deployment.

From the start, each service was developed and deployed as a Docker container. Containerization ensures strong isolation between services and simplifies dependency management. It also guarantees consistency across development and production environments by replicating the same runtime conditions. More details about the deployment setup are provided in the [Deployment & Integration](#deployment--integration) section.

Descriptions of the individual services can be found in the [System Architecture](#system-architecture) section.
### Multistaged GitHub CI Pipeline
A clear separation between the build and run stages is a key principle of modern application architecture [3]. In this project, each service was packaged as a custom Docker image. The build stage was fully automated using a GitHub CI pipeline, while the run stage consisted of deploying these images as containers on the production server.

The pipeline is triggered by the creation of a new Git tag. Once triggered, parallel jobs build the Docker images for each service. The resulting images are tagged according to the Git version and pushed to a private container registry hosted on BFH’s GitLab. From there, the server can securely pull and run the containers.

This approach ensures reproducible, versioned deployments and centralized control over image distribution. Using a private registry improves reliability and avoids dependency on public registries. Versioning with Git tags also allows for easy rollbacks in case of errors or regressions.

Because the build stage does not run on the deployment environment, it avoids spreading the full Git repository across multiple systems, reducing the risk of accidental source code leakage. Although this is not critical for this project, since the codebase is not proprietary, it reflects good practice. It’s worth noting, however, that this protection does not apply to services written in interpreted languages, where source code remains accessible within the container.
## Technology Stack
This section provides an overview of the technologies and tools used in the project, along with the reasoning behind their selection. Choices were guided by factors such as developer familiarity, compatibility, community support, and alignment with the project’s goals and constraints.
### MQTT Broker
The team selected Eclipse Mosquitto as the MQTT broker. It is lightweight, widely used in IoT systems, and offers excellent community support. Its reliability and ease of integration made it a good choice. Additionally, the team had prior training with Mosquitto through the IoT specialization course.
### Reverse Proxy
Although several reverse proxy solutions were briefly considered (e.g., NGINX, Traefik), the team opted for Caddy, as the project only required a small number of simple reverse proxy rules. Caddy offers automatic HTTPS, a user-friendly configuration syntax, and minimal maintenance overhead, features that aligned well with the project’s goals and time constraints.
### Time-Series Database
The use of InfluxDB as the time-series database was a requirement defined by the stakeholder from the outset. InfluxDB was already familiar to the stakeholder and provided a good fit for the type and volume of time-series data collected by the system.
### RDF Triplestore
For persistent storage and querying of RDF data, the team evaluated multiple triplestore options and ultimately selected Apache Jena Fuseki. Fuseki is open-source, lightweight, and easy to set up—either as a standalone Docker container or integrated into Java applications via Maven. Compared to alternatives such as Blazegraph, which is no longer actively maintained, or GraphDB Free, which imposes limitations in its free version, Fuseki provided a more reliable and unrestricted solution. Commercial tools like Stardog or Amazon Neptune were also considered but were outside the scope of the project in terms of scale and cost. Fuseki had already been used successfully in a previous project, where it proved effective and simple to work with. The only notable limitation is the lack of built-in role-based access control for managing users and permissions [12].
### SPARQL Query Editor
To enable users to interact with the triplestore, a graphical SPARQL query editor was also required. The team evaluated several tools and selected YASGUI, a widely used and actively maintained editor. YASGUI offers helpful features such as syntax highlighting, validation, and autocompletion [11]. One of its most valuable capabilities is its plugin architecture, which allows for custom extensions—for example, rendering query results directly on a map—making it ideal for enhancing user experience in this project.

### REST Framework
To implement REST services, several frameworks were evaluated with a focus on performance, ease of development, Docker compatibility, and ecosystem maturity. While the programming language was not fixed, the team had experience with Python, Java, Rust, and JavaScript. The following options were considered:
| Framework         | Language    | Pros                                                                                   | Cons                                                                                      |
|------------------|-------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Express.js        | JavaScript  | - Lightweight and minimalistic  <br> - Large ecosystem and community  <br> - Fast prototyping | - No built-in type safety  <br> - Requires manual setup for validation and documentation [4] |
| Spring Boot       | Java        | - Enterprise-ready features  <br> - Mature ecosystem and tooling  <br> - Integrated validation and DI | - Heavy for small services  <br> - Slower startup time [5] |
| Actix-Web         | Rust        | - High performance and low memory usage  <br> - Strong type safety                      | - Steep learning curve  <br> - Smaller ecosystem  <br> - Less mature tooling [6]          |
| FastAPI           | Python      | - Clean syntax and fast development cycle  <br> - Built-in OpenAPI documentation  <br> - Asynchronous support  <br> - Strong typing with Pydantic | - Slightly lower raw performance compared to Actix or Spring [7] |

FastAPI was ultimately chosen for its balance between developer ergonomics and powerful features. Its automatic documentation generation, async support, and strong typing accelerated development and testing. It also aligned well with the team’s prior experience in Python and the need for quick iteration. All REST-based services in the project, such as the backend of the web application, were implemented using FastAPI and deployed in Docker containers.
### Frontend Framework
Given the requirements for an interactive and maintainable web interface, the use of a modern frontend framework was considered essential. The team evaluated several established frameworks, each with its own strengths and trade-offs:

The team ultimately selected Vue, as it offered the best balance between simplicity and capability for the project’s needs. Additionally, one team member was concurrently taking a university course on JavaScript frameworks, which included Vue, providing valuable hands-on experience during development.

| Framework | Pros                                                                                   | Cons                                                                                   |
|-----------|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| React     | - Very popular  <br> - Large community  <br> - Rich ecosystem of libraries and tools  <br> - Strong documentation | - Large bundle size  <br> - Complex state management  <br> - Steep learning curve [8]  |
| Vue       | - Easy to learn  <br> - Excellent documentation  <br> - Small bundle size  <br> - Good performance               | - Smaller community compared to React  <br> - Fewer third-party libraries [9]          |
| Angular   | - Large community  <br> - Strong tooling  <br> - Robust performance  <br> - Built-in features                    | - Heavy bundle size  <br> - Steep learning curve  <br> - Complex state handling [10]    |

The team ultimately selected Vue, as it offered the best balance between simplicity and capability for the project’s needs. Additionally, one team member was concurrently taking a university course on JavaScript frameworks, which included Vue, providing valuable hands-on experience during development.

An overview of all key technologies used can be found in the system architecture diagram in the [System Architecture](#system-architecture) section. The following sections provide more details on the individual components and their interactions.
# System Architecture (Concept) --> Linus
# System Architecture (Results) --> Linus
## High-level System-overview  --> Enrico
- what building blocks are needed?
- conceptional
## System Architecture (technical) --> Linus
- diagram of system
- short explanation of each service
## Compiler Engine --> Enrico
## Timeseries Parser --> Linus
- fuseki
- influxdb
- parse from schema
## Webapplication 
### Frontend --> Enrico
### Backend --> Linus
### Reverse Proxy --> Enrico
## Protobuf Service --> Linus
## Deployment & Integration --> Enrico
- DevOps

## Testing --> Linus
- Con

ept,

# Discussion

## Summary  

### Achieved goals

### Unachieved goals

### Workload per student

## Conclusion

### Future work

### Final thoughts

# Bibliography
[1] L. Degen, "Project2: Internet of Soils Revised," unpublished student report, BFH-TI, Biel/Bienne, Jan. 2025.  
[2] K. Schwaber and J. Sutherland, The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game, Scrum.org, Nov. 2020. [Online]. Available: https://scrumguides.org/  
[3] A. Wiggins, The Twelve-Factor App, Heroku, 2011. [Online]. Available: https://12factor.net/
[4] Express, “Express - Node.js web application framework,” [Online]. Available: https://expressjs.com  
[5] Spring, “Spring Boot,” [Online]. Available: https://spring.io/projects/spring-boot  
[6] Actix Project, “Actix Web,” [Online]. Available: https://actix.rs  
[7] FastAPI, “FastAPI - The modern Python web framework,” [Online]. Available: https://fastapi.tiangolo.com  
[8] Meta, React – A JavaScript library for building user interfaces, 2024. [Online]. Available: https://reactjs.org/
[9] Vue.js, The Progressive JavaScript Framework, 2024. [Online]. Available: https://vuejs.org/
[10] Google, Angular – The modern web developer’s platform, 2024. [Online]. Available: https://angular.io/
[11] Triply B.V., "Yasgui – Triply Documentation," [Online]. Available: https://docs.triply.cc/yasgui/.
[12] The Apache Software Foundation, "Fuseki – Serving RDF data over HTTP," Apache Jena Documentation, [Online] Available: https://jena.apache.org/documentation/fuseki2/.
[19] Heltec Automation, “HTCC-AB01 V2,” [Online]. Available: https://heltec.org/project/htcc-ab01-v2/
[20] Heltec Automation, “Programming CubeCell – HTCC-AM01,” [Online]. Available: https://docs.heltec.org/en/node/asr650x/htcc_am01/programming_cubecell.html
[21] Heltec Automation, “Issue #80: Web Serial not working,” GitHub, [Online]. Available: https://github.com/HelTecAutomation/CubeCell-Arduino/issues/80
[22] Heltec Automation, “Issue #281: Serial Upload Problems,” GitHub, [Online]. Available: https://github.com/HelTecAutomation/CubeCell-Arduino/issues/281
[23] Heltec Automation, “CubeCell-Arduino,” GitHub repository, [Online]. Available: https://github.com/HelTecAutomation/CubeCell-Arduino
[24] Heltec Community Forum, “CubeCell Download Tool for Raspberry Pi,” [Online]. Available: http://community.heltec.cn/t/cubecell-download-tool-for-raspberry-pi/2522/12
[25] Heltec Community Forum, “CubeCellFlash Tool,” [Online]. Available: http://community.heltec.cn/t/cubecellflash-tool/1953/3
[26] Heltec Community Forum, “CubeCell Firmware Upload,” [Online]. Available: http://community.heltec.cn/t/cubecell-firmware-upload/1063
[28] Mozilla Developer Network, “Web Serial API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API
[29] Mozilla Developer Network, “WebUSB API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/USB
[30] Mozilla Developer Network, “WebHID API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/WebHID_API
[31] Mozilla Developer Network, “Web Bluetooth API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API
[32] Infineon Technologies AG, Format of .cyacd File for PSoC 3 or PSoC 5LP Bootloader, Knowledge Base Article, Oct. 2020. [Online]. Available: https://community.infineon.com/t5/Knowledge-Base-Articles/Format-of-cyacd-File-for-PSoC-3-or-PSoC-5LP-Bootloader/ta-p/249707
# Declaration of authorship
## Who did what?
### Enrico
- Methods
