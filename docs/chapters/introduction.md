# Introduction
## Context & Background
- motivation / relevance today
- Typical aspects of an IoT application
    - remote sensing and gathering of time-based data
    - transmissioning via (wireless) network
    - persisting of data for later usage/analyzing
- Problems that may arise
- Description of research projects
    - IoS, MUG
        - two research project of the BFH-internal departements AHB and HAFL (collab)
        - very similar in a technical-perspective (data transmission, hardware, used services/tools) as MUG was designed on the experiences made in IoS
        - future research projects may arise with again similar architecture but difference in hardware, data model..
    - Technical details
        - remote sensing of environmental data.
            - Design is as autonomous and long-living as possible, by:
            - power provided by solar panel and lead battery
            - IoS measures soil moisture and temperature in protection forests to estimate how good it's natural protection is
            - MUG measures the impact of urban trees (in big pots) on the urban environemnt as well as many characterstics around the trees themselves
        - transmissioning over LoRaWAN (TTN or Swisscom LPN)
    - Current states **nikita fragen**
        - IoS already was deployed in **ort** for about **time** 
        - MUG had an alpha test but should be deployed this summer
    - pointing out certain problems that hinder the scalability and robunstness of the systems:
        - data gets transmitted in an own binary format, has to be known and correctly handled both in encoding and decoding. May introduce problems when evolving data format by introducing for example a new sensor (all sensor nodes need same format or per node parsing-logic)
        - new sensor nodes have to be flashed manually and the right keys (DevEUI, AppKey) have to be written inside Arduino IDE before compilation. Before that, each end devices gets manually created over the TTN Dashboard. These manual steps may lead to confusing keys and hardware
        - data generated during research projects exist in various formats (excel, csv etc.) and is spread over different locations (gitlab, sharepoint, influxdb). The fragmented filing complicates the linking/collection of data, especially during analysis. These problems also apply to metadata of sensor nodes as firmware-version, exact coordinates of the deployment and TTN keys.
        [1]

## Goal of the project
*Broad system overview (technical range)*
- title of this thesis already implies that the goal is to build an infrastructure which streamlines all processes around handling sensor nodes
- Especially the mentioned problems in the chapter before shall be adressed and solution implemented

- concrete features which :
- Centralized management of all data-entities
    - Projects to bundle other entities.
    - Templating of sensor nodes to efficiently create multiple similar ones
    - Relevant attributes of sensor nodes, 
- Compiling of (hardware-specific) firmware
    - enrich firmware with per-node configurations
- transmissioning of time series data in a speficied format using binary protobuf schemas
    - data should be stored both in a influxdb (time series database) and a triplestore to have a graph containing all relevant data
- Automatic provisioning of end devices on TTN
    - Keys get generated (on our side) and saved
    - As soon as keys get compiled into firmware and flashed onto hardware, data already reaches TTN

general goals:
- architecture of both system (big picture) and specific software components (small picutre) should follow modern guidelines to ensure:
- division of responsibilities (layers/microservices) so that they could be exchanged or used on their own
- usage of well-established technologies to build a long-lasting platform 
- built in a portable (right word for containerized?) way so that it can be deployed on various platforms with only a handful of configs
- system should be designed as generic as possible so that it could be used for any similar IoT project (better wording)

## Value Proposition for Stakeholder
*What problems should be solved? Which aspects of a researcher's life becomes easier?*

- The goal of this project is to simply the workflow of provisioning and managing sensor nodes while making the whole process less error-prune
- All relevant meta-data in one place, external resources can be linked
    -  single source of truth, no scattered data anymore
    - referenced external data can be easily accessed (manuals of sensor node, ttn end devices, positioning of sensor nodes) 
-




## Bibliography
[1] L. Degen, "Project2: Internet of Soils Revised," unpublished student report, BFH-TI, Biel/Bienne, 2025.
