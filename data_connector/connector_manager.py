from data_connector.temperature_connector import TemperatureConnector

class ConnectorManager:
    def __init__(self):
        self.connectors = {
            "temperature": TemperatureConnector()
            # Weitere Sensoren hier ergänzen
        }

    def get(self, sensor_type: str):
        sensor = self.connectors.get(sensor_type)
        if sensor:
            return sensor.read()
        return None
