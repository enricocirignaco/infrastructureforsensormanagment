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
### Funcional Requirements
- Verwaltung und darstellung von Sensorentypen und Ihre Attributen (z.B. Model, Datasheet, datenformat, lagerbestand)
- Verwaltung und darstellung von Sensorknoten die aus mehrere Sensoren bestehen (z.B. Standort, Sensoren, Projektzugehörigkeit)
- Verwaltung und darstellung von Projekten die aus mehrere Sensorknoten bestehen (z.B. Projektname, Projektbeschreibung)
- Die Webapplikation soll durch zwei verschiedenen Benutzerprofile benutzt werden können: *Researcher* und *Data Analyst*. Der *Researcher* soll Sensoren, Sensorknoten und Projekte erstellen, bearbeiten und löschen können. Der *Data Analyst* soll Sensoren, Sensorknoten und Projekte nur lesen können.
- Die Webapplikation soll nur durch eine Authentifizierung benutzt werden können; ein Authhentifizierung und Authorizierungskonzept soll erarbeitet und implementiert werden.
- Benutzer sollen ihre Passwort zurücksetzen können.
- Das Firmware soll mittels *WebSerial API* direkt vom browser/webapplikation auf den Sensorknoten geflash werden können.
- Optional kann der Benutzer das parametrisierte Firmware auch als Arduino Code heruntergeladen und in eine spätere Zeitpunkt manuell mittels Arduino IDE geflashen.
- Die Webapplikation soll eine REST API zur Verfügung stellen, die die CRUD Operationen für Sensoren, Sensorknoten und Projekte ermöglicht.
- Sensorknoten und Projekten sollen auf TTN automatisch über die REST API provisioniert werden.
- Die Sensordaten sollen vom Sensorknoten über LoRaWAN und *The Things Network* erhoben werden und über MQTT an das Backend gesendet werden.
- Alle Projektdaten sollen in ein Linked Data Triple Store persistiert werden.
in ein InfluxDB gelangen.
- Firmware für die Sensorknoten soll serverseitig parametrisiert und kompiliert werden; Der Benutzer soll die Firmware über die Webapplikation auf den Sensorknoten flashen oder Herunterladen Können.
- Bei der herstellung ein neues Projektes muss eine Gitlab repo angebunden werden. Die Firmware soll vor dem kompilieren aus diesem Repo bezogen werden.
### Non-Functional Requirements
- Die Webapplikation soll auf ein moderne "Single Page Architekture" aufgebaut werden.
- Die REST API soll möglichst unabhängig von der Webapplikation aufgebaut werden und nach denRESTful prinzipien aufgebaut werden.
- Für die Vewaltung von Linked Date sollen geegnete Ontologien und Schemas verwendet werden.
### Optionale Features
- Sensordaten sollen in der Webapplikation visualisiert werden und als CSV exportiert werden können.
- Admin Benutzer um Benutzern zu verwalten und Passwörter zurückzusetzen.
- Sensordaten sollen nicht nur über MQTT aber auch über Webhooks an das Backend gesendet werden können.