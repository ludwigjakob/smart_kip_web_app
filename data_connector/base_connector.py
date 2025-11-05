from abc import ABC, abstractmethod

class BaseConnector(ABC):
    def __init__(self, name: str, bucket: str):
        self.name = name
        self.bucket = bucket

    @abstractmethod
    def read(self) -> float:
        """Liefert den aktuellsten Messwert aus InfluxDB"""
        pass
