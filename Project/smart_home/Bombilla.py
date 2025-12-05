from .Dispositivo import Dispositivo

class Bombilla(Dispositivo):
    _counter = 1

    def __init__(self, name=None, color="white", intensity=0, state="off"):
        if name is None:
            name = f"Bombilla{Bombilla._counter}"
            Bombilla._counter += 1
        
        super().__init__(name, intensity_min=0, intensity_max=100)
        self._intensity = intensity
        self._color = color
        self._state = state

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def to_dict(self):
        data = super().to_dict()
        data['color'] = self._color
        return data

    def __str__(self):
        return f"{self._name}: State: {self._state}, Intensity: {self._intensity}%, Color: {self._color}"
