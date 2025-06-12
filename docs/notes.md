# Documentation Draft
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

# Ursprüngliche Milestones

| SW    | KW    | Phase                                    |
|-------|-------|------------------------------------------|
| 1-3   | 8-10  | Konzept Phase                            |
| 4-6   | 11-13 | Infrastruktur, Live-Daten, Firmware      |
| 7-8   | 14-15 | Frontend & Backend                       |
| 9     | 16    | *Ferien*                                 |
| 10-11 | 17-18 | Frontend & Backend                       |
| 12-13 | 19-20 | End-to-End                               |
| 14-15 | 21-22 | Feedback-Integration, Optionale Features |
| 16-17 | 23-24 | Projekt Deadline                         |


# Sprint Planing

| Sprint   | SW           | KW    | Phase                                                                  |
|----------|--------------|-------|------------------------------------------------------------------------|
| Sprint 1 | 1,2,3        |       | Konzept Phase, Toolchain, Systemdiagram, Requirements                  |
| Sprint 2 | (3),4,5,6,7? |       | Container-Infrastruktur, Timeseries-Parser, Compile-Engine             |
| Sprint 3 | 8,9          |       | Project, Sensor, Security, Groundwork                                  |
| Sprint 4 | 10,11        |       | Sensor-Node Template, Sensor Nodes                                     |
| Sprint 5 | 12,13        |       | Webserial/Script, Anbindung Compile-Engine / TTN, Protbuf-Service      |
| Sprint 6 | 14,15        |       |                                                                        |
| Sprint 7 | 16,17        |       |                                                                        |


# Sprints tatsächlich

| Sprint   | SW           | KW    | Phase                                                                  |
|----------|--------------|-------|------------------------------------------------------------------------|
| Sprint 1 | 1,2,3        |       | Konzept Phase, Toolchain, Systemdiagram, Requirements                  |
| Sprint 2 | 4,5,6,7      |       | Container-Infrastruktur, Timeseries-Parser, Compile-Engine             |
| Sprint 3 | 8,9,10       |       | Project, Sensor, Security, Groundwork                                  |
| Sprint 4 | 11,12        |       | Sensor-Node Template, Sensor Nodes                                     |
| Sprint 5 | 13,14        |       | Webserial/Script, Anbindung Compile-Engine / TTN, Protbuf-Service      |
| Sprint 6 | 15,16        |       |                                                                        |
| Sprint 7 | 17           |       | **Keine Features mehr -> Film, Doku**  Nur noch Mo-Do                  |


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


# Future Work Notes
- Mark end devices as "archived" on TTN when set so over 
- Improved state management. Certain data should still be changeable even when "In-use"
- data repositores, clean strucuture
    - generate from linkml?
    - use more ontologies?


# Aufgaben letzter Tag
- Formatierung
- Backend/Frontend abgleichen
- Appendix: Meeting Notes
- Appendix: Journal updaten und einfügen
- Appendix: Setup Guide
- Appendix: Requirements
- Abstract schreiben
- Discussion vervollständigen
- who has done what?
- unterschrift dings + absatz bezüglich GPT
- Source hochladen