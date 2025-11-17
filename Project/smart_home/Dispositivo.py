class Dispositivo:
    def __init__(self, name, intensity_min=0, intensity_max=100):
        self.name = name
        self.state = "off"
        self.intensity = intensity_min
        self._intensity_min = intensity_min
        self._intensity_max = intensity_max
        self._programador = None

    def turn_on(self):
        self.state = "on"
        print(f"{self.name} has been turned on.")

    def turn_off(self):
        self.state = "off"
        print(f"{self.name} has been turned off.")

    def increase_intensity(self):
        if self.intensity >= self._intensity_max:
            raise ValueError(f"Cannot increase the intensity of {self.name} any further. Limit reached.")
        self.intensity += 1
        print(f"Intensity of {self.name} increased to {self.intensity}")

    def decrease_intensity(self):
        if self.intensity <= self._intensity_min:
            raise ValueError(f"Cannot decrease the intensity of {self.name} any further. Limit reached.")
        self.intensity -= 1
        print(f"Intensity of {self.name} decreased to {self.intensity}")

    def set_programador(self, programador):
        self._programador = programador
        print(f"{self.name}: Programador set.")

    def get_programador(self):
        return self._programador

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'state': self.state,
            'intensity': self.intensity
        }

    def __str__(self):
        return f"Device: {self.name}, State: {self.state}, Intensity: {self.intensity}"
