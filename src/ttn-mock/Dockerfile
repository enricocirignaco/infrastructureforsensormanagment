FROM python:3.9-slim

WORKDIR /usr/src/app

# Kopiere requirements und installiere Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Quellcode, das Template und das generierte Protobuf-Modul
COPY . .

CMD ["python", "./mqtt_publisher.py"]
