import time

class Programador:

    _DIAS_SEMANA_MAP = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }

    def __init__(self, bombilla: 'Bombilla'):
        self._bombilla = bombilla
        self._programador_list = []

    @classmethod
    def get_week_days(cls) -> list:
        return list(cls._DIAS_SEMANA_MAP.values())

    @classmethod
    def get_system_time(cls) -> str:
        now = time.localtime()
        dia_str = cls._DIAS_SEMANA_MAP.get(now.tm_wday, "Unknown")
        return f"{dia_str} {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"

    def start(self, week_day: str, hour: int, min: int, sec: int):
        if week_day not in self.get_week_days():
            print(f"ERROR: Day '{week_day}' is incorrect")
            return

        evento = ("START", week_day, hour, min, sec)

        if evento not in self._programador_list:
            self._programador_list.append(evento)
            print(f"Programador: planned activation {self._bombilla} w {week_day} o {hour:02}:{min:02}:{sec:02}")
        else:
            print("Programador: already planned")

    def end(self, week_day: str, hour: int, min: int, sec: int):
        if week_day not in self.get_week_days():
            print(f"ERROR: Day '{week_day}' is incorrect")
            return

        evento = ("STOP", week_day, hour, min, sec)

        if evento not in self._programador_list:
            self._programador_list.append(evento)
            print(f"Programador: planned deactivation {self._bombilla} w {week_day} o {hour:02}:{min:02}:{sec:02}")
        else:
            print("Programador: already planned")

    def delete(self, week_day: str, hour: int, min: int, sec: int):
        evento_start = ("START", week_day, hour, min, sec)
        evento_stop = ("STOP", week_day, hour, min, sec)

        if evento_start in self._programador_list:
            self._programador_list.remove(evento_start)
            print(f"Programador: event start deleted at {hour:02}:{min:02}:{sec:02} w {week_day}")
        elif evento_stop in self._programador_list:
            self._programador_list.remove(evento_stop)
            print(f"Programador: event stop deleted at {hour:02}:{min:02}:{sec:02} w {week_day}")
        else:
            print("Programador: event not found")

    def check_schedule(self):
        now = time.localtime()
        dia_str = self._DIAS_SEMANA_MAP.get(now.tm_wday)

        for evento in self._programador_list:
            action_type, day, h, m, s = evento

            if (day == dia_str and
                    h == now.tm_hour and
                    m == now.tm_min and
                    s == now.tm_sec):

                if action_type == "START":
                    print(f"\n!!! PROGRMADOR (Time: {self.get_system_time()}) !!!")
                    print(f"-> Enabling {self._bombilla}")
                    self._bombilla.turn_on()

                elif action_type == "STOP":
                    print(f"\n!!! PROGRMADOR (Time: {self.get_system_time()}) !!!")
                    print(f"-> Disabling {self._bombilla}")
                    self._bombilla.turn_off()