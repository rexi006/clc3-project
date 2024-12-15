# CLC3 Project Proposal

## Project: Explore Prometheus & Grafana to observe an application

## Goal of the Project

The project aims to design a monitoring system for an IoT-based production simulation using cloud technologies. Therefore, we will use Raspberry Pi devices to simulate a manufacturing process. The generated data will be transmitted to Azure IoT Hub, where it will serve as a centralized communication point between the IoT devices and the cloud infrastructure. To host both Prometheus and Grafana, we will use Azure Kubernetes Service (AKS). Prometheus will be configured to collect metrics like device health from the IoT devices and the cloud infrastructure. We will set up alerting rules in Prometheus to notify us of potential issues. Grafana will be used to visualize the logs.

#### Overview of Features

- Simulate a production environment using Rasperry Pi devices
- Integrate IoT devices with Azure IoT Hub
- Host monitoring tools on a Kubernetes Cluster in Azure (AKS)
- Collect metrics and logs using Prometheus
- Visualize metrics and logs with Grafana dashboards
- Implement alerting to detect and notify of system issues


#### High Level Goal

- Build a cloud-based monitoring system for IoT-enabled production simulation
- Use Prometheus to collect metric and trigger alerts for defined thresholds
- Employ Grafana to visualize collected metrics and logs in a user-friendly dashboard
- Integrate these monitoring tools into a Kubernetes-based infrastructure deployed on Azure

