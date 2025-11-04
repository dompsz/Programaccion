import datetime
import time
from smart_home.Bombilla import Bombilla
from smart_home.AireAcondicionado import AireAcondicionado
from smart_home.Hogar import Hogar
from smart_home.Programador import Programador

def devices_test():
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

def programador_test():
    print("\nProgramador testing")

    bombilla = Bombilla(name="Night Lamp")
    print(bombilla.get_state())

    prog = Programador(bombilla)
    bombilla.set_programador(prog)

    print("\nWeek days test:", Programador.getWeekDays())
    print("time test:", Programador.getSystemTime())

    try:
        days_map = Programador._DIAS_SEMANA_MAP

        now = datetime.datetime.now()
        print(f"current time: {now.strftime('%H:%M:%S')}")

        start_time = now + datetime.timedelta(seconds=5)
        start_day = days_map[start_time.weekday()]

        stop_time = now + datetime.timedelta(seconds=10)
        stop_day = days_map[stop_time.weekday()]

        print(f"Start planned for: {start_day} {start_time.strftime('%H:%M:%S')}")
        prog.start(start_day, start_time.hour, start_time.minute, start_time.second)

        print(f"Stop planned for: {stop_day} {stop_time.strftime('%H:%M:%S')}")
        prog.end(stop_day, stop_time.hour, stop_time.minute, stop_time.second)

    except Exception as e:
        print(f"Programador setup error: {e}")

    print("\nStarting program loop")

    try:
        for i in range(15):
            print(f"Segunda {i + 1}... {bombilla.get_state()}")
            prog.check_schedule()
            time.sleep(1)

        print("loop stopped")
        print("Final status:", bombilla.get_state())

    except KeyboardInterrupt:
        print("\nprogram stopped")

def main():
    devices_test()
    programador_test()

if __name__ == '__main__':
    main()