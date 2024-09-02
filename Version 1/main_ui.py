import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QDateEdit, QTimeEdit, QLineEdit, QDoubleSpinBox, QComboBox, QTextEdit, QPushButton, QFormLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from station_ui import StationUI

class HamRadioLogbook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HamLog")
        self.setGeometry(0, 0, 800, 600)
        self.showMaximized()
        self.create_menu_bar()
        self.create_menu_bar_connections()
        self.create_tab_widget()

    def open_station_ui(self):
        self.station_ui = StationUI()
        self.station_ui.show()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #800000;
                color: white;
                font-size: 14pt;
                padding: 20px;
            }
            QMenuBar::item {
                background-color: #800000;
                color: white;
            }
            QMenu {
                background-color: #800000;
                color: white;
            }
            QMenu::item {
                background-color: #800000;
                color: white;
            }
        """)
        home_menu = menu_bar.addMenu("Home")
        home_menu.setObjectName("Home")
        my_station_action = QAction("My Station", self)
        home_menu.addAction(my_station_action)
        my_station_action.triggered.connect(self.open_station_ui)
        home_menu.addSeparator()
        exit_hamlog_action = QAction("Exit HamLog", self)
        exit_hamlog_action.setObjectName("Exit HamLog")
        exit_hamlog_action.triggered.connect(self.close)
        home_menu.addAction(exit_hamlog_action)
        logbook_menu = menu_bar.addMenu("Logbook")
        logbook_menu.setObjectName("Logbook")
        export_logs_action = QAction("Export Logs", self)
        export_logs_action.setObjectName("Export Logs")
        logbook_menu.addAction(export_logs_action)
        erase_all_logs_action = QAction("Erase All Logs", self)
        erase_all_logs_action.setObjectName("Erase All Logs")
        logbook_menu.addAction(erase_all_logs_action)

    def create_tab_widget(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setMovable(True)
        tab1 = QWidget()
        tab2 = QWidget()
        self.tab_widget.addTab(tab1, "New Contact")
        self.tab_widget.addTab(tab2, "View Contacts")
        tab1_layout = QVBoxLayout()
        tab1_layout.setContentsMargins(20, 20, 20, 20)
        tab1_layout.setSpacing(20)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft)
        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setCalendarPopup(True)
        self.date_input.setObjectName("date_input")
        form_layout.addRow("Date", self.date_input)
        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm:ss")
        self.time_input.setObjectName("time_input")
        form_layout.addRow("Time", self.time_input)
        self.callsign_input = QLineEdit()
        self.callsign_input.setObjectName("callsign_input")
        form_layout.addRow("Callsign", self.callsign_input)
        self.name_input = QLineEdit()
        self.name_input.setObjectName("name_input")
        form_layout.addRow("Name", self.name_input)
        frequency_layout = QHBoxLayout()
        frequency_input_layout = QFormLayout()
        frequency_input_layout.setLabelAlignment(Qt.AlignLeft)
        frequency_input_layout.setFormAlignment(Qt.AlignLeft)
        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(0, 1000000)
        self.frequency_input.setDecimals(3)
        self.frequency_input.setObjectName("frequency_input")
        frequency_input_layout.addRow("Frequency", self.frequency_input)
        frequency_layout.addLayout(frequency_input_layout)
        unit_combo_layout = QFormLayout()
        unit_combo_layout.setLabelAlignment(Qt.AlignLeft)
        unit_combo_layout.setFormAlignment(Qt.AlignLeft)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["kHz", "gHz", "mHz"])
        self.unit_combo.setObjectName("unit_combo")
        unit_combo_layout.addRow("Unit:", self.unit_combo)
        frequency_layout.addLayout(unit_combo_layout)
        form_layout.addRow(frequency_layout)
        self.band_combo = QComboBox()
        self.band_combo.addItems(["HF", "VHF", "UHF"])
        self.band_combo.setObjectName("band_combo")
        form_layout.addRow("Band", self.band_combo)
        self.notes_input = QTextEdit()
        self.notes_input.setObjectName("notes_input")
        form_layout.addRow("Notes / Comments", self.notes_input)
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.clicked.connect(self.clear_form_clicked)
        self.log_button = QPushButton("Log Contact")
        self.log_button.setObjectName("log_button")
        self.log_button.clicked.connect(self.log_contact_clicked)
        button_layout.addWidget(self.clear_button, stretch=3)
        button_layout.addWidget(self.log_button, stretch=7)
        tab1_layout.addLayout(form_layout)
        tab1_layout.addLayout(button_layout)
        tab1.setLayout(tab1_layout)
        tab2_layout = QVBoxLayout()
        tab2_layout.setContentsMargins(0, 0, 0, 0)
        tab2_layout.setSpacing(0)
        self.table_widget = QTableWidget()
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        tab2_layout.addWidget(self.table_widget)
        tab2.setLayout(tab2_layout)
        layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Lexend", 10)
    app.setFont(font)
    window = HamRadioLogbook()
    window.show()
    sys.exit(app.exec_())