from .Dispositivo import Dispositivo

class Bombilla(Dispositivo):
    _counter = 1

    def __init__(self, name=None, color="white", intensity=0, state="off"):
        if name is None:
            name = f"Bombilla{Bombilla._counter}"
            Bombilla._counter += 1
        
        super().__init__(name, intensity_min=0, intensity_max=100)
        self.intensity = intensity
        self.color = color
        self.state = state

    def set_color(self, color):
        self.color = color
        print(f"Color of {self.name} changed to {self.color}")

    def get_state(self):
        return f"{self.name}: State: {self.state}, Intensity: {self.intensity}%, Color: {self.color}"

    def to_dict(self):
        data = super().to_dict()
        data['color'] = self.color
        return data

    def __str__(self):
        return self.name
