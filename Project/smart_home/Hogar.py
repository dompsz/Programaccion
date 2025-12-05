import pickle
from .Habitacion import Habitacion

class Hogar:
    def __init__(self):
        self._rooms = []

    def add_room(self, room: Habitacion):
        if not any(r.get_name() == room.get_name() for r in self._rooms):
            self._rooms.append(room)

    def get_room(self, room_name: str) -> Habitacion:
        for room in self._rooms:
            if room.get_name() == room_name:
                return room
        return None

    def get_rooms(self):
        return self._rooms

    def save_to_file(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self._rooms, f)
        except IOError as e:
            print(f"Error saving state: {e}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                # Basic validation to check if the loaded data is a list of Habitacion objects
                if isinstance(data, list) and all(isinstance(item, Habitacion) for item in data):
                    self._rooms = data
                else:
                    # If data is not in the expected format, start fresh
                    self._rooms = []
                    print("Warning: State file was in an old format and has been reset.")
        except (FileNotFoundError, EOFError):
            self._rooms = []
        except Exception as e:
            print(f"Error loading state: {e}")
            self._rooms = []
