from Bombilla import Bombilla
from AireAcondicionado import AireAcondicionado
from Hogar import Hogar

# Bombilla
print("\nHU01: Bombilla")
b1 = Bombilla()
b1.turn_on()
b1.set_intensity(75)
b1.set_color("red")
print(b1.get_state())
b1.turn_off()
b1.set_intensity(40)
b1.set_color("blue")
print(b1.get_state())

# AireAcondicionado
print("\nHU02: AireAcondicionado")
ac1 = AireAcondicionado(20, "Bedroom AC")
ac1.turn_on()
ac1.set_temperature(22)
print(ac1.get_state())
ac1.set_temperature(26)
ac1.turn_off()
print(ac1.get_state())

# Hogar
print("\nHU03: Hogar")
hogar = Hogar()
hogar.add_room("Living Room")
hogar.add_room("Bedroom")
hogar.add_device("Living Room", b1)
hogar.add_device("Bedroom", ac1)

print("Existing rooms:", hogar.get_rooms())
hogar.list_devices()
hogar.device_count()
print()

# Example of modifying a device
b2 = Bombilla()
hogar.modify_device("Living Room", b1, b2)
hogar.list_devices()