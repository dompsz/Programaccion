from .Dispositivo import Dispositivo

class AireAcondicionado(Dispositivo):
    _counter = 1

    def __init__(self, name=None, temperature=24, state="off"):
        if name is None:
            name = f"AireAcondicionado{AireAcondicionado._counter}"
            AireAcondicionado._counter += 1
        
        super().__init__(name, intensity_min=16, intensity_max=30)
        self.intensity = temperature  # use 'intensity' for temperature
        self.state = state

    @property
    def temperature(self):
        return self.intensity

    @temperature.setter
    def temperature(self, value):
        self.intensity = value

    def get_state(self):
        return f"{self.name}: State: {self.state}, Temperature: {self.intensity}°C"

    def to_dict(self):
        data = super().to_dict()
        data['temperature'] = self.intensity
        del data['intensity'] # Rename for clarity
        return data

    # overwrites default method to display name instead of object hexadecimal id
    def __str__(self):
        return self.name
