# Abstract 

# Introduction --> Linus
## Context & Background --> Linus
- Description of MUG, IoS
## Goal of the project --> Linus
- Broad system overview 
## Value Proposition for Stakeholder --> Linus

# State of Research
This chapter provides an overview of existing research and available technologies relevant to the project. The focus lies on niche or emerging tools and methods that appeared promising but required feasibility evaluation before adoption. Most of the research was conducted during the conceptual phase, where assessing the practicality and integration potential of such technologies was critical for planning and system design.
## Retrospect Project2 --> Linus
## Webserial --> Enrico
#### Research
After reading the poorly documented documentation of the CubeCell board if was discovered that neigher the bootloader that works with the arduino enviroment nor the utility to flash the arduino code on the board are open source. Only their binaries are provided. This complicate the work of the developers a lot.
As described here [20] the Cubecell in question supports two different bootloaders, one of them is arduino compatible but as can be seen from the screenshoot on the same page this bootloader is closed source and it's not avalable to the public. Different issues on the matter were already started on github like this [21]. In this gitlab issue[22] someone is even accusing Heltec of misusing the GCC compiler that is under GPL license. So it's clear that this company is not interrested in open sourcing it's development tools and thus aworkaround should be found.
To better understand what exactly it's missing to be able to flash a firmware on the cubecell board the compilation and flashing process via the arduino IDE was closely investigated. Before any code can be compiled for this board the Hardware-specific files must be installed to the Arduino IDE using its board manager. The Board manange does nothing else than downloading the content of the following gitlab repository [23]. By getting a look at the get.py file in the tools folder the following line can be seen:
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
- **CubeCellflash**: This tool is usedd to flash boards with a ASR650x series chip [24]
- **flash6601**: This tool is used to flash boards with a ASR6601 series chip [24]
Those tools are provided as binaries for linux and macos and as exe for windows but only for x86 CPU architecture. Additionally a arm binary compatible with raspberry Pi is provided for the CubeCellflash utility.
There is some sparse informations on how to use those tools in different forum posts like this[25] and this [26] but no official documentation was found. The exact usage can be reverse engineered by looking enabling verbose logging in the arduino IDE and trying to compile and flash a test firmware on the board.
<!-- write here your findings with arduino ide -->

Because of the closed source nature and the lack of ready to use tools it's unlikely that upload-via-browser functionality can be implemented. The only way to flash the firmware on the board is to use the provided binaries, either directly of via arduino toolchain.

Another interesting software is the arduino create agent (also named arduino cloud agent). This is an utility that needs to be locally installed on the host machine that can communicate with the arduino cloud (browser based arduino IDE) and practically giving the possibility to program and debug arduino boards via browser[27]. It's unclear if this software can be used to flash the firmware on the Heltec boards. 
If the arduino create agent can be used for our project, it would simply and speed up the development process. Otherwise a custom solution with a similar approach as the arduino create agent has to be developed.

The idea would be to create an application that exposes a rest api that can be used by the webapplication to send the binary and integrates the propetary flashing tools of heltec to be able to flash the binary on the board. The application should be packaged in a single executable for easy installation.
#### Followups
After further analysis and siscussion with the team and stakeholders it was decided to move in two different directions. The first high priority task is to implement a solution so that the user can program the heltech hardware in a as hasslyfree as possible way without using the invaiable webserial API. This means that the requirements that no addtional software is allowedto be installed on the host machine is lifted. The second task is to try to get a working solution using the webserial API for flashing a compatible Hardware board. This will provide a proof of concept for the webserial API and the idel workflow can be demostraded. This proof of concept can also be used in future project to convince the stakeholders to adopt an hardware platform conpatible with the webserial API and thus leveraging the advantages of this technology.
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
[27] Arduino, “Arduino Cloud Agent,” [Online]. Available: https://docs.arduino.cc/arduino-cloud/hardware/cloud-agent/
[28] Mozilla Developer Network, “Web Serial API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API
[29] Mozilla Developer Network, “WebUSB API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/USB
[30] Mozilla Developer Network, “WebHID API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/WebHID_API
[31] Mozilla Developer Network, “Web Bluetooth API,” [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API
# Declaration of authorship
## Who did what?
### Enrico
- Methods
