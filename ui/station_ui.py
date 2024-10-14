import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class StationUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_station_info()

    def initUI(self):
        self.setWindowTitle("My Station")
        self.setWindowIcon(QIcon('assets/HamLog-Logo.png'))
        self.setGeometry(300, 300, 400, 200)
        tab_widget = QTabWidget()
        tab_info = QWidget()
        layout_info = QGridLayout()
        label_name = QLabel("Station Name:")
        self.name_label = QLabel()
        layout_info.addWidget(label_name, 0, 0)
        layout_info.addWidget(self.name_label, 0, 1)
        label_callsign = QLabel("Callsign:")
        self.callsign_label = QLabel()
        layout_info.addWidget(label_callsign, 1, 0)
        layout_info.addWidget(self.callsign_label, 1, 1)
        label_location = QLabel("Station Location:")
        self.location_label = QLabel()
        layout_info.addWidget(label_location, 2, 0)
        layout_info.addWidget(self.location_label, 2, 1)
        label_notes = QLabel("Notes:")
        self.notes_label = QTextBrowser()
        self.notes_label.setReadOnly(True)
        layout_info.addWidget(label_notes, 3, 0)
        layout_info.addWidget(self.notes_label, 3, 1)
        tab_info.setLayout(layout_info)
        tab_edit = QWidget()
        layout_edit = QGridLayout()
        label_name_edit = QLabel("Station Name:")
        self.name_input_edit = QLineEdit()
        layout_edit.addWidget(label_name_edit, 0, 0)
        layout_edit.addWidget(self.name_input_edit, 0, 1)
        label_callsign_edit = QLabel("Callsign:")
        self.callsign_input_edit = QLineEdit()
        layout_edit.addWidget(label_callsign_edit, 1, 0)
        layout_edit.addWidget(self.callsign_input_edit, 1, 1)
        label_location_edit = QLabel("Station Location:")
        self.location_input_edit = QLineEdit()
        layout_edit.addWidget(label_location_edit, 2, 0)
        layout_edit.addWidget(self.location_input_edit, 2, 1)
        label_notes_edit = QLabel("Notes:")
        self.notes_input_edit = QTextBrowser()
        self.notes_input_edit.setReadOnly(False)
        layout_edit.addWidget(label_notes_edit, 3, 0)
        layout_edit.addWidget(self.notes_input_edit, 3, 1)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_station_info)
        layout_edit.addWidget(save_button, 4, 1)
        tab_edit.setLayout(layout_edit)
        tab_widget.addTab(tab_info, "Station Info")
        tab_widget.addTab(tab_edit, "Edit Station")
        layout = QGridLayout()
        layout.addWidget(tab_widget, 0, 0)
        self.setLayout(layout)
        self.name_label.setText("")
        self.callsign_label.setText("")
        self.location_label.setText("")
        self.notes_label.setText("")

    def save_station_info(self):
        name = self.name_input_edit.text()
        callsign = self.callsign_input_edit.text()
        location = self.location_input_edit.text()
        notes = self.notes_input_edit.toPlainText()
        self.name_label.setText(name)
        self.callsign_label.setText(callsign)
        self.location_label.setText(location)
        self.notes_label.setText(notes)
        self.save_to_file(name, callsign, location, notes)

    def save_to_file(self, name, callsign, location, notes):
        data = {
            "name": name,
            "callsign": callsign,
            "location": location,
            "notes": notes
        }

        with open("station_info.json", "w") as file:
            json.dump(data, file)

    def load_station_info(self):
        try:
            with open("station_info.json", "r") as file:
                data = json.load(file)
                self.name_label.setText(data["name"])
                self.callsign_label.setText(data["callsign"])
                self.location_label.setText(data["location"])
                self.notes_label.setText(data["notes"])
        except FileNotFoundError:
            print("Station info file not found.")
        except json.JSONDecodeError:
            print("Invalid JSON format in station info file.")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    app = QApplication(sys.argv)
    station_ui = StationUI()
    station_ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()