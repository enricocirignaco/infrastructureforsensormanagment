# Introduction
## Context & Background
- Typical aspects of an IoT application
    - remote sensing and gathering of time-based data
    - transmissioning via (wireless) network
    - persisting of data for later usage/analyzing
- Problems that may arise
- Description of research projects
    - IoS, MUG
    - Technical details
    - Current states
    - pointing out certain problems
## Goal of the project
*Broad system overview (technical range)*

- Centralized management of all data-entities
- Compiling of (hardware-specific) firmware
    - enrich firmware with per-node configurations 
- Templating of sensor nodes to efficiently create mutliple similar ones
- Automatic provisioning of end devices on TTN
    - Keys get generated (on our side) and saved
    - As soon as keys get compiled into firmware and flashed onto hardware, data already reaches TTN

## Value Proposition for Stakeholder
*What problems should be solved? Which aspects of a researcher's life becomes easier?*

- The goal of this project is to simply the workflow of provisioning and managing sensor nodes while making the whole process less error-prune
- All relevant meta-data in one place, external resources can be linked
    -  single source of truth, no scattered data anymore
    - referenced external data can be easily accessed (manuals of sensor node, ttn end devices, positioning of sensor nodes) 
-