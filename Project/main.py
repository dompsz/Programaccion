import json
from smart_home.Bombilla import Bombilla
from smart_home.AireAcondicionado import AireAcondicionado
from smart_home.Hogar import Hogar

def save_state(home, filename='home_state.json'):
    state = {
        'rooms': {}
    }
    for room_name, devices in home.list_devices().items():
        state['rooms'][room_name] = [d.to_dict() for d in devices]
    
    with open(filename, 'w') as f:
        json.dump(state, f, indent=4)
    print("Home state saved.")

def load_state(filename='home_state.json'):
    try:
        with open(filename, 'r') as f:
            state = json.load(f)
            
        home = Hogar()
        for room_name, devices_data in state['rooms'].items():
            home.add_room(room_name)
            for data in devices_data:
                device = None
                if data['type'] == 'Bombilla':
                    device = Bombilla(name=data['name'], state=data['state'], intensity=data['intensity'], color=data.get('color', 'white'))
                elif data['type'] == 'AireAcondicionado':
                    device = AireAcondicionado(name=data['name'], state=data['state'], temperature=data.get('temperature', 24))
                
                if device:
                    home.add_device(room_name, device)
        print("Home state loaded.")
        return home
    except FileNotFoundError:
        print("No saved state found. Creating a new home.")
        return Hogar()
    except json.JSONDecodeError:
        print("Error reading the state file. Creating a new home.")
        return Hogar()

def device_control_menu(home):
    while True:
        print("\n--- Device Control ---")
        devices = []
        for room, devs in home.list_devices().items():
            for dev in devs:
                devices.append((room, dev))
        
        if not devices:
            print("No devices to control.")
            return

        for i, (room, dev) in enumerate(devices):
            print(f"{i + 1}. {dev.name} in {room} ({dev.get_state()})")
        
        print("0. Return to the main menu and save changes")

        try:
            option = int(input("Select a device to control: "))
            if option == 0:
                save_state(home)
                break
            
            if 1 <= option <= len(devices):
                room, device = devices[option - 1]
                control_device(device)
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")

def control_device(device):
    while True:
        print(f"\n--- Controlling: {device.name} ---")
        print(f"Current state: {device.get_state()}")
        print("1. Turn On")
        print("2. Turn Off")
        print("3. Increase intensity/temperature")
        print("4. Decrease intensity/temperature")
        if isinstance(device, Bombilla):
            print("5. Change color")
        print("0. Stop controlling this device")

        try:
            option = int(input("Select an action: "))
            if option == 0:
                break
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
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    home = load_state()

    while True:
        print("\n--- Main Menu ---")
        print("1. View home status")
        print("2. Add room")
        print("3. Add device")
        print("4. Control devices")
        print("5. Save and Exit")

        option = input("Select an option: ")

        if option == '1':
            print("\n--- Home Status ---")
            for room, devices in home.list_devices().items():
                print(f"Room: {room}")
                for dev in devices:
                    print(f"  - {dev.get_state()}")
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
            save_state(home)
            print("Hasta Luego!")
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()
