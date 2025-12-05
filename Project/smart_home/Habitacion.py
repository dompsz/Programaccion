import datetime
from .LogHistorico import LogHistorico

class Habitacion(LogHistorico):
    def __init__(self, name):
        self._name = name
        self._devices = []

    def get_name(self):
        return self._name

    def add_device(self, device):
        self._devices.append(device)

    def get_devices(self):
        return self._devices

    def save_log(self, filename: str):
        try:
            with open(filename, 'a') as f:
                f.write(f"--- Log for room '{self._name}' - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                if not self._devices:
                    f.write("No devices in the room.\n")
                else:
                    for device in self._devices:
                        f.write(f"- {str(device)}\n")
                f.write("-" * (25 + len(self._name)) + "\n\n")
            print(f"Log successfully saved to '{filename}'.")
        except IOError as e:
            print(f"Error writing to file '{filename}': {e}")

    def __str__(self):
        return self._name
