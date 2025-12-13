# SmartKIP Web Application

A Flask-based web interface for controlling the caravan refrigerator fan and smart socket.

## Features
- Display the current temperature behind the refrigerator
- Switch between **manual** and **automatic** fan control
- Toggle a Wi-Fi smart socket (e.g., Tapo P100)
- Store control states in MariaDB
- Trigger analysis jobs from `smart_kip_analyze_data`

## Screenshot of Start Page
![WhatsApp Image 2025-12-13 at 17 54 27](https://github.com/user-attachments/assets/3007ea96-e24e-48ec-85d9-a4151805231c)

## Start the app with Docker
```bash
./start.sh
```

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
This project uses third-party libraries under the following licenses:
- Flask (BSD-3-Clause)
- influxdb-client (MIT)
- python-dotenv (BSD-3-Clause)
- mysql-connector-python (GPL-2.0 with FOSS Exception)
- pandas (BSD-3-Clause)
- requests (Apache-2.0)
