# Event Processor - main.py

## Overview

This Python application is a FastAPI-based event processor that integrates with Azure Event Hub to collect IoT device events. It processes incoming telemetry data, exposes Prometheus metrics for monitoring, and provides alerting capabilities via Prometheus Alertmanager. The application runs as a microservice within a Kubernetes cluster.

## Features

- **Event Processing**: Reads events from Azure Event Hub and processes IoT telemetry data.
- **Prometheus Integration**: Exposes metrics (`events_processed_total` and `unique_devices_total`) for monitoring.
- **Alert Handling**: Receives alerts from Prometheus Alertmanager via a webhook endpoint.
- **Health Checks**: Implements `/healthz` and `/ready` endpoints for Kubernetes probes.
- **Testing Capabilities**: Provides a `/simulate_alert` endpoint to manually trigger an alert for testing.

## API Endpoints

| Endpoint                | Method | Description |
|-------------------------|--------|-------------|
| `/`                     | GET    | Returns a simple health message. |
| `/healthz`              | GET    | Kubernetes liveness probe. |
| `/ready`                | GET    | Kubernetes readiness probe. |
| `/get_events`           | GET    | Returns the latest processed events and event count. |
| `/metrics`              | GET    | Exposes Prometheus metrics for scraping. |
| `/received_alerts`      | GET    | Lists all received alerts. |
| `/devices`              | GET    | Shows the count of unique devices and a list of known devices. |
| `/alert`                | POST   | Webhook to receive alerts from Prometheus Alertmanager. |
| `/simulate_alert`       | POST   | Increments event counter to simulate an alert condition. |

## Event Processing

The function `process_events(partition_context, event)` extracts relevant event data from Azure Event Hub, updates the metrics, and stores the event.

### Key Processing Steps:
1. Extracts `device_id` from `event.system_properties`.
2. If the device is new, it is added to `known_devices`, and `UNIQUE_DEVICES` counter is incremented.
3. Appends event data to `event_store` for tracking.
4. Increments the `EVENTS_PROCESSED` counter for Prometheus monitoring.

```python
def process_events(partition_context, event):
    global event_store, known_devices

    event_data = {
        "partition_id": partition_context.partition_id,
        "data": event.body_as_str(),
        "properties": event.properties,
        "system_properties": event.system_properties,
    }

    # Extract device ID from system properties
    device_id = event.system_properties.get(b"iothub-connection-device-id", b"unknown_device").decode("utf-8")

    if device_id not in known_devices:
        known_devices.add(device_id)
        UNIQUE_DEVICES.inc()

    event_store.append(event_data)
    EVENTS_PROCESSED.inc()
```

## Event Hub Listener

The function `azure_eventhub_listener()` starts a background thread to continuously listen for new events from Azure Event Hub.

```python
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
```

A separate thread is used to prevent blocking the main FastAPI application.

## Deployment Considerations

- The application requires an Azure Event Hub connection string, set via the `EVENT_HUB_CONNECTION_STRING` environment variable.
- The service must be deployed inside a Kubernetes cluster with Prometheus scraping enabled.
- When modifying `main.py`, the application must be rebuilt and redeployed:
  ```sh
  docker build --platform linux/amd64 -t <your-dockerhub>/event-processor:latest .
  
  docker push <your-dockerhub>/event-processor:latest
  
  kubectl apply -f deployment.yaml
  
  kubectl rollout restart deployment event-processor
  ```

## Next Steps

- Implement additional event processing logic for different IoT devices.
- Enhance alerting by forwarding notifications to Slack or email.
- Improve logging and error handling for production use cases.

This service serves as the core of the monitoring system, enabling real-time event tracking and alerting in an IoT environment.
