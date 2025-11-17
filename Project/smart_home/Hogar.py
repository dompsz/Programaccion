class Hogar:
    def __init__(self):
        self._rooms = {}  # dictionary: key = room name, value = list of devices

    def add_room(self, name):
        if name not in self._rooms:
            self._rooms[name] = []

    def remove_room(self, name):
        if name in self._rooms:
            del self._rooms[name]

    def add_device(self, room_name, device):
        if room_name in self._rooms:
            self._rooms[room_name].append(device)

    def remove_device(self, room_name, device):
        if room_name in self._rooms and device in self._rooms[room_name]:
            self._rooms[room_name].remove(device)

    def modify_device(self, room_name, old_device, new_device):
        if room_name in self._rooms:
            try:
                index = self._rooms[room_name].index(old_device)
                self._rooms[room_name][index] = new_device
            except ValueError:
                pass

    def list_devices(self):
        return self._rooms

    def device_count(self):
        total = sum(len(d) for d in self._rooms.values())
        per_room = {room: len(d) for room, d in self._rooms.items()}
        return total, per_room

    def get_rooms(self):
        return list(self._rooms.keys())
