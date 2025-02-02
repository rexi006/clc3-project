# IoT Monitoring with Prometheus & Grafana
This repository demonstrate a project for the lecture CloudComputing at the University of Applied Sciences Upper Austria.  

Team Members: Ackerl Bernadette, Altendorfer Fabian, Gugg Regina
 
### Goal of the Project

This project focuses on designing a monitoring system for an IoT-based production simulation using cloud technologies. We use a Raspberry Pi device to simulate a manufacturing process, sending data to Azure IoT Hub. The data is then processed by a microservice running in Kubernetes, and the system is monitored using Prometheus and Grafana. 

#### High-Level Objectives

- Simulate a production environment using Raspberry Pi devices.
- Integrate IoT devices with Azure IoT Hub.
- Use Prometheus to collect metrics and trigger alerts based on defined thresholds.
- Use Grafana to visualize collected metrics in a dashboard.
- Deploy a microservice in a Kubernetes-based infrastructure on Azure.

!["Flowchart"](./screenshots/Flowchart.jpg)
## Project Proposal 
- File: proposal.md

## Project Documentations 
- IoT - Part of the Project:
  - Documentation: documentation_iotsetup.md
  - Implementation: simulation.py
- Monitoring - Part of the Project: 
  - Documentation: documentation.md
  - Implementation: monitoring-app-setup/
  - Implementation-Details: monitoring-app-setup/ -> for each yml-file a corresponding explaination-file is provided
- Prometheus - Showcase: 
  - File: alert-demo.md
- Grafana - Showcase and Configuration:
  - File: grafana-demo.md
