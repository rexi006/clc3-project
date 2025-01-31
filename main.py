from fastapi import FastAPI, Request, Response
from prometheus_client import start_http_server, Counter, Gauge, generate_latest
from azure.eventhub import EventHubConsumerClient
import os
import threading
from collections import deque
import logging
import requests

# Prometheus-Metriken
EVENTS_PROCESSED = Counter('events_processed_total', 'Total number of processed events')
UNIQUE_DEVICES = Counter('unique_devices_total', 'Total number of unique IoT devices')

# FastAPI App
app = FastAPI()

# Zwischenspeicher für Events und bekannte Geräte
MAX_EVENTS = 100
event_store = deque(maxlen=MAX_EVENTS)
known_devices = set()  
received_alerts = []

# Logging konfigurieren
logger = logging.getLogger("azure.eventhub")
logging.basicConfig(level=logging.INFO)


@app.get("/")
async def root():
    return {"message": "Event Processor Running"}

# Readiness und Liveness Probes
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

# Endpoint für Event Hub Events abrufen
@app.get("/get_events")
def get_events():
    return {
        "recent_events": list(event_store),
        "event_count": EVENTS_PROCESSED._value.get(),
    }    
    # Events als Liste zurückgeben - altes code snippet für manuelles testen ohne event hub anbindung
    """ return {
        "test": "bekomme events",
        "recent_events": [
            {
                "partition_id": event["partition_id"],
                "data": event["data"],
                "properties": event["properties"],
                "system_properties": event["system_properties"],
            }
            for event in list(event_store)
        ],
        "event_count": EVENTS_PROCESSED._value.get(),
    } """

@app.get("/metrics")
def get_metrics():
    return Response(
        content=generate_latest(),  
        media_type="text/plain"
    )

# Endpoint für empfangene Alarme
@app.get("/received_alerts")
def get_received_alerts():
    return {"received_alerts": received_alerts}

# debugging devices
@app.get("/devices")
def get_known_devices():
    return {
        "counter": UNIQUE_DEVICES._value.get(),  
        "devices": list(known_devices)  
    }

# Alerting Endpoint
@app.post("/alert")
async def receive_alert(request: Request):
    alert_data = await request.json()
    print("Received Alert:", alert_data)

    received_alerts.append(alert_data)
    return {"status": "received"}

# Zum Testen
@app.post("/simulate_alert")
def simulate_alert():
    for _ in range(110):  
        EVENTS_PROCESSED.inc()
    return {"status": "Alert simulated"}


# Event-Verarbeitung
def process_events(partition_context, event):
    global event_store, known_devices

    event_data = {
        "partition_id": partition_context.partition_id,
        "data": event.body_as_str(),
        "properties": event.properties,
        "system_properties": event.system_properties,
    }

    # Extrahiere device-id aus dem event, wegen Check für neues device, unknown_device wird verwendet falls keine device id vorhanden wäre
    device_id = event.system_properties.get(b"iothub-connection-device-id", b"unknown_device").decode("utf-8")    
    
    if device_id not in known_devices:
        known_devices.add(device_id)
        UNIQUE_DEVICES.inc() 

    event_store.append(event_data)
    EVENTS_PROCESSED.inc()
    # updaten um dann stateful zu sein beim events lesen, weil sonst liest man immer alle aus und somit events auch doppelt
    # partition_context.update_checkpoint(event)


# EventHub-Listener starten in eigenem Thread
def azure_eventhub_listener():
    connection_str = os.getenv('EVENT_HUB_CONNECTION_STRING')
    eventhub_name = "clc-project-eventhub-2"

    client = EventHubConsumerClient.from_connection_string(
        connection_str,
        consumer_group="$Default",
        eventhub_name=eventhub_name
    )

    def on_event(partition_context, event):
        process_events(partition_context, event)

    try:
        print("Starting Event Hub Listener...")
        client.receive(
            on_event=on_event,
            starting_position="-1",  
        )
    except KeyboardInterrupt:
        print("Event Hub Listener stopped.")
    finally:
        client.close()

# Thread starten
threading.Thread(target=azure_eventhub_listener, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
