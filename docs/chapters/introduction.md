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

## Goal of the project
*Broad system overview (technical range)*
- title of this thesis already implies that the goal is to build a generic infrastructure which streamlines all processes around handling sensor nodes
- Especially the mentioned problems in the chapter before shall be addressed and solution implemented
- The whole system should be made accessible / used via an intuitive web-based User interface which follows proven guidelines to ensure usability

- concrete features:
- Centralized management of all data-entities
    - Projects group all other entities, so different project with different deployments, sizes, background can all be administrated over one platform
    - Templating of sensor nodes to efficiently create multiple similar ones, shall be reusable across different projects
    - 
    - Relevant attributes of sensor nodes like hardware type, location of deployment, 

- Compiling of (hardware-specific) firmware
    - right source code for firmware should be fetched from Gitlab 
    - enrich firmware with per-node configurations
    - products should be binaries (for flashing), compilation logs as well as generated code for debugging/development

- Flashing of generated binaries onto the hardware
    - Should be as automatically as possible, if contraints (hardware etc.) allow it directly over the developed webapplication
    - alternatively flashed via a script 

- transmissioning of time series data in a speficied schema
    - time series data should be parsed back on a central point independent of data format and then persisted:
        - data should be stored in an influxdb (time series database) because:
            - requirement by stakeholders as this was already used in existing projects
            - influxdb offers a strong UI whcih allows filtering and visualization of data in a straightforward way
        - triplestore to have one linked graph containing all data of the project

- Automatic provisioning of end devices on TTN
    - Keys get generated (on our side) and saved
    - As soon as keys get compiled into firmware and flashed onto hardware, data already reaches TTN


general goals:

- architecture of both system (big picture) and specific software components (small picutre) should follow modern software guidelines to ensure:
- division of responsibilities (layers/microservices) so that they could be exchanged or used on their own
- usage of well-established technologies to build a long-lasting platform 
- built in a portable (right word for containerized?) way so that it can be deployed on various platforms with only a handful of configs

- system should be designed as generic as possible so that it could be used for any similar IoT project (better wording) even outside of academic research for example in the industry
- modular software design simplifies later addition of new specific features for which can be turn on/off 

## Value Proposition for Stakeholder
*What problems should be solved? Which aspects of a researcher's life becomes easier?*

- The goal of this project is to simply the workflow of provisioning and managing sensor nodes while making the whole process less error-prune

- System offers an intuitive UI which acts as a central administration platform that bundles all actions for managing the IoT projects (or sensor nodes/entities?) in one place.

- All relevant meta-data in one data storage, external resources can be linked
    - single source of truth, no scattered data anymore
    - underlying RDF data model is flexible and allows easy extension/adaption for future datamodel changes
    - referenced external data can be easily accessed (manuals of sensor node, ttn end devices, positioning of sensor nodes)
    - time series data stored as well to allow agregated queries over the whole data structure

- Process of compiling and flashing of firmware is streamlined 
    - no more manual looking up and writing of TTN keys when flashing
    - 

- TTN console has not to be touched anymore, fully automatic. Can be directly accessed per sensor node in one click to get more infos


- state management offers easy overview and handling of status of each entity. For example entities that are not used anymore can be archived and thefore hidden in the UI, the data is still accessiable though.
- additional state also shows if deployed sensor node is still sending data or is inactive. This way, a quick overview over all deployed sensor nodes can be gathered
- Deployed and working nodes also display their last transmitted values on the UI, allowing quick insight into current measurements

- Whole system ist built as a generic software solution and can be tailored to specific needs of each project
- groundwork for role based workflows, tailor user interface to the workflow of the user's role and hide irrelevant actions



## Bibliography
[1] L. Degen, "Project2: Internet of Soils Revised," unpublished student report, BFH-TI, Biel/Bienne, 2025.
