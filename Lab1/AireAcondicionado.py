class AireAcondicionado:
    counter = 1  # static counter for auto-naming

    def __init__(self, temperature=24, name=None):
        if name is None:
            self.name = f"AireAcondicionado{AireAcondicionado.counter}"
            AireAcondicionado.counter += 1
        else:
            self.name = name

        self.is_on = False
        self.temperature = temperature

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def set_temperature(self, temperature):
        self.temperature = temperature

    def get_state(self):
        return f"{self.name}: {'ON' if self.is_on else 'OFF'}, Temperature: {self.temperature}°C"

    # overwrites default method to display name instead of object hexadecimal id
    def __str__(self):
        return self.name