from .Dispositivo import Dispositivo

class AireAcondicionado(Dispositivo):
    _counter = 1

    def __init__(self, name=None, temperature=24, state=False):
        if name is None:
            name = f"AireAcondicionado{AireAcondicionado._counter}"
            AireAcondicionado._counter += 1
        
        super().__init__(name, min_intensity=16, max_intensity=30)
        self._intensity_level = temperature 
        self._state = state

    def increase_intensity(self, amount: int = 0):
        increment = amount if amount > 0 else 1
        self._intensity_level = min(self._max_intensity, self._intensity_level + increment)

    def decrease_intensity(self, amount: int = 0):
        decrement = amount if amount > 0 else 1
        self._intensity_level = max(self._min_intensity, self._intensity_level - decrement)

    def to_dict(self):
        data = super().to_dict()
        data['temperature'] = self._intensity_level
        del data['intensity_level']
        return data

    def __str__(self):
        return f"{self._name}: State: {self.get_state()}, Temperature: {self._intensity_level}°C"
