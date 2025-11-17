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

    # overwrites default method to display name instead of object hexadecimal id
    def __str__(self):
        return self.name

    # programador methods
    def set_programador(self, programador: 'Programador'):
        self._programador = programador
        print(f"{self.name}: Programador set")

    def get_programador(self):
        if hasattr(self, '_programador'):
            return self._programador
        return None
