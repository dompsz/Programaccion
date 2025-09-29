class Bombilla:
    counter = 1  # static counter for auto-naming

    def __init__(self, color="white", intensity=0, name=None):
        if name is None:
            self.name = f"Bombilla{Bombilla.counter}"
            Bombilla.counter += 1
        else:
            self.name = name

        self.is_on = False
        self.intensity = intensity  # 0-100
        self.color = color

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def set_intensity(self, value):
        self.intensity = max(0, min(100, value))

    def set_color(self, color):
        self.color = color

    def get_state(self):
        return f"{self.name}: {'ON' if self.is_on else 'OFF'}, Intensity: {self.intensity}%, Color: {self.color}"

    # overwrites default method to display name instead of object hexadecimal id
    def __str__(self):
        return self.name