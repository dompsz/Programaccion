import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QInputDialog, QMessageBox, 
                             QComboBox, QFormLayout, QDialog, QDialogButtonBox, QSpinBox, QLineEdit)
from PyQt6.QtCore import Qt

from smart_home import Hogar, Habitacion, Bombilla, AireAcondicionado, Programador, Dispositivo

HOME_STATE_FILE = 'home_state.pkl'

class SmartHomeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.home = Hogar()
        self.load_data()
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Smart Home Manager")
        self.setGeometry(100, 100, 900, 600)

        # Dark Mode Stylesheet
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #484b4d;
            }
            QPushButton:pressed {
                background-color: #5c5f61;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #555555;
                font-family: Consolas;
                font-size: 14px;
            }
            QLabel {
                color: #bbbbbb;
                font-size: 14px;
            }
            QInputDialog, QDialog {
                background-color: #2b2b2b;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 4px;
            }
        """)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Control Panel
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        btn_add_room = QPushButton("Add Room")
        btn_add_room.clicked.connect(self.add_room)
        button_layout.addWidget(btn_add_room)

        btn_add_device = QPushButton("Add Device")
        btn_add_device.clicked.connect(self.add_device)
        button_layout.addWidget(btn_add_device)

        btn_control = QPushButton("Control Devices")
        btn_control.clicked.connect(self.control_devices_menu)
        button_layout.addWidget(btn_control)

        btn_simulate = QPushButton("Simulate Time")
        btn_simulate.clicked.connect(self.simulate_time)
        button_layout.addWidget(btn_simulate)

        btn_log = QPushButton("Save Room Log")
        btn_log.clicked.connect(self.save_room_log)
        button_layout.addWidget(btn_log)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save_data)
        button_layout.addWidget(btn_save)

        button_layout.addStretch()

        # Display Area
        display_layout = QVBoxLayout()
        
        self.info_label = QLabel("System Ready")
        self.info_label.setStyleSheet("font-weight: bold; color: #00ff00;") # Green text for status
        display_layout.addWidget(self.info_label)

        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        display_layout.addWidget(self.display_area)

        # Combine layouts
        main_layout.addLayout(button_layout, 1) # 1 part width
        main_layout.addLayout(display_layout, 3) # 3 parts width

        self.show_status() # Show status on startup

    def load_data(self):
        self.home.load_from_file(HOME_STATE_FILE)

    def log_message(self, message):
        self.info_label.setText(message)

    # Actions

    def show_status(self):
        self.display_area.clear()
        rooms = self.home.get_rooms()
        if not rooms:
            self.display_area.setText("No rooms configured.")
            return

        text = "--- HOME STATUS ---\n\n"
        for room in rooms:
            text += f"[{room.get_name()}]\n"
            devices = room.get_devices()
            if not devices:
                text += "  (No devices)\n"
            for device in devices:
                text += f"  - {str(device)}\n"
            text += "\n"
        self.display_area.setText(text)
        self.log_message("Home status updated.")

    def add_room(self):
        name, ok = QInputDialog.getText(self, "Add Room", "Enter room name:")
        if ok and name:
            self.home.add_room(Habitacion(name))
            self.log_message(f"Room '{name}' added.")
            self.show_status()

    def add_device(self):
        rooms = self.home.get_rooms()
        if not rooms:
            QMessageBox.warning(self, "Error", "Add a room first!")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Device")
        layout = QFormLayout(dialog)

        room_combo = QComboBox()
        for r in rooms:
            room_combo.addItem(r.get_name())
        
        type_combo = QComboBox()
        type_combo.addItems(["Bombilla", "AireAcondicionado"])

        name_input = QLineEdit()
        
        # Function to update default device names
        def update_placeholder():
            if type_combo.currentText() == "Bombilla":
                next_name = f"Bombilla{Bombilla._counter}"
            else:
                next_name = f"AireAcondicionado{AireAcondicionado._counter}"
            
            name_input.setPlaceholderText(next_name)

        type_combo.currentTextChanged.connect(update_placeholder)
        update_placeholder()

        layout.addRow("Select Room:", room_combo)
        layout.addRow("Device Type:", type_combo)
        layout.addRow("Device Name:", name_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec():
            room_name = room_combo.currentText()
            dev_type = type_combo.currentText()
            dev_name_input = name_input.text().strip()

            # If input is empty, set to None so the class handles auto-naming
            final_name = dev_name_input if dev_name_input else None

            room = self.home.get_room(room_name)
            if dev_type == "Bombilla":
                room.add_device(Bombilla(name=final_name))
            else:
                room.add_device(AireAcondicionado(name=final_name))
            
            # Get the last added device to show its real name (in case it was auto-generated)
            added_device = room.get_devices()[-1]
            self.log_message(f"{dev_type} '{added_device.get_name()}' added to {room_name}.")
            self.show_status()

    def control_devices_menu(self):
        # 1. Select Device
        all_devices = []
        for r in self.home.get_rooms():
            for d in r.get_devices():
                all_devices.append((r, d))
        
        if not all_devices:
            QMessageBox.information(self, "Info", "No devices to control.")
            return

        device_names = [f"{d.get_name()} (in {r.get_name()})" for r, d in all_devices]
        item, ok = QInputDialog.getItem(self, "Select Device", "Choose a device:", device_names, 0, False)
        
        if ok and item:
            # Find the selected device object
            index = device_names.index(item)
            _, selected_device = all_devices[index]
            self.open_device_control_window(selected_device)

    def open_device_control_window(self, device):
        # Window for controlling a specific device
        control_win = QDialog(self)
        control_win.setWindowTitle(f"Control: {device.get_name()}")
        layout = QVBoxLayout(control_win)

        info_label = QLabel(str(device))
        layout.addWidget(info_label)

        # Buttons
        btn_on = QPushButton("Turn On")
        btn_on.clicked.connect(lambda: [device.turn_on(), info_label.setText(str(device)), self.show_status()])
        layout.addWidget(btn_on)

        btn_off = QPushButton("Turn Off")
        btn_off.clicked.connect(lambda: [device.turn_off(), info_label.setText(str(device)), self.show_status()])
        layout.addWidget(btn_off)

        # Intensity/Temp Control
        intensity_layout = QHBoxLayout()
        
        spin_intensity = QSpinBox()
        # Access protected members to set correct range
        spin_intensity.setRange(device._min_intensity, device._max_intensity)
        spin_intensity.setValue(device.get_intensity_level())
        
        btn_set = QPushButton("Set")
        btn_set.clicked.connect(lambda: self.apply_intensity_change(device, spin_intensity.value(), info_label))

        # Dynamic label based on device type
        label_text = "Temperature:" if isinstance(device, AireAcondicionado) else "Intensity:"
        intensity_layout.addWidget(QLabel(label_text))
        
        intensity_layout.addWidget(spin_intensity)
        intensity_layout.addWidget(btn_set)
        layout.addLayout(intensity_layout)

        # Color (if Bulb)
        if isinstance(device, Bombilla):
            btn_color = QPushButton("Change Color")
            btn_color.clicked.connect(lambda: self.change_color_action(device, info_label))
            layout.addWidget(btn_color)

        # Programador
        btn_sched = QPushButton("Programador")
        btn_sched.clicked.connect(lambda: self.open_scheduler_window(device))
        layout.addWidget(btn_sched)

        control_win.exec()

    def apply_intensity_change(self, device, target_value, label):
        current_value = device.get_intensity_level()
        diff = target_value - current_value
        
        if diff > 0:
            device.increase_intensity(diff)
        elif diff < 0:
            device.decrease_intensity(abs(diff))
        
        label.setText(str(device))
        self.show_status()

    def change_color_action(self, device, label):
        color, ok = QInputDialog.getText(self, "Change Color", "Enter new color:")
        if ok and color:
            device.set_color(color)
            label.setText(str(device))
            self.show_status()

    def open_scheduler_window(self, device):
        if device.get_scheduler() is None:
            device.set_scheduler(Programador(device))
        
        scheduler = device.get_scheduler()
        
        sched_win = QDialog(self)
        sched_win.setWindowTitle(f"Scheduler: {device.get_name()}")
        layout = QFormLayout(sched_win)

        day_combo = QComboBox()
        day_combo.addItems(Programador.get_week_days())
        
        time_input = QLineEdit()
        time_input.setPlaceholderText("HH:MM:SS")

        btn_start = QPushButton("Add Start Event")
        btn_start.clicked.connect(lambda: self.add_event(scheduler, "START", day_combo.currentText(), time_input.text()))

        btn_stop = QPushButton("Add Stop Event")
        btn_stop.clicked.connect(lambda: self.add_event(scheduler, "STOP", day_combo.currentText(), time_input.text()))

        layout.addRow("Day:", day_combo)
        layout.addRow("Time:", time_input)
        layout.addRow(btn_start)
        layout.addRow(btn_stop)

        sched_win.exec()

    def add_event(self, scheduler, type, day, time_str):
        try:
            parts = list(map(int, time_str.split(':')))
            if len(parts) != 3: raise ValueError
            h, m, s = parts
            
            if type == "START":
                res = scheduler.add_start_event(day, h, m, s)
            else:
                res = scheduler.add_stop_event(day, h, m, s)
            
            msg = "Event added." if res else "Event already exists."
            QMessageBox.information(self, "Scheduler", msg)
        except:
            QMessageBox.warning(self, "Error", "Invalid time format (HH:MM:SS)")

    def simulate_time(self):
        seconds, ok = QInputDialog.getInt(self, "Simulate Time", "Seconds to simulate:", 60, 1, 3600)
        if ok:
            # Simple simulation loop (blocking, but okay for this scope)
            all_devs = [d for r in self.home.get_rooms() for d in r.get_devices()]
            schedulers = [d.get_scheduler() for d in all_devs if d.get_scheduler()]
            
            for _ in range(seconds):
                for prog in schedulers:
                    prog.check_schedule()
            
            self.show_status()
            QMessageBox.information(self, "Simulation", f"Simulated {seconds} seconds.")

    def save_room_log(self):
        rooms = self.home.get_rooms()
        if not rooms: return
        
        names = [r.get_name() for r in rooms]
        item, ok = QInputDialog.getItem(self, "Save Log", "Select Room:", names, 0, False)
        
        if ok and item:
            filename, ok2 = QInputDialog.getText(self, "Filename", "Enter filename:", text="log.txt")
            if ok2 and filename:
                room = self.home.get_room(item)
                room.save_log(filename)
                self.log_message(f"Log saved to {filename}")

    def save_data(self):
        self.home.save_to_file(HOME_STATE_FILE)
        self.log_message(f"Home state saved to {HOME_STATE_FILE}.")
        QMessageBox.information(self, "Saved", "Data saved successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartHomeApp()
    window.show()
    sys.exit(app.exec())
