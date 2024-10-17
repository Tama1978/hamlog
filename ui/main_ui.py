import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from ui.station_ui import StationUI

class HamRadioLogbook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HamLog")
        self.setWindowIcon(QIcon('assets/HamLog-Logo.png'))
        self.setGeometry(0, 0, 800, 600)
        self.showMaximized()
        self.create_menu_bar()
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
        export_adif_action = QAction("Export as ADIF", self)
        export_csv_action = QAction("Export as CSV", self)
        import_adif_action = QAction("Import ADIF", self)
        erase_all_logs_action = QAction("Erase All Logs", self)
        export_adif_action.triggered.connect(self.export_adif)
        export_csv_action.triggered.connect(self.export_csv)
        import_adif_action.triggered.connect(self.import_adif)
        erase_all_logs_action.triggered.connect(self.erase_all_logs)
        logbook_menu.addAction(export_adif_action)
        logbook_menu.addAction(export_csv_action)
        logbook_menu.addAction(import_adif_action)
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
        tab3 = QWidget()
        self.tab_widget.addTab(tab1, "New Contact")
        self.tab_widget.addTab(tab2, "View Contacts")
        self.tab_widget.addTab(tab3, "Mapping")
        tab1_layout = QVBoxLayout()
        tab1_layout.setContentsMargins(20, 20, 20, 20)
        tab1_layout.setSpacing(20)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft)
        date_time_layout = QHBoxLayout()
        date_input_layout = QFormLayout()
        date_input_layout.setLabelAlignment(Qt.AlignLeft)
        date_input_layout.setFormAlignment(Qt.AlignLeft)
        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setCalendarPopup(True)
        self.date_input.setObjectName("date_input")
        self.date_input.setStyleSheet("""
            QDateEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        date_input_layout.addRow("Date", self.date_input)
        time_input_layout = QFormLayout()
        time_input_layout.setLabelAlignment(Qt.AlignLeft)
        time_input_layout.setFormAlignment(Qt.AlignLeft)
        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm:ss")
        self.time_input.setObjectName("time_input")
        self.time_input.setStyleSheet("""
            QTimeEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        time_input_layout.addRow("Time", self.time_input)
        date_time_layout.addLayout(date_input_layout)
        date_time_layout.addLayout(time_input_layout)
        form_layout.addRow("Date/Time", date_time_layout)
        station_info_layout = QHBoxLayout()
        callsign_input_layout = QFormLayout()
        callsign_input_layout.setLabelAlignment(Qt.AlignLeft)
        callsign_input_layout.setFormAlignment(Qt.AlignLeft)
        self.callsign_input = QLineEdit()
        self.callsign_input.setObjectName("callsign_input")
        self.callsign_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        callsign_input_layout.addRow("Callsign", self.callsign_input)
        name_input_layout = QFormLayout()
        name_input_layout.setLabelAlignment(Qt.AlignLeft)
        name_input_layout.setFormAlignment(Qt.AlignLeft)
        self.name_input = QLineEdit()
        self.name_input.setObjectName("name_input")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        name_input_layout.addRow("Name", self.name_input)
        type_combo_layout = QFormLayout()
        type_combo_layout.setLabelAlignment(Qt.AlignLeft)
        type_combo_layout.setFormAlignment(Qt.AlignLeft)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Base Station", "Base Station (Home)", "Base Station (Away)", "Base Station (Event)", "Base Station (Club)", "Mobile", "Mobile (Vehicle)", "Mobile (Boat)", "Mobile (Handheld)"])
        self.type_combo.setObjectName("type_combo")
        self.type_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        type_combo_layout.addRow("Station Type", self.type_combo)
        station_info_layout = QHBoxLayout()
        station_info_layout.addLayout(callsign_input_layout)
        station_info_layout.addLayout(name_input_layout)
        station_info_layout.addLayout(type_combo_layout)
        form_layout.addRow("Station Info", station_info_layout)
        frequency_layout = QHBoxLayout()
        frequency_input_layout = QFormLayout()
        frequency_input_layout.setLabelAlignment(Qt.AlignLeft)
        frequency_input_layout.setFormAlignment(Qt.AlignLeft)
        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(0, 1000000)
        self.frequency_input.setDecimals(3)
        self.frequency_input.setObjectName("frequency_input")
        self.frequency_input.setStyleSheet("""
            QDoubleSpinBox {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        frequency_input_layout.addRow("Frequency", self.frequency_input)
        unit_combo_layout = QFormLayout()
        unit_combo_layout.setLabelAlignment(Qt.AlignLeft)
        unit_combo_layout.setFormAlignment(Qt.AlignLeft)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["kHz", "gHz", "mHz"])
        self.unit_combo.setObjectName("unit_combo")
        self.unit_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        unit_combo_layout.addRow("Unit:", self.unit_combo)
        band_combo_layout = QFormLayout()
        band_combo_layout.setLabelAlignment(Qt.AlignLeft)
        band_combo_layout.setFormAlignment(Qt.AlignLeft)
        self.band_combo = QComboBox()
        self.band_combo.addItems(["HF", "VHF", "UHF"])
        self.band_combo.setObjectName("band_combo")
        self.band_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        band_combo_layout.addRow("Band", self.band_combo)
        frequency_layout.addLayout(frequency_input_layout)
        frequency_layout.addLayout(unit_combo_layout)
        frequency_layout.addLayout(band_combo_layout)
        form_layout.addRow("Frequency / Band", frequency_layout)
        contact_location_layout = QFormLayout()
        contact_location_layout.setLabelAlignment(Qt.AlignLeft)
        contact_location_layout.setFormAlignment(Qt.AlignLeft)
        contact_location_layout = QHBoxLayout()
        self.contact_location_input = QLineEdit()
        self.contact_location_input.setObjectName("contact_location_input")
        self.contact_location_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        contact_location_layout.addWidget(QLabel("Contact Location"))
        contact_location_layout.addWidget(self.contact_location_input)
        self.operator_location_input = QLineEdit()
        self.operator_location_input.setObjectName("operator_location_input")
        self.operator_location_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        contact_location_layout.addWidget(QLabel("Operator Location"))
        contact_location_layout.addWidget(self.operator_location_input)
        form_layout.addRow("Location Info", contact_location_layout)
        mode_layout = QFormLayout()
        mode_layout.setLabelAlignment(Qt.AlignLeft)
        mode_layout.setFormAlignment(Qt.AlignLeft)
        signal_report_layout = QHBoxLayout()
        self.signal_report_input = QLineEdit()
        self.signal_report_input.setObjectName("signal_report_input")
        self.signal_report_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        signal_report_layout.addWidget(QLabel("Signal Report"))
        signal_report_layout.addWidget(self.signal_report_input)
        self.qso_duration_input = QTimeEdit()
        self.qso_duration_input.setDisplayFormat("HH:mm:ss")
        self.qso_duration_input.setObjectName("qso_duration_input")
        self.qso_duration_input.setStyleSheet("""
            QTimeEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        signal_report_layout.addWidget(QLabel("QSO Duration"))
        signal_report_layout.addWidget(self.qso_duration_input)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["SSB", "FM", "Digital", "AM", "DMR", "Other"])
        self.mode_combo.setObjectName("mode_combo")
        self.mode_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        signal_report_layout.addWidget(QLabel("Mode"))
        signal_report_layout.addWidget(self.mode_combo)
        form_layout.addRow("RST, Mode, QSO", signal_report_layout)
        self.notes_input = QTextEdit()
        self.notes_input.setObjectName("notes_input")
        self.notes_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        form_layout.addRow("Notes / Comments", self.notes_input)
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: white;
                padding: 20px;
                border-radius: 10px;
            }
            
            QPushButton:Hover {
                background-color: #700000;
                border-radius: 10px;
            }
        """)
        self.clear_button.setObjectName("clear_button")
        self.clear_button.clicked.connect(self.clear_form_clicked)
        self.log_button = QPushButton("Log Contact")
        self.log_button.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: white;
                padding: 20px;
                border-radius: 10px;
            }
            
            QPushButton:Hover {
                background-color: #700000;
                border-radius: 10px;
            }
        """)
        self.log_button.setObjectName("log_button")
        self.log_button.clicked.connect(self.log_contact_clicked)
        button_layout.addWidget(self.clear_button, stretch=3)
        button_layout.addWidget(self.log_button, stretch=7)
        tab1_layout.addLayout(form_layout)
        tab1_layout.addLayout(button_layout)
        tab1.setLayout(tab1_layout)
        tab2_layout = QVBoxLayout()
        tab2_layout.setContentsMargins(20, 20, 20, 20)
        tab2_layout.setSpacing(20)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by callsign, date, or name")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #800000;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_logs)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            
            QPushButton:Hover {
                background-color: #700000;
                border-radius: 10px;
            }
        """)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        tab2_layout.addLayout(search_layout)
        self.table_widget = QTableWidget()
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        tab2_layout.addWidget(self.table_widget)
        tab2.setLayout(tab2_layout)
        layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(layout)
        mapping_layout = QVBoxLayout()
        self.map_view = QWebEngineView()
        mapping_layout.addWidget(self.map_view)
        self.generate_map_button = QPushButton("Generate Map")
        self.generate_map_button.clicked.connect(self.generate_map)
        mapping_layout.addWidget(self.generate_map_button)
        tab3.setLayout(mapping_layout)
        layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Lexend", 10)
    app.setFont(font)
    window = HamRadioLogbook()
    window.show()
    sys.exit(app.exec_())