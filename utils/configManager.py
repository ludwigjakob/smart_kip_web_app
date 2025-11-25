import json
import sys
from debug import Debugger

debug = Debugger()

class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path
        self._config = self._load()

    def _load(self):
        with open(self.path) as f:
            return json.load(f)

    def get_fan_type(self):
        fans = self._config.get("actors", {}).get("fans", [])
        if not fans:
            debug.log("Keine Fans in der Config gefunden", label="Config Error")
            sys.exit(1)

        types = {fan.get("type") for fan in fans}
        if len(types) > 1:
            debug.log(f"Ungültige Config: unterschiedliche Fan-Typen gefunden: {types}", label="Config Error")
            sys.exit(1)

        fan_type = types.pop()
        debug.log(f"Fan-Typ erkannt: {fan_type}", label="Config")
        return fan_type


    def get_threshold_levels(self):
        """Threshold-Levels abhängig vom Fan-Typ bestimmen"""
        fan_type = self.get_fan_type()
        if fan_type == "pwm":
            return [0, 20, 40, 60, 80, 100]
        elif fan_type == "digital":
            return [0, 100]
        else:
            debug.log(f"Unbekannter Fan-Typ: {fan_type}", label="Config Error")
            sys.exit(1)

    def get_sockets(self):
        """Liest die Sockets aus der Config"""
        sockets = self._config.get("actors", {}).get("sockets", [])
        if not sockets:
            debug.log("Keine Socket in der Config gefunden", label="Config")
            return []
        debug.log(f"Socket erkannt: {[s['id'] for s in sockets]}", label="Config")
        return sockets


