#!/bin/bash

# Datei mit der Markdown-Tabelle
FILE="arbeitsjournal.md"

# Variablen für die Gesamtstunden
cirie1_hours=0
degel2_hours=0

# Flag, um erst nach der Trennlinie zu starten
start_reading=false

# Lese die Datei zeilenweise
while IFS='|' read -r blank datum uhrzeit dauer bearbeiter issue taetigkeit; do
    # Überprüfe, ob die Trennlinie erreicht wurde
    if [[ "$datum" == "------------" ]]; then
        start_reading=true
        continue
    fi
    
    # Starte erst nach der Trennlinie
    if [[ "$start_reading" == false ]]; then
        continue
    fi
    
    # Entferne führende und nachfolgende Leerzeichen
    dauer=$(echo "$dauer" | tr -d '[:space:]')
    bearbeiter=$(echo "$bearbeiter" | tr -d '[:space:]')
    
    # Konvertiere Komma in Punkt für Berechnungen
    dauer=$(echo "$dauer" | tr ',' '.')
    
    # Prüfe, wer gearbeitet hat und addiere die Stunden
    if [[ "$bearbeiter" == *"CIRIE1"* ]]; then
        cirie1_hours=$(echo "$cirie1_hours + $dauer" | bc -l)
    fi
    if [[ "$bearbeiter" == *"DEGEL2"* ]]; then
        degel2_hours=$(echo "$degel2_hours + $dauer" | bc -l)
    fi

done < "$FILE"

# Ausgabe der Gesamtstunden
echo "CIRIE1 hat insgesamt $cirie1_hours Stunden gearbeitet."
echo "DEGEL2 hat insgesamt $degel2_hours Stunden gearbeitet."
