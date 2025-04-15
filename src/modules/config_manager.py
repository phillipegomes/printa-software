
import json
import os

class ConfigManager:
    def __init__(self, evento_path="config"):
        self.config_path = os.path.join(evento_path, "config.json")
        os.makedirs(evento_path, exist_ok=True)
        if not os.path.exists(self.config_path):
            self.salvar_config_padrao()

    def salvar_config_padrao(self):
        config_padrao = {
            "ia": {"ativo": True},
            "layout": {"ativo": True},
            "impressao": {"auto": True, "max_por_foto": 5},
            "whatsapp": {"ativo": True},
            "qr": {"ativo": True}
        }
        with open(self.config_path, "w") as f:
            json.dump(config_padrao, f, indent=4)

    def load_config(self):
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except Exception:
            self.salvar_config_padrao()
            return self.load_config()

    def salvar_config(self, config):
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
