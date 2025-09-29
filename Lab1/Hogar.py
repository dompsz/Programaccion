class Hogar:
    def __init__(self):
        self.rooms = {}  # dictionary: key = room name, value = list of devices

    def add_room(self, name):
        if name not in self.rooms:
            self.rooms[name] = []

    def remove_room(self, name):
        if name in self.rooms:
            del self.rooms[name]

    def add_device(self, room_name, device):
        if room_name in self.rooms:
            self.rooms[room_name].append(device)

    def remove_device(self, room_name, device):
        if room_name in self.rooms and device in self.rooms[room_name]:
            self.rooms[room_name].remove(device)

    def modify_device(self, room_name, old_device, new_device):
        if room_name in self.rooms:
            try:
                index = self.rooms[room_name].index(old_device)
                self.rooms[room_name][index] = new_device
            except ValueError:
                pass

    def list_devices(self):
        for room, devices in self.rooms.items():
            # object to string convert for __str__ trigger to print device name instead of hex id
            device_names = [str(device) for device in devices]
            print(f"Room {room}: {device_names}")

    def device_count(self):
        total = sum(len(d) for d in self.rooms.values())
        per_room = {room: len(d) for room, d in self.rooms.items()}
        print(f"Total devices: {total}")
        print("Devices per room: ", per_room)

    def get_rooms(self):
        return list(self.rooms.keys())
