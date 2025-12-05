import time
from smart_home import Hogar, Habitacion, Bombilla, AireAcondicionado, Programador, Dispositivo

HOME_STATE_FILE = 'home_state.pkl'

def set_schedule_menu(device: Dispositivo):
    if device.get_scheduler() is None:
        print(f"Creating a new scheduler for {device.get_name()}.")
        device.set_scheduler(Programador(device))
    
    scheduler = device.get_scheduler()
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
                        if scheduler.add_start_event(day, hour, minute, second):
                            print("Start time scheduled.")
                        else:
                            print("Event already scheduled.")
                    else:
                        if scheduler.add_stop_event(day, hour, minute, second):
                            print("Stop time scheduled.")
                        else:
                            print("Event already scheduled.")
                except ValueError as e:
                    print(f"Invalid input: {e}")
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")

def simulate_time(home: Hogar, duration_seconds=60):
    print(f"\n--- Simulating time for {duration_seconds} seconds ---")
    
    all_devices = []
    for room in home.get_rooms():
        for device in room.get_devices():
            all_devices.append(device)

    schedulers = [dev.get_scheduler() for dev in all_devices if dev.get_scheduler() is not None]

    if not schedulers:
        print("No schedules to check.")
        return

    try:
        for i in range(duration_seconds):
            print(f"\nSecond {i + 1}")
            for prog in schedulers:
                prog.check_schedule()
            
            for dev in all_devices:
                print(f"  {str(dev)}")
            
            time.sleep(1)
        print("\nSimulation finished.")
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

def device_control_menu(home: Hogar):
    controlling = True
    while controlling:
        print("\n--- Device Control ---")
        all_devices = []
        for room in home.get_rooms():
            for device in room.get_devices():
                all_devices.append((room, device))

        if not all_devices:
            print("No devices to control.")
            return

        for i, (room, device) in enumerate(all_devices):
            print(f"{i + 1}. {device.get_name()} in {room.get_name()} ({str(device)})")
        
        print("0. Return to main menu")

        try:
            choice = input("Select a device to control: ")
            option = int(choice)
            
            if option == 0:
                controlling = False
            elif 1 <= option <= len(all_devices):
                room, device = all_devices[option - 1]
                control_single_device(device)
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")

def control_single_device(device: Dispositivo):
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
        print("6. Set schedule") # Added scheduler option
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
                amount_str = input("Enter amount (0 for default value): ")
                amount = int(amount_str) if amount_str.isdigit() else 0
                device.increase_intensity(amount)
            elif option == 4:
                amount_str = input("Enter amount (0 for default value): ")
                amount = int(amount_str) if amount_str.isdigit() else 0
                device.decrease_intensity(amount)
            elif option == 5 and isinstance(device, Bombilla):
                color = input("Enter the new color: ")
                device.set_color(color)
            elif option == 6: # Handle scheduler option
                set_schedule_menu(device)
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

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
        print("5. Simulate time") # Added simulate time option
        print("6. Save room log")
        print("7. Save and Exit") # Changed to 7

        option = input("Select an option: ")

        if option == '1':
            print("\n--- Home Status ---")
            for room in home.get_rooms():
                print(f"Room: {room.get_name()}")
                for device in room.get_devices():
                    print(f"  - {str(device)}")
        elif option == '2':
            room_name = input("Name of the new room: ")
            home.add_room(Habitacion(room_name))
            print(f"Room '{room_name}' added.")
        elif option == '3':
            room_name = input("In which room do you want to add the device?: ")
            room = home.get_room(room_name)
            if room:
                device_type = input("What type of device? (bombilla/aire): ").lower()
                device_name = input("Device name: ")
                if device_type == 'bombilla':
                    room.add_device(Bombilla(name=device_name))
                    print("Bulb added.")
                elif device_type == 'aire':
                    room.add_device(AireAcondicionado(name=device_name))
                    print("Air conditioner added.")
                else:
                    print("Invalid device type.")
            else:
                print("The room does not exist.")
        elif option == '4':
            device_control_menu(home)
        elif option == '5': # Handle simulate time option
            try:
                duration = int(input("Enter simulation duration in seconds: "))
                simulate_time(home, duration)
            except ValueError:
                print("Please enter a valid number.")
        elif option == '6': # Handle save room log option
            room_name = input("Which room's log do you want to save?: ")
            room = home.get_room(room_name)
            if room:
                filename = input("Enter the filename for the log (e.g., log.txt): ")
                room.save_log(filename)
            else:
                print("The room does not exist.")
        elif option == '7': # Handle save and exit option
            home.save_to_file(HOME_STATE_FILE)
            print(f"Home state saved to {HOME_STATE_FILE}. Goodbye!")
            running = False
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()
