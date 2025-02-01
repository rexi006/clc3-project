# Prometheus Deployment - prometheus-deployment.yml

## Overview

This file defines the **Prometheus deployment** in Kubernetes, which is responsible for collecting, storing, and querying metrics from monitored services. It is configured to scrape data from the **event-processor-service** and trigger alerts when predefined conditions are met.

For a demo/flow-showcase have a look at the file: **alert-demo.md**

## Deployment Configuration

### Key Components:

1. **Deployment**
   - Runs a **single instance** of Prometheus.
   - Loads Prometheus configuration from a **ConfigMap**.
   - Scrapes metrics from the `event-processor-service` at **port 8000**.
   - Uses alerting rules to send notifications via **Alertmanager**.

2. **Service**
   - Exposes Prometheus **internally** within the cluster.
   - Accessible on **port 9090** for querying metrics.

3. **ConfigMap**
   - Stores Prometheus configuration (`prometheus.yml`).
   - Defines scrape targets and alerting rules (`alerts.yml`).

---

## Deployment Details

### 1. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
```

- **`replicas: 1`** → Runs a single Prometheus instance.
- **`matchLabels`** → Ensures the correct pod is selected for this deployment.

### 2. Pod Template

```yaml
template:
  metadata:
    labels:
      app: prometheus
  spec:
    containers:
      - name: prometheus
        image: prom/prometheus
        args:
          - "--config.file=/etc/prometheus/prometheus.yml"
        ports:
          - containerPort: 9090
        volumeMounts:
          - name: prometheus-config
            mountPath: /etc/prometheus/
```

- **`image: prom/prometheus`** → Uses the official Prometheus image.
- **`containerPort: 9090`** → Prometheus UI is exposed on **port 9090**.
- **`--config.file=/etc/prometheus/prometheus.yml`** → Specifies the config file location.

### 3. Persistent Configuration

```yaml
volumes:
  - name: prometheus-config
    configMap:
      name: prometheus-config
```

- Stores the Prometheus configuration in a **ConfigMap**.
- Ensures Prometheus loads its configuration when the pod restarts.

---

## Service Configuration

The **Service** exposes Prometheus within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
spec:
  selector:
    app: prometheus
  ports:
    - protocol: TCP
      port: 9090
      targetPort: 9090
```

### Service Details:

| Parameter      | Value |
|---------------|-------|
| `name`        | prometheus-service |
| `type`        | ClusterIP (internal service) |
| `port`        | 9090 (accessible within the cluster) |
| `targetPort`  | 9090 (application listens here) |

- **`ClusterIP`** makes Prometheus **accessible only inside Kubernetes**.
- To access it from outside, use **port-forwarding**.

---

## ConfigMap Configuration

Prometheus loads its configuration from a **ConfigMap**, which includes **scraping rules**, **alerting rules**, and the connection to Alertmanager.

### 1. Prometheus Configuration (`prometheus.yml`)

```yaml
global:
  scrape_interval: 15s 
```
- Defines a **scrape interval** of **15 seconds** (how often Prometheus collects metrics).

```yaml
scrape_configs:
  - job_name: "event-processor"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["event-processor-service.default.svc.cluster.local:8000"]
```
- **Scrapes metrics** from the **event-processor-service**.
- Fetches data from **`/metrics`** endpoint.
- Uses the Kubernetes service name:  
  `event-processor-service.default.svc.cluster.local:8000`.

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - "alertmanager-service.default.svc.cluster.local:9093"
```
- **Sends alerts** to Alertmanager running at:  
  `alertmanager-service.default.svc.cluster.local:9093`.

### 2. Alerting Rules (`alerts.yml`)

```yaml
groups:
  - name: event_alerts
    rules:
      - alert: HighEventRate
        expr: events_processed_total > 100
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Too many events processed"
          description: "More than 100 events were processed in a short time."
```
- **Triggers an alert** when the total number of processed events **exceeds 100** within 1 minute.
- **Severity** is marked as **"warning"**.

```yaml
      - alert: NewIoTDevice
        expr: increase(unique_devices_total[1m]) > 0
        for: 1m
        labels:
          severity: info
        annotations:
          summary: "New IoT device detected"
          description: "A new IoT device has been registered."
```

---

## Deployment Commands

### 1. Apply Deployment
```sh
kubectl apply -f prometheus-deployment.yml
```

### 2. Restart Deployment (after updates)
```sh
kubectl rollout restart deployment prometheus
```

### 3. Verify Running Pods
```sh
kubectl get pods
```

### 4. Port Forward Prometheus (to access UI)
```sh
kubectl port-forward svc/prometheus-service 9090:9090
```

### 5. Open Prometheus UI:
```
http://localhost:9090
```

- Navigate to **Status → Targets** to check if **event-processor-service** is being scraped.
- Navigate to **Alerts** to see **active alerts**.

---

### How to add a new alert

Please have a look at the file **alert-demo.md**

---
This deployment ensures **real-time monitoring and alerting** of our IoT-based microservice.

