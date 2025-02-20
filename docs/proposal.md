# "Infrastructure for Sensor Management"

## Einleitung

In der Projekt-2-Arbeit "Internet of Soils Revised" wurde ein Sensornetzwerk
der BFH AHB untersucht, welches im Rahmen eines Forschungsprojektes umgesetzt
wurde. Es wurden Möglichkeiten zur Vereinfachung der Inbetriebnahme und des
Betriebes dieses und ähnlicher Projekte untersucht. Im Bericht zu der Arbeit
werden in einem Lösungsvorschlag verschiedene Erweiterungen und Verbesserungen
vorgeschlagen, die nun in dieser Bachelorthesis umgesetzt werden sollen.

## Aufgabe

Basierend auf den Erkenntnissen aus der Projekt-2-Arbeit soll eine
Infrastruktur zur Dokumentation, Inbetriebnahme und zum Betrieb der Sensoren
entwickelt werden. Diese soll auf der bestehenden Sensor-Hardware aufsetzen und
an die bestehenden Entwicklungsprozesse anknüpfen. Teil dieser Infrastruktur
sind:

1. Eine zentrale Verwaltung relevanter Attribute zu den Sensoren. Dies
   beinhaltet u.a. Informationen zu Typ/Standort, zur Sensor-HW und Firmware,
   sowie die Möglichkeit, weitere Informationen (z.B. Kalibrationsdaten,
   Bilddokumentation) zu verlinken. Die Daten sollen als Linked Data (RDF)
   abgelegt werden, z.B. in einem Triplestore und es sollen, wo möglich,
   geeignete Schemas und Ontologien verwendet werden.

2. Eine Schnittstelle zu The Things Network (TTN, Anbindung der Sensoren via
   LoRaWAN), über welche einerseits die Sensoren provisioniert werden können,
   und andererseits die Messwerte empfangen werden. Die Messwerte sollen
   ebenfalls als Linked Data abgelegt werden, z.B. mit für Zeitserien
   geeigneten Schemas und Ontologien. Die bestehende Datenerfassung mittels
   InfluxDB soll dabei beibehalten werden.

3. Ein automatisiertes Build-System zum kompilieren der pro Sensor spezifischen
   Firmware. Dieses soll basierend auf den Attributen der Sensoren aus Punkt 1
   entsprechende Releases aus dem BFH-GitLab beziehen, ggf. anpassen (ersetzen
   von Werten mittels Templating) und ein Firmware-Image kompilieren.

4. Ein Mechanismus zum einspielen der Firmware auf die Sensoren. Der Prozess
   soll weitestgehend automatisiert sein: Im Idealfall wird ein neuer Sensor
   mit allen relevanten Attributen erfasst, worauf automatisch eine
   Registrierung bei TTN stattfindet und das kompilieren der Firmware
   ausgelöst wird. Der Sensor muss dann nur noch an einen Computer
   angeschlossen und die Firmware aufgespielt werden. Auch dieser Schritt soll
   wenn möglich automatisch, insbesondere jedoch ohne die bisher eingesetzte
   Arduino-IDE möglich sein.

5. Für die Punkte 1 und 2 soll ein ansprechendes und einfach zu bedienendes
   Web-Interface erstellt werden.
