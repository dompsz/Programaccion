import time
from smart_home.Bombilla import Bombilla
from smart_home.AireAcondicionado import AireAcondicionado
from smart_home.Hogar import Hogar
from smart_home.Programador import Programador

# Constant for the state file
HOME_STATE_FILE = 'home_state.pkl'

def device_control_menu(home):
    controlling = True
    while controlling:
        print("\n--- Device Control ---")
        devices = []
        for room, devs in home.list_devices().items():
            for dev in devs:
                devices.append((room, dev))
        
        if not devices:
            print("No devices to control.")
            return

        for i, (room, dev) in enumerate(devices):
            print(f"{i + 1}. {str(dev)} in {room}")
        
        print("0. Return to the main menu and save changes")

        try:
            choice = input("Select a device to control: ")
            option = int(choice)
            
            if option == 0:
                home.save_to_file(HOME_STATE_FILE)
                print("Changes saved.")
                controlling = False
            elif 1 <= option <= len(devices):
                room, device = devices[option - 1]
                control_device(device)
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")

def control_device(device):
    active = True
    while active:
        print(f"\n--- Controlling: {device.get_name()} ---")
        print(f"Current state: {str(device)}")
        print("1. Turn On")
        print("2. Turn Off")
        print("3. Increase intensity/temperature")
        print("4. Decrease intensity/temperature")
        if isinstance(device, Bombilla):
            print("5. Change color")
        print("6. Set schedule")
        print("0. Stop controlling this device")

        try:
            choice = input("Select an action: ")
            option = int(choice)

            if option == 0:
                active = False
            elif option == 1:
                device.turn_on()
            elif option == 2:
                device.turn_off()
            elif option == 3:
                try:
                    device.increase_intensity()
                except ValueError as e:
                    print(f"Error: {e}")
            elif option == 4:
                try:
                    device.decrease_intensity()
                except ValueError as e:
                    print(f"Error: {e}")
            elif option == 5 and isinstance(device, Bombilla):
                color = input("Enter the new color: ")
                device.set_color(color)
            elif option == 6:
                set_schedule_menu(device)
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def set_schedule_menu(device):
    if device.get_programador() is None:
        print(f"Creating a new programador for {device.get_name()}.")
        device.set_programador(Programador(device))
    
    programador = device.get_programador()
    scheduling = True
    while scheduling:
        print(f"\n--- Scheduling for {device.get_name()} ---")
        print("1. Schedule start time")
        print("2. Schedule stop time")
        print("0. Return to device control")

        try:
            choice = input("Select an option: ")
            option = int(choice)

            if option == 0:
                scheduling = False
            elif option in [1, 2]:
                day = input(f"Enter day of the week ({', '.join(Programador.get_week_days())}): ")
                time_str = input("Enter time (HH:MM:SS): ")
                
                try:
                    time_parts = list(map(int, time_str.split(':')))
                    if len(time_parts) != 3:
                        raise ValueError("Invalid time format.")
                        
                    hour, minute, second = time_parts
                    
                    if option == 1:
                        if programador.start(day, hour, minute, second):
                            print("Start time scheduled.")
                        else:
                            print("Event already scheduled.")
                    else:
                        if programador.end(day, hour, minute, second):
                            print("Stop time scheduled.")
                        else:
                            print("Event already scheduled.")
                except ValueError as e:
                    print(f"Invalid input: {e}")
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")

def simulate_time(home, duration_seconds=60):
    print(f"\n--- Simulating time for {duration_seconds} seconds ---")
    
    all_devices = [dev for room in home.list_devices().values() for dev in room]
    programadores = [dev.get_programador() for dev in all_devices if dev.get_programador() is not None]

    if not programadores:
        print("No schedules to check.")
        return

    try:
        for i in range(duration_seconds):
            print(f"\nSecond {i + 1}")
            for prog in programadores:
                prog.check_schedule()
            
            for dev in all_devices:
                print(f"  {str(dev)}")
            
            time.sleep(1)
        print("\nSimulation finished.")
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

def main():
    home = Hogar()
    home.load_from_file(HOME_STATE_FILE)
    print("Home state loaded from", HOME_STATE_FILE)

    running = True
    while running:
        print("\n--- Main Menu ---")
        print("1. View home status")
        print("2. Add room")
        print("3. Add device")
        print("4. Control devices")
        print("5. Simulate time")
        print("6. Save and Exit")

        option = input("Select an option: ")

        if option == '1':
            print("\n--- Home Status ---")
            for room, devices in home.list_devices().items():
                print(f"Room: {room}")
                for dev in devices:
                    print(f"  - {str(dev)}")
        elif option == '2':
            room_name = input("Name of the new room: ")
            home.add_room(room_name)
            print(f"Room '{room_name}' added.")
        elif option == '3':
            room_name = input("In which room do you want to add the device?: ")
            if room_name in home.get_rooms():
                device_type = input("What type of device? (bombilla/aire): ").lower()
                device_name = input("Device name: ")
                if device_type == 'bombilla':
                    home.add_device(room_name, Bombilla(name=device_name))
                    print("Bombilla added.")
                elif device_type == 'aire':
                    home.add_device(room_name, AireAcondicionado(name=device_name))
                    print("Aire acondicionado added.")
                else:
                    print("Invalid device type.")
            else:
                print("The room does not exist.")
        elif option == '4':
            device_control_menu(home)
        elif option == '5':
            try:
                duration = int(input("Enter simulation duration in seconds: "))
                simulate_time(home, duration)
            except ValueError:
                print("Please enter a valid number.")
        elif option == '6':
            home.save_to_file(HOME_STATE_FILE)
            print(f"Home state saved to {HOME_STATE_FILE}. Goodbye!")
            running = False
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()
