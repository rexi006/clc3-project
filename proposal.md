# CLC3 Project Proposal
## Project: Explore Prometheus & Grafana to observe an application
## Goal of the Project
The project aims to design a monitoring system for an IoT-based production simulation using cloud technologies. Therefore, we will use Raspberry Pi devices to simulate a manufacturing process. The generated data will be transmitted to Azure IoT Hub, where it will serve as a centralized communication point between the IoT devices and the cloud infrastructure. To host both Prometheus and Grafana, we will use Azure Kubernetes Service (AKS). Prometheus will be configured to collect metrics like device health from the IoT devices and the cloud infrastructure. We will set up alerting rules in Prometheus to notify us of potential issues. Grafana will be used to visualize the logs.

### High Level Goals

- Simulate a production environment using Rasperry Pi devices
- Integrate IoT devices with Azure IoT Hub
- Use Prometheus to collect metric and trigger alerts for defined thresholds
- Employ Grafana to visualize collected metrics and logs in a dashboard
- Integrate into a Kubernetes-based infrastructure deployed on Azure


### Development and Existing Components

#### Components to build

- Rasperry Pi based IoT production simulation setup with various devices
- Integration of Azure IoT Hub with the simulation setup
- Kubernetes Cluster (AKS) deployment for hosting Prometheus and Grafana
- Prometheus configuration for collecting system metrics and alerting rules
- Grafana dashboards for log visualization and metrics monitoring

#### Existing Components

- Prometheus and Grafana as open-source tools
- Azure IoT Hub
- Azure Kubernetes Service (AKS)

### High-Level Cloud Architecture

#### IoT Layer
- Rasperry Pi devices simulate production by sending data to Azure IoT Hub

#### Cloud Integration
- Azure IoT Hub serves as the bridge between IoT devices and cloud infrastructure
- Azure Kubernetes Service (AKS) hosts Prometheus and Grafana for metrics collection and visualization

#### Monitoring and Alerting
- Prometheus collects application and system metrics from the Kubernetes Cluster
- Alert Manager (part of Prometheus) sends notifications based on thresholds

#### Visualization
- Grafana connects to Prometheus to visualize metrics/logs on dashboards

#### Architecture Diagram

## Setup
### Prerequisites
- Azure account with permissions to create and manage resources.
- Kubernetes CLI 
- Prometheus and Grafana

### Steps
1. **Setup IoT Simulation**
   - configure Raspberry Pi devices to simulate production processes
   - ensure data is sent to Azure IoT Hub

2. **Azure IoT Hub Configuration**
   - create Azure IoT Hub instance
   - register IoT devices and obtain their connection strings

3. **Deploy AKS Cluster**
   - create AKS cluster
   - connect to the AKS cluster

4. **Install Prometheus and Grafana**
   - deploy Prometheus to the AKS cluster
   - deploy Grafana to the AKS cluster
   - configure Prometheus as a data source for Grafana

5. **Dashboard and Alerts**
   - create Grafana dashboards for metrics and logs visualization
   - define Prometheus alert rules and configure notifications


## Relation to Cloud Computing
The project is related to cloud computing because it utilizes cloud-based technologies to manage and scale monitoring solutions. By utilizing Azure IoT Hub, the project collects and processes data from IoT devices in the cloud. Azure Kubernetes Service (AKS) is used for deploying monitoring tools in a scalable manner. Additionally, tools like Prometheus and Grafana are hosted in the cloud, providing real-time monitoring and visualization.

#### Cloud Technologies used
- Azure IoT Hub
- Azure Kubernetes Service (AKS)
- Prometheus
- Grafana

## Milestones
| Milestone               | Description                                      | Deadline |
|-------------------------|--------------------------------------------------|----------|
| Setup IoT Simulation    | Configure Raspberry Pi and IoT Hub              | 24.12.2024   |
| Deploy AKS and Tools    | Install Prometheus and Grafana on AKS           | 24.12.2024   |
| Integrate Monitoring    | Instrument application and configure Prometheus | 31.12.2024   |
| Build Dashboards        | Create Grafana dashboards for visualization     | 06.01.2025   |
| Test and Finalize       | Test alerts and prepare the demo                | 10.01.2025   |


## Distribution of work and responsibilities

| Responsibility               | Team Member                                      | |
|-------------------------|--------------------------------------------------|----------|
| Set up Rasperry Pi and production simulation   | Fabian Altendorfer              |
| Configure Azure IoT Hub and ensure communication with IoT devices    | Fabian Altendorfer           |
| Deploy and manage Kubernetes Cluster (AKS)    | Bernadette Ackerl |
| Configure Prometheus for metrics collection and alerting        | Bernadette Ackerl     |
| Set up Grafana dashboards for visualization       | Regina Gugg                |
| Run simulations and test alerts       | Regina Gugg                |
| Document Results       | All Members                |






