class AireAcondicionado:
    _counter = 1  # static counter for auto-naming

    def __init__(self, temperature=24, name=None):
        if name is None:
            self._name = f"AireAcondicionado{AireAcondicionado._counter}"
            AireAcondicionado._counter += 1
        else:
            self._name = name

        self._is_on = False
        self._temperature = temperature

    def turn_on(self):
        self._is_on = True

    def turn_off(self):
        self._is_on = False

    def set_temperature(self, temperature):
        self._temperature = temperature

    def get_state(self):
        return f"{self._name}: {'ON' if self._is_on else 'OFF'}, Temperature: {self._temperature}°C"

    # overwrites default method to display name instead of object hexadecimal id
    def __str__(self):
        return self._name