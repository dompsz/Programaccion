from abc import ABC, abstractmethod

class Dispositivo(ABC):
    def __init__(self, name, min_intensity=0, max_intensity=100):
        self._name = name
        self._state = False  # False: off, True: on
        self._min_intensity = min_intensity
        self._max_intensity = max_intensity
        self._intensity_level = min_intensity
        self._scheduler = None

    def get_name(self):
        return self._name

    def get_state(self):
        return "On" if self._state else "Off"

    def get_intensity_level(self):
        return self._intensity_level

    def turn_on(self):
        self._state = True

    def turn_off(self):
        self._state = False

    @abstractmethod
    def increase_intensity(self, amount: int = 0):
        pass

    @abstractmethod
    def decrease_intensity(self, amount: int = 0):
        pass

    def set_scheduler(self, scheduler):
        self._scheduler = scheduler

    def get_scheduler(self):
        return self._scheduler

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self._name,
            'state': self._state,
            'intensity_level': self._intensity_level
        }

    def __str__(self):
        return f"Device: {self._name}, State: {self.get_state()}, Intensity: {self._intensity_level}"
