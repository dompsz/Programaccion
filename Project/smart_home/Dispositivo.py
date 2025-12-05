class Dispositivo:
    def __init__(self, name, intensity_min=0, intensity_max=100):
        self._name = name
        self._state = "off"
        self._intensity = intensity_min
        self._intensity_min = intensity_min
        self._intensity_max = intensity_max
        self._programador = None

    def get_name(self):
        return self._name

    def get_state(self):
        return self._state

    def get_intensity(self):
        return self._intensity

    def turn_on(self):
        self._state = "on"

    def turn_off(self):
        self._state = "off"

    def increase_intensity(self):
        if self._intensity >= self._intensity_max:
            raise ValueError(f"Cannot increase the intensity of {self._name} any further. Limit reached.")
        self._intensity += 1

    def decrease_intensity(self):
        if self._intensity <= self._intensity_min:
            raise ValueError(f"Cannot decrease the intensity of {self._name} any further. Limit reached.")
        self._intensity -= 1

    def set_programador(self, programador):
        self._programador = programador

    def get_programador(self):
        return self._programador

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self._name,
            'state': self._state,
            'intensity': self._intensity
        }

    def __str__(self):
        return f"Device: {self._name}, State: {self._state}, Intensity: {self._intensity}"
