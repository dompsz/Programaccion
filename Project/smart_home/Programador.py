import time
import datetime

class Programador:

    _WEEK_DAYS_MAP = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }

    def __init__(self, device: 'Dispositivo'):
        self._device = device
        self._schedule_list = []

    @classmethod
    def get_week_days(cls) -> list:
        return list(cls._WEEK_DAYS_MAP.values())

    @classmethod
    def get_system_time(cls) -> str:
        now = datetime.datetime.now()
        day_str = cls._WEEK_DAYS_MAP.get(now.weekday(), "Unknown")
        return f"{day_str} {now.strftime('%H:%M:%S')}"

    def start(self, week_day: str, hour: int, minute: int, second: int):
        if week_day not in self.get_week_days():
            print(f"ERROR: Day '{week_day}' is incorrect")
            return

        event = ("START", week_day, hour, minute, second)

        if event not in self._schedule_list:
            self._schedule_list.append(event)
            print(f"Programador: planned activation for {self._device} on {week_day} at {hour:02}:{minute:02}:{second:02}")
        else:
            print("Programador: already planned")

    def end(self, week_day: str, hour: int, minute: int, second: int):
        if week_day not in self.get_week_days():
            print(f"ERROR: Day '{week_day}' is incorrect")
            return

        event = ("STOP", week_day, hour, minute, second)

        if event not in self._schedule_list:
            self._schedule_list.append(event)
            print(f"Programador: planned deactivation for {self._device} on {week_day} at {hour:02}:{minute:02}:{second:02}")
        else:
            print("Programador: already planned")

    def delete(self, week_day: str, hour: int, minute: int, second: int):
        event_start = ("START", week_day, hour, minute, second)
        event_stop = ("STOP", week_day, hour, minute, second)

        if event_start in self._schedule_list:
            self._schedule_list.remove(event_start)
            print(f"Programador: event start deleted at {hour:02}:{minute:02}:{second:02} on {week_day}")
        elif event_stop in self._schedule_list:
            self._schedule_list.remove(event_stop)
            print(f"Programador: event stop deleted at {hour:02}:{minute:02}:{second:02} on {week_day}")
        else:
            print("Programador: event not found")

    def check_schedule(self):
        now = datetime.datetime.now()
        day_str = self._WEEK_DAYS_MAP.get(now.weekday())

        for event in self._schedule_list:
            action_type, day, h, m, s = event

            if (day == day_str and
                    h == now.hour and
                    m == now.minute and
                    s == now.second):

                if action_type == "START":
                    print(f"\n!!! PROGRAMADOR (Time: {self.get_system_time()}) !!!")
                    print(f"-> Enabling {self._device}")
                    self._device.turn_on()

                elif action_type == "STOP":
                    print(f"\n!!! PROGRAMADOR (Time: {self.get_system_time()}) !!!")
                    print(f"-> Disabling {self._device}")
                    self._device.turn_off()
