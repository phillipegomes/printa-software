import json
import os

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        if not os.path.exists(self.config_path):
            self.config = {}
            self.salvar_config()
        else:
            self.carregar_config()

    def carregar_config(self):
        with open(self.config_path, "r") as f:
            self.config = json.load(f)

    def salvar_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)