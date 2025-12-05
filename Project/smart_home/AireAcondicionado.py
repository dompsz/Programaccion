from .Dispositivo import Dispositivo

class AireAcondicionado(Dispositivo):
    _counter = 1

    def __init__(self, name=None, temperature=24, state="off"):
        if name is None:
            name = f"AireAcondicionado{AireAcondicionado._counter}"
            AireAcondicionado._counter += 1
        
        super().__init__(name, intensity_min=16, intensity_max=30)
        self._intensity = temperature 
        self._state = state

    @property
    def temperature(self):
        return self._intensity

    @temperature.setter
    def temperature(self, value):
        if self._intensity_min <= value <= self._intensity_max:
            self._intensity = value
        else:
            raise ValueError(f"Temperature must be between {self._intensity_min} and {self._intensity_max}")

    def to_dict(self):
        data = super().to_dict()
        data['temperature'] = self._intensity
        del data['intensity']
        return data

    # overwrites default method to display name instead of object hexadecimal id
    def __str__(self):
        return f"{self._name}: State: {self._state}, Temperature: {self._intensity}°C"
