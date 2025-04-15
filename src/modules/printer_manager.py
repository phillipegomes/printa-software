import subprocess

class PrinterManager:
    def __init__(self):
        self.print_count = 0

    def get_status(self):
        try:
            result = subprocess.check_output(["lpstat", "-p"], universal_newlines=True)
            if "is idle" in result:
                return "Pronta"
            elif "disabled" in result:
                return "Desativada"
            elif "is printing" in result:
                return "Imprimindo"
            else:
                return "Status desconhecido"
        except Exception as e:
            return f"Erro: {e}"
