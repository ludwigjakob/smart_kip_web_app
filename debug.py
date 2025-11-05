import datetime
import json

class Debugger:
    def __init__(self, config_path='config.json'):
        self.enabled = self.load_mode(config_path)

    def load_mode(self, path):
        try:
            with open(path, 'r') as f:
                config = json.load(f)
                return config.get('mode', 'productive') == 'debug'
        except Exception as e:
            print(f"[Debugger] Fehler beim Laden der Konfiguration: {e}")
            return False

    def log(self, message, label=None):
        if self.enabled:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            prefix = f"[{timestamp}]"
            if label:
                prefix += f" [{label}]"
            print(f"{prefix} {message}")
