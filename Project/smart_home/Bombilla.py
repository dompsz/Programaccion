from .Dispositivo import Dispositivo

class Bombilla(Dispositivo):
    _counter = 1

    def __init__(self, name=None, color="white", intensity=0, state=False):
        if name is None:
            name = f"Bombilla{Bombilla._counter}"
            Bombilla._counter += 1
        
        super().__init__(name, min_intensity=0, max_intensity=100)
        self._intensity_level = intensity
        self._color = color
        self._state = state

    def increase_intensity(self, amount: int = 0):
        increment = amount if amount > 0 else 1
        self._intensity_level = min(self._max_intensity, self._intensity_level + increment)

    def decrease_intensity(self, amount: int = 0):
        decrement = amount if amount > 0 else 1
        self._intensity_level = max(self._min_intensity, self._intensity_level - decrement)

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def to_dict(self):
        data = super().to_dict()
        data['color'] = self._color
        return data

    def __str__(self):
        return f"{self._name}: State: {self.get_state()}, Intensity: {self._intensity_level}%, Color: {self._color}"
