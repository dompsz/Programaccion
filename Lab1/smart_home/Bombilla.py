class Bombilla:
    _counter = 1  # static counter for auto-naming

    def __init__(self, color="white", intensity=0, name=None):
        if name is None:
            self._name = f"Bombilla{Bombilla._counter}"
            Bombilla._counter += 1
        else:
            self._name = name

        self._is_on = False
        self._intensity = intensity  # 0-100
        self._color = color

    def turn_on(self):
        self._is_on = True

    def turn_off(self):
        self._is_on = False

    def set_intensity(self, value):
        self._intensity = max(0, min(100, value))

    def set_color(self, color):
        self._color = color

    def get_state(self):
        return f"{self._name}: {'ON' if self._is_on else 'OFF'}, Intensity: {self._intensity}%, Color: {self._color}"

    # overwrites default method to display name instead of object hexadecimal id
    def __str__(self):
        return self._name

    #programador methods
    def set_programador(self, programador: 'Programador'):
        self._programador = programador
        print(f"{self._name}: Programador set")

    def get_programador(self):
        if hasattr(self, '_programador'):
            return self._programador
        return None