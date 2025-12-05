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

    def add_start_event(self, week_day: str, hour: int, minute: int, second: int) -> bool:
        if week_day not in self.get_week_days():
            raise ValueError(f"ERROR: Day '{week_day}' is incorrect")

        event = ("START", week_day, hour, minute, second)

        if event not in self._schedule_list:
            self._schedule_list.append(event)
            return True
        return False

    def add_stop_event(self, week_day: str, hour: int, minute: int, second: int) -> bool:
        if week_day not in self.get_week_days():
            raise ValueError(f"ERROR: Day '{week_day}' is incorrect")

        event = ("STOP", week_day, hour, minute, second)

        if event not in self._schedule_list:
            self._schedule_list.append(event)
            return True
        return False

    def delete_event(self, week_day: str, hour: int, minute: int, second: int) -> bool:
        event_start = ("START", week_day, hour, minute, second)
        event_stop = ("STOP", week_day, hour, minute, second)

        if event_start in self._schedule_list:
            self._schedule_list.remove(event_start)
            return True
        elif event_stop in self._schedule_list:
            self._schedule_list.remove(event_stop)
            return True
        return False

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
                    self._device.turn_on()

                elif action_type == "STOP":
                    self._device.turn_off()
