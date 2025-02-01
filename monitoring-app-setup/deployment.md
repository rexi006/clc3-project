# Event Processor Deployment - deployment.yaml

## Overview

This Kubernetes deployment configuration defines how the **Event Processor** service is deployed and managed within the cluster. It ensures that the FastAPI-based microservice runs reliably, integrates with Prometheus for monitoring, and connects to Azure Event Hub for IoT event processing.

## Deployment Configuration

### Key Components:

1. **Deployment**
   - Runs a **single replica** of the event processor (`replicas: 1`).
   - Defines environment variables for Azure Event Hub connectivity.
   - Includes **readiness** and **liveness** probes for health checks.
   - Annotated for **Prometheus scraping** to collect metrics.

2. **Service**
   - Exposes the event processor inside the cluster.
   - Uses **ClusterIP** to allow internal communication between Prometheus, Alertmanager, and other services.

---

## Deployment Details

### 1. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-processor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: event-processor
```

- **`replicas: 1`** → Runs a single instance of the event processor.  
- **`matchLabels`** → Ensures the correct pod is selected when applying updates.  

### 2. Pod Template

```yaml
template:
  metadata:
    labels:
      app: event-processor
    annotations:
      prometheus.io/scrape: "true"
      prometheus.io/path: "/metrics"
      prometheus.io/port: "8000"
```

- **`prometheus.io/scrape: "true"`** → Enables Prometheus to collect metrics from this pod.  
- **`prometheus.io/path: "/metrics"`** → Specifies the endpoint where Prometheus retrieves metrics.  
- **`prometheus.io/port: "8000"`** → Defines the port for metric exposure.

### 3. Container Configuration

```yaml
    spec:
      containers:
      - name: event-processor
        image: bernadetteackerl/event-processor:latest
        ports:
        - containerPort: 8000
```

- **`image: bernadetteackerl/event-processor:latest`** → Pulls the latest event processor image from DockerHub. Change here 'bernadetteackerl' to your own if you have one :) 
- **`containerPort: 8000`** → The application runs on port **8000** inside the container.  

### 4. Environment Variables

```yaml
        env:
        - name: EVENT_HUB_CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: event-hub-secret
              key: EVENT_HUB_CONNECTION_STRING
        - name: WEBHOOK_URL  
          value: "http://event-processor-service.default.svc.cluster.local:8000/alert"
```

- **`EVENT_HUB_CONNECTION_STRING`** → Reads the connection string from a **Kubernetes Secret** (`event-hub-secret`). How to setup the connection string, please have a look at the setup steps in the documentation.md file.
- **`WEBHOOK_URL`** → Defines the webhook URL for Prometheus alerts (internal service communication).  

### 5. Health Checks (Readiness & Liveness Probes)

```yaml
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
```

- **Liveness Probe (`/healthz`)** → Ensures the container is still running.  
- **Readiness Probe (`/ready`)** → Ensures the application is ready to handle traffic before it receives requests.  
- **Delays & Intervals**:
  - Initial delay: **10 seconds**
  - Check interval: **10 seconds**

---

## Service Configuration

The **Service** allows other components (e.g., Prometheus, Alertmanager) to communicate with the event processor.

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: event-processor-service
spec:
  selector:
    app: event-processor
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
```

### Service Details:

| Parameter      | Value |
|---------------|-------|
| `name`        | event-processor-service |
| `type`        | ClusterIP (internal service) |
| `port`        | 8000 (accessible within the cluster) |
| `targetPort`  | 8000 (application listens here) |

- **`ClusterIP`** is used because the service only needs to be accessed **inside the cluster**.
- **Other components (Prometheus, Alertmanager, and Grafana)** can communicate with the event processor via `event-processor-service.default.svc.cluster.local`.

---

## Deployment Commands

### 1. Apply Deployment
```sh
kubectl apply -f deployment.yaml
```

### 2. Restart Deployment (after updates)
```sh
kubectl rollout restart deployment event-processor
```

### 3. Verify Running Pods
```sh
kubectl get pods
```

---

## Next Steps

- If you update `main.py`, **rebuild and push the image** before redeploying:
  ```sh
  docker build --platform linux/amd64 -t <your-dockerhub>/event-processor:latest .
  
  docker push <your-dockerhub>/event-processor:latest
  
  kubectl apply -f deployment.yaml
  
  kubectl rollout restart deployment event-processor
  ```
- Ensure Prometheus is scraping this service (`/metrics`).
- Check logs if the pod is not working properly:
  ```sh
  kubectl logs -l app=event-processor
  ```

This deployment ensures that the event processor remains available, monitored, and integrated with Prometheus and Azure Event Hub.
