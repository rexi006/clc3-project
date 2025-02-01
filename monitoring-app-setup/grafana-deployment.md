# Grafana Deployment - grafana-deployment.yml

## Overview

This file defines the **Grafana deployment** in Kubernetes, which provides visualization and dashboard capabilities for our monitored metrics. Grafana is connected to Prometheus as a **data source**, allowing us to display and analyze the collected metrics in a graphical format.

## Deployment Configuration

### Key Components:

1. **Deployment**
   - Runs a **single replica** of Grafana.
   - Uses the official **Grafana Docker image**.
   - Mounts storage for Grafana's internal database and dashboard configurations.

2. **Service**
   - Exposes Grafana **internally** within the cluster.
   - Allows access to the web interface on **port 3000**.

---

## Deployment Details

### 1. Kubernetes Deployment (`kind: Deployment`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
```

- **`replicas: 1`** → Runs a single instance of Grafana.
- **`matchLabels`** → Ensures the correct pod is selected for this deployment.

### 2. Pod Template

```yaml
template:
  metadata:
    labels:
      app: grafana
  spec:
    containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
          - containerPort: 3000
        volumeMounts:
          - name: grafana-storage
            mountPath: /var/lib/grafana
```

- **`image: grafana/grafana:latest`** → Uses the latest official Grafana image.
- **`containerPort: 3000`** → Grafana's web UI is exposed on port **3000**.
- **`volumeMounts`** → Mounts storage to persist dashboards and settings.

### 3. Persistent Storage

```yaml
volumes:
  - name: grafana-storage
    emptyDir: {}
```

- **`emptyDir: {}`** → data is lost if the pod restarts.
- For production, replace `emptyDir: {}` with a **PersistentVolumeClaim (PVC)**.

---

## Service Configuration

The **Service** exposes Grafana within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: grafana-service
spec:
  selector:
    app: grafana
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
  type: ClusterIP
```

### Service Details:

| Parameter      | Value |
|---------------|-------|
| `name`        | grafana-service |
| `type`        | ClusterIP (internal service) |
| `port`        | 3000 (accessible within the cluster) |
| `targetPort`  | 3000 (application listens here) |

- **`ClusterIP`** means Grafana is **only accessible inside the cluster**.
- To access it from outside, use **port-forwarding**.

---

## Deployment Commands

### 1. Apply Deployment
```sh
kubectl apply -f grafana-deployment.yml
```

### 2. Restart Deployment (after updates)
```sh
kubectl rollout restart deployment grafana
```

### 3. Verify Running Pods
```sh
kubectl get pods
```

### 4. Port Forward Grafana (to access UI)
```sh
kubectl port-forward svc/grafana-service 3000:3000
```

### 5. Open Grafana UI:
```
http://localhost:3000
```

- Default **username/password**:  
  - Username: `admin`
  - Password: `admin` (or set during deployment)

---

## Connecting Grafana to Prometheus

Once Grafana is running, follow the instructions in the file: **grafana-demo.md** 

---

This deployment ensures **real-time monitoring** of our microservices using Prometheus and Grafana.
