from smart_home.Bombilla import Bombilla
from smart_home.AireAcondicionado import AireAcondicionado
from smart_home.Hogar import Hogar

def main():
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
    print("\nDevices:")
    all_devices_map = hogar.list_devices()
    for room, devices in all_devices_map.items():
        print(f"Room {room}: {devices}")

    total_devices, devices_in_each_room = hogar.device_count()
    print(f"\nTotal devices: {total_devices}")
    print("Devices per room: ", devices_in_each_room)

    # Example of modifying a device
    b2 = Bombilla()
    hogar.modify_device("Living Room", b1, b2)
    print("\nDevices:")
    all_devices_map = hogar.list_devices()
    for room, devices in all_devices_map.items():
        print(f"Room {room}: {devices}")

if __name__ == '__main__':
    main()