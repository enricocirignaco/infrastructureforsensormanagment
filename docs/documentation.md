# Documentation Draft
## Initial Situation
//TODO
## Product deliverables
//TODO
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

## Requirements
//TODO
