# Abstract 

# Introduction --> Linus
## Context & Background --> Linus
- Description of MUG, IoS
## Goal of the project --> Linus
- Broad system overview 
## Value Proposition for Stakeholder 

# State of Research --> Enrico
## Retrospect Project2 --> Linus
## Webserial --> Enrico
## Heltec ? --> Enrico
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
[screenshot of kanban board]

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
The Codebase was managed using Git, a single project repositry hosted on github. This allowed for collaborative development, version control, and avoid loosing code. each feature was developed in a separate branch, which was merged into the main branch after review and approval by the other team member. Not only code was versioned with git but all documents related to the project like documentation, diagram and presentations. Documents that were not code were allowed to be pushed directly to the main branch. Tags were used to mark points in the project history when the system was integrated togheter and deployed to the server, allowing for easy rollback if needed. A three version schema was used. the first number was incremented for major releases (0 for the whole development pahse and was then incremented to 1 for the first alpha release.), the second for minor releases (those are everx time a new integration is deployed to prod server), and the third for bugfixes within the prod deployment. Those tags also serverd as triggers for the CI pipeline. this bit will be discummes in details in the section Multistaged GitHub CI Pipeline.
### Microservice Architecture
### Containerization with Docker
### Multistaged GitHub CI Pipeline
### Local Development with Production Parity

## Technology Stack --> Enrico
	•	Overview of used tools/languages
	•	Reasoning for selection



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
# Declaration of authorship
## Who did what?
### Enrico
- Methods
