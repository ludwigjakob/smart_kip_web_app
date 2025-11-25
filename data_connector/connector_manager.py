from data_connector.temperature_connector import TemperatureConnector
from data_connector.mode_connector import ModeConnector
from data_connector.threshold_connector import ThresholdConnector
from data_connector.analysis_connector import AnalysisConnector
from data_connector.socket_connector import SocketConnector

class ConnectorManager:
    def __init__(self):
        self.connectors = {
            "temperature": TemperatureConnector(),
            "mode": ModeConnector(),
            "threshold": ThresholdConnector(),
            "analysis": AnalysisConnector(),
            "socket": SocketConnector()
        }

    def get(self, sensor_type: str):
        sensor = self.connectors.get(sensor_type)
        if sensor:
            return sensor.read()
        return None

    def set(self, sensor_type: str, value):
        sensor = self.connectors.get(sensor_type)
        if sensor and hasattr(sensor, "write"):
            sensor.write(value)