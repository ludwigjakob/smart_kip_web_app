# SmartKIP Web Application

A Flask-based web interface for controlling the caravan refrigerator fan and smart socket.

## Features
- Display the current temperature behind the refrigerator
- Switch between **manual** and **automatic** fan control
- Toggle a Wi-Fi smart socket (e.g., Tapo P100)
- Store control states in MariaDB
- Trigger analysis jobs from `smart_kip_analyze_data`

## Start the app with Docker
```bash
./start.sh
