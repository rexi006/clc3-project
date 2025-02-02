# Alertmanager Deployment - alerts-manager.yml

## Overview

This file defines the **Alertmanager deployment** in Kubernetes, which is responsible for handling alerts generated by Prometheus. It processes alerts, applies routing rules, and forwards them to the appropriate receiver—in this case, our **Event Processor webhook**.

## Deployment Configuration

### Key Components:

1. **Deployment**
   - Runs a **single replica** of Alertmanager.
   - Loads its configuration from a **ConfigMap** (`alertmanager-config`).
   - Mounts the configuration inside the container.

2. **ConfigMap**
   - Stores the Alertmanager configuration (`alertmanager.yml`).
   - Defines **routing rules** to send alerts to the **Event Processor webhook**.

3. **Service**
   - Exposes Alertmanager within the cluster.
   - Allows Prometheus to communicate with Alertmanager for alert forwarding.

---

## Deployment Details

### 1. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alertmanager
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alertmanager
```

- **`replicas: 1`** → Runs a single instance of Alertmanager.
- **`matchLabels`** → Ensures the correct pod is selected when applying updates.

### 2. Pod Template

```yaml
template:
  metadata:
    labels:
      app: alertmanager
  spec:
    containers:
      - name: alertmanager
        image: prom/alertmanager:latest
        ports:
          - containerPort: 9093
        volumeMounts:
          - name: alertmanager-config-volume
            mountPath: /etc/alertmanager/
            readOnly: true
```

- **`image: prom/alertmanager:latest`** → Uses the latest official Alertmanager image.
- **`containerPort: 9093`** → The application listens on port **9093**.
- **`volumeMounts`** → Mounts the Alertmanager configuration (`alertmanager.yml`) as **read-only**.

### 3. Configuration via ConfigMap

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
data:
  alertmanager.yml: |
    global:
      resolve_timeout: 5m
    route:
      receiver: "webhook"
    receivers:
      - name: "webhook"
        webhook_configs:
          - url: "http://event-processor-service.default.svc.cluster.local:8000/alert"
```

- **`resolve_timeout: 5m`** → Alerts are considered resolved **5 minutes** after they stop firing.
- **`route`** → Defines the default **receiver** (`webhook`).
- **`receivers`** → Sends alerts to our **Event Processor webhook**.

  ```yaml
  webhook_configs:
    - url: "http://event-processor-service.default.svc.cluster.local:8000/alert"
  ```

  - This forwards alerts to the **`/alert` endpoint** of the Event Processor service.
  - In a real-world scenario, you could replace this with **Slack, email, etc.**.

---

## Service Configuration

The **Service** allows Prometheus to communicate with Alertmanager inside the cluster.

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: alertmanager-service
spec:
  selector:
    app: alertmanager
  ports:
    - protocol: TCP
      port: 9093
      targetPort: 9093
  type: ClusterIP
```

### Service Details:

| Parameter      | Value |
|---------------|-------|
| `name`        | alertmanager-service |
| `type`        | ClusterIP (internal service) |
| `port`        | 9093 (accessible within the cluster) |
| `targetPort`  | 9093 (application listens here) |

- **`ClusterIP`** is used because **Prometheus needs internal access** to Alertmanager.
- **Prometheus will send alerts** to `alertmanager-service.default.svc.cluster.local:9093`.

---

## Deployment Commands

### 1. Apply Deployment
```sh
kubectl apply -f alerts-manager.yml
```

### 2. Restart Deployment (after updates)
```sh
kubectl rollout restart deployment alertmanager
```

### 3. Verify Running Pods
```sh
kubectl get pods
```

### 4. Port Forward Alertmanager (to access UI)
```sh
kubectl port-forward svc/alertmanager-service 9093:9093
```

---

## Next Steps

- If you want to **change where alerts are sent**, modify the **`receivers`** section in `alertmanager.yml`.
- To **add Slack/email notifications**, configure `receivers` like this:

  ```yaml
  receivers:
    - name: "slack"
      slack_configs:
        - send_resolved: true
          channel: "#alerts"
          api_url: "<your-slack-webhook-url>"
  ```

- To **test Alertmanager**, manually send a test alert:

  ```sh
  curl -X POST http://alertmanager-service.default.svc.cluster.local:9093/api/v2/alerts \
  -H "Content-Type: application/json" \
  -d '[{
        "labels": { "alertname": "TestAlert", "severity": "critical" },
        "annotations": { "summary": "This is a test alert" },
        "startsAt": "2024-06-01T12:00:00.000Z"
      }]'
  ```

This deployment ensures **alerts are processed correctly**, routed to the right receiver, and visible in Alertmanager.
