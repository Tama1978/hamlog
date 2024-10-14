from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.main_ui import HamRadioLogbook
from ui.station_ui import StationUI
import adif_io as adif
import sys
import csv
import os

class MainWindow(HamRadioLogbook):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.log_button.clicked.connect(self.log_contact_clicked)
        self.clear_button.clicked.connect(self.clear_form_clicked)
        self.create_logbook_file()
        self.table_widget.setColumnCount(13)
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Date"))
        self.table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Time"))
        self.table_widget.setHorizontalHeaderItem(2, QTableWidgetItem("Callsign"))
        self.table_widget.setHorizontalHeaderItem(3, QTableWidgetItem("Name"))
        self.table_widget.setHorizontalHeaderItem(4, QTableWidgetItem("Frequency"))
        self.table_widget.setHorizontalHeaderItem(5, QTableWidgetItem("Band"))
        self.table_widget.setHorizontalHeaderItem(6, QTableWidgetItem("Type"))
        self.table_widget.setHorizontalHeaderItem(7, QTableWidgetItem("Contact Location"))
        self.table_widget.setHorizontalHeaderItem(8, QTableWidgetItem("Operator Location"))
        self.table_widget.setHorizontalHeaderItem(9, QTableWidgetItem("Mode"))
        self.table_widget.setHorizontalHeaderItem(10, QTableWidgetItem("Signal Report"))
        self.table_widget.setHorizontalHeaderItem(11, QTableWidgetItem("QSO Duration"))
        self.table_widget.setHorizontalHeaderItem(12, QTableWidgetItem("Notes"))
        self.load_logbook()

    def create_menu_bar_connections(self):
        menu_bar = self.menuBar()
        logbook_menu = menu_bar.addMenu("Logbook")
        export_adif_action = self.find_action(logbook_menu, "Export as ADIF")
        if export_adif_action:
            export_adif_action.triggered.connect(self.export_adif)
        else:
            print("Error: Export as ADIF action not found")
        export_csv_action = self.find_action(logbook_menu, "Export as CSV")
        if export_csv_action:
            export_csv_action.triggered.connect(self.export_csv)
        else:
            print("Error: Export as CSV action not found")
        import_adif_action = self.find_action(logbook_menu, "Import ADIF")
        if import_adif_action:
            import_adif_action.triggered.connect(self.import_adif)
        else:
            print("Error: Import ADIF action not found")
        erase_all_logs_action = self.find_action(logbook_menu, "Erase All Logs")
        if erase_all_logs_action:
            erase_all_logs_action.triggered.connect(self.erase_all_logs)
        else:
            print("Error: Erase All Logs action not found")
            
    def import_adif(self):
        if hasattr(self, 'importing_logs') and self.importing_logs:
            return
        self.importing_logs = True
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Logs", "", "ADIF Files (*.adi)")
        if file_name:
            try:
                self.load_adif(file_name)
            except Exception as e:
                print(f"Error importing logs: {e}")
        self.importing_logs = False

    def load_adif(self, file_name):
        try:
            with open(file_name, 'r') as adif_file:
                adif_data = adif_file.readlines()
                for line in adif_data:
                    if line.startswith('<CALL:'):
                        callsign = line.split(':')[1].strip('>\n')
                    elif line.startswith('<QSO_DATE:'):
                        date = line.split(':')[2].strip('>\n')
                    elif line.startswith('<TIME_ON:'):
                        time = line.split(':')[2].strip('>\n')
                    elif line.startswith('<FREQ:'):
                        frequency = line.split(':')[1].strip('>\n')
                    elif line.startswith('<BAND:'):
                        band = line.split(':')[1].strip('>\n')
                    elif line.startswith('<MODE:'):
                        mode = line.split(':')[1].strip('>\n')
                    elif line.startswith('<NAME:'):
                        name = line.split(':')[1].strip('>\n')
                    elif line.startswith('<QTH:'):
                        contact_location = line.split(':')[1].strip('>\n')
                    elif line.startswith('<OPERATOR:'):
                        operator_location = line.split(':')[1].strip('>\n')
                    elif line.startswith('<SIG_RPT:'):
                        signal_report = line.split(':')[1].strip('>\n')
                    elif line.startswith('<QSO_DT:'):
                        qso_duration = line.split(':')[2].strip('>\n')
                    elif line.startswith('<NOTES:'):
                        notes = line.split(':')[1].strip('>\n')
                    elif line.startswith('<EOR>'):
                        self.table_widget.insertRow(self.table_widget.rowCount())
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, QTableWidgetItem(date))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 1, QTableWidgetItem(time))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 2, QTableWidgetItem(callsign))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 3, QTableWidgetItem(name))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 4, QTableWidgetItem(frequency))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 5, QTableWidgetItem(band))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 6, QTableWidgetItem(''))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 7, QTableWidgetItem(contact_location))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 8, QTableWidgetItem(operator_location))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 9, QTableWidgetItem(mode))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 10, QTableWidgetItem(signal_report))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 11, QTableWidgetItem(qso_duration))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 12, QTableWidgetItem(notes))
        except Exception as e:
            print(f"Error loading ADIF file: {e}")
            QMessageBox.critical(self, "Error", "Failed to load ADIF file.")

    def export_adif(self):
        if hasattr(self, 'exporting_logs') and self.exporting_logs:
            return
        self.exporting_logs = True
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Logs", "", "ADIF Files (*.adi)")
        if file_name:
            try:
                self.save_adif(file_name)
            except Exception as e:
                print(f"Error exporting logs: {e}")
        self.exporting_logs = False

    def save_adif(self, file_name):
        try:
            with open(file_name, 'w', newline='') as adif_file:
                adif_file.write('<ADIF_VER:5.0.0>\n')
                for row in range(self.table_widget.rowCount()):
                    adif_file.write(f'<QSO_DATE:8:{self.table_widget.item(row, 0).text().replace("-", "")}\n')
                    adif_file.write(f'<TIME_ON:6:{self.table_widget.item(row, 1).text().replace(":", "")}\n')
                    adif_file.write(f'<CALL:{self.table_widget.item(row, 2).text()}\n')
                    adif_file.write(f'<NAME:{self.table_widget.item(row, 3).text()}\n')
                    adif_file.write(f'<FREQ:9>{self.table_widget.item(row, 4).text()} {self.table_widget.item(row, 5).text()}\n')
                    adif_file.write(f'<BAND:{self.table_widget.item(row, 6).text()}\n')
                    adif_file.write(f'<MODE:{self.table_widget.item(row, 10).text()}\n')
                    adif_file.write(f'<QTH:{self.table_widget.item(row, 8).text()}\n')
                    adif_file.write(f'<OPERATOR:{self.table_widget.item(row, 9).text()}\n')
                    adif_file.write(f'<SIG_RPT:{self.table_widget.item(row, 11).text()}\n')
                    adif_file.write(f'<QSO_DT:6:{self.table_widget.item(row, 12).text().replace(":", "")}\n')
                    adif_file.write(f'<NOTES:{self.table_widget.item(row, 13).text()}\n')
                    adif_file.write('<EOR>\n')
        except Exception as e:
            print(f"Error saving ADIF: {e}")

    def export_csv(self):
        if hasattr(self, 'exporting_logs') and self.exporting_logs:
            return
        self.exporting_logs = True
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Logs", "", "CSV Files (*.csv)")
        if file_name:
            try:
                self.save_csv(file_name)
            except Exception as e:
                print(f"Error exporting logs: {e}")
        self.exporting_logs = False

    def save_csv(self, file_name):
        try:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Date", "Time", "Callsign", "Name", "Frequency", "Band", "Type", 'contact_location', 'operator_location', 'mode', 'signal_report', 'qso_duration', "Notes"])
                for row in range(self.table_widget.rowCount()):
                    data = [self.table_widget.item(row, column).text() for column in range(self.table_widget.columnCount())]
                    writer.writerow(data)
        except Exception as e:
            print(f"Error saving CSV: {e}")

    def erase_all_logs(self):
        if os.path.exists('logbook.adi'):
            try:
                os.remove('logbook.adi')
                self.table_widget.setRowCount(0)
                QMessageBox.information(self, "Logs Erased", "All logs have been erased successfully.")
            except Exception as e:
                print(f"Error erasing logs: {e}")
                QMessageBox.critical(self, "Error", "Failed to erase logs.")
        else:
            QMessageBox.information(self, "No Logs", "There are no logs to erase.")

    def find_action(self, parent, name):
        for action in parent.actions():
            if action.objectName() == name:
                return action
        return None

    def create_logbook_file(self):
        if not os.path.exists('logbook.adi'):
            try:
                with open('logbook.adi', 'w', newline='') as adif_file:
                    adif_file.write('<ADIF_VER:5.0.0>\n')
                    adif_file.write('<EOH>\n')
            except Exception as e:
                print(f"Error creating logbook file: {e}")

    def log_contact_clicked(self):
        if hasattr(self, 'logging_in_progress') and self.logging_in_progress:
            return
        self.logging_in_progress = True
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm:ss")
        callsign = self.callsign_input.text()
        name = self.name_input.text()
        frequency = self.frequency_input.value()
        type = self.type_combo.currentText()
        band = self.band_combo.currentText()
        contact_location = self.contact_location_input.text()
        operator_location = self.operator_location_input.text()
        mode = self.mode_combo.currentText()
        signal_report = self.signal_report_input.text()
        qso_duration = self.qso_duration_input.time().toString("HH:mm:ss")
        notes = self.notes_input.toPlainText()
        if not callsign or not name:
            QMessageBox.critical(self, "Error", "Please enter all the required information.")
            self.logging_in_progress = False
            return
        try:
            with open('logbook.adi', 'a', newline='') as adif_file:
                adif_file.write(f'<CALL:{self.callsign_input.text()}\n')
                adif_file.write(f'<QSO_DATE:8:{self.date_input.date().toString("yyyyMMdd")}\n')
                adif_file.write(f'<TIME_ON:6:{self.time_input.time().toString("HHmmss")}\n')
                adif_file.write(f'<FREQ:9>{self.frequency_input.value()} {self.unit_combo.currentText()}\n')
                adif_file.write(f'<APP_DEFINED:TYPE:{type}\n')
                adif_file.write(f'<BAND:{self.band_combo.currentText()}\n')
                adif_file.write(f'<MODE:{self.mode_combo.currentText()}\n')
                adif_file.write(f'<NAME:{self.name_input.text()}\n')
                adif_file.write(f'<QTH:{self.contact_location_input.text()}\n')
                adif_file.write(f'<OPERATOR:{self.operator_location_input.text()}\n')
                adif_file.write(f'<SIG_RPT:{self.signal_report_input.text()}\n')
                adif_file.write(f'<QSO_DT:6:{self.qso_duration_input.time().toString("HHmmss")}\n')
                adif_file.write(f'<NOTES:{self.notes_input.toPlainText()}\n')
                adif_file.write('<EOR>\n')
        except Exception as e:
            print(f"Error writing to logbook file: {e}")
        self.load_logbook()
        QMessageBox.information(self, "Contact Logged", "The contact has been logged successfully.")
        QTimer.singleShot(100, self.clear_form_clicked_and_reset_flag)

    def clear_form_clicked_and_reset_flag(self):
        self.clear_form_clicked()
        self.logging_in_progress = False

    def load_logbook(self):
        try:
            with open('logbook.adi', 'r') as adif_file:
                adif_data = adif_file.readlines()
                self.table_widget.setRowCount(0)
                qso = {}
                for line in adif_data:
                    if line.startswith('<CALL:'):
                        qso['callsign'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<QSO_DATE:'):
                        qso['date'] = line.split(':')[2].strip('>\n')
                    elif line.startswith('<TIME_ON:'):
                        qso['time'] = line.split(':')[2].strip('>\n')
                    elif line.startswith('<FREQ:'):
                        qso['frequency'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<BAND:'):
                        qso['band'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<MODE:'):
                        qso['mode'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<NAME:'):
                        qso['name'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<QTH:'):
                        qso['contact_location'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<OPERATOR:'):
                        qso['operator_location'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<SIG_RPT:'):
                        qso['signal_report'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<QSO_DT:'):
                        qso['qso_duration'] = line.split(':')[2].strip('>\n')
                    elif line.startswith('<NOTES:'):
                        qso['notes'] = line.split(':')[1].strip('>\n')
                    elif line.startswith('<APP_DEFINED:TYPE:'):
                        qso['type'] = line.split(':')[2].strip('>\n')
                    elif line.startswith('<EOR>'):
                        self.table_widget.insertRow(self.table_widget.rowCount())
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, QTableWidgetItem(qso['date']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 1, QTableWidgetItem(qso['time']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 2, QTableWidgetItem(qso['callsign']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 3, QTableWidgetItem(qso['name']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 4, QTableWidgetItem(qso['frequency']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 5, QTableWidgetItem(qso['band']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 6, QTableWidgetItem(qso['type']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 7, QTableWidgetItem(qso['contact_location']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 8, QTableWidgetItem(qso['operator_location']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 9, QTableWidgetItem(qso['mode']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 10, QTableWidgetItem(qso['signal_report']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 11, QTableWidgetItem(qso['qso_duration']))
                        self.table_widget.setItem(self.table_widget.rowCount() - 1, 12, QTableWidgetItem(qso['notes']))
                        qso = {}
        except Exception as e:
            print(f"Error loading logbook file: {e}")
            QMessageBox.critical(self, "Error", "Failed to load logbook file.")

    def clear_form_clicked(self):
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())
        self.callsign_input.clear()
        self.name_input.clear()
        self.frequency_input.setValue(0)
        self.band_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)
        self.contact_location_input.clear()
        self.operator_location_input.clear()
        self.mode_combo.setCurrentIndex(0)
        self.signal_report_input.clear()
        self.qso_duration_input.setTime(QTime(0, 0, 0))
        self.notes_input.clear()

    def search_logs(self):
        search_term = self.search_input.text().lower()
        self.table_widget.setRowCount(0)
        try:
            with open('logbook.adi', 'r') as adif_file:
                adif_data = adif_file.readlines()
                qso = {}
                for line in adif_data:
                    if line.startswith('<EOR>'):
                        if qso:
                            if not search_term or any(search_term in item.lower() for item in qso.values()):
                                self.table_widget.insertRow(self.table_widget.rowCount())
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, QTableWidgetItem(qso['date']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 1, QTableWidgetItem(qso['time']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 2, QTableWidgetItem(qso['callsign']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 3, QTableWidgetItem(qso['name']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 4, QTableWidgetItem(qso['frequency']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 6, QTableWidgetItem(qso['band']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 7, QTableWidgetItem(''))  # type
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 8, QTableWidgetItem(qso['contact_location']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 9, QTableWidgetItem(qso['operator_location']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 10, QTableWidgetItem(qso['mode']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 11, QTableWidgetItem(qso['signal_report']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 12, QTableWidgetItem(qso['qso_duration']))
                                self.table_widget.setItem(self.table_widget.rowCount() - 1, 13, QTableWidgetItem(qso['notes']))
                            qso = {}
                    else:
                        if line.startswith('<CALL:'):
                            qso['callsign'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<QSO_DATE:'):
                            qso['date'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<TIME_ON:'):
                            qso['time'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<FREQ:'):
                            qso['frequency'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<BAND:'):
                            qso['band'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<MODE:'):
                            qso['mode'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<NAME:'):
                            qso['name'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<QTH:'):
                            qso['contact_location'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<OPERATOR:'):
                            qso['operator_location'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<SIG_RPT:'):
                            qso['signal_report'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<QSO_DT:'):
                            qso['qso_duration'] = line.split(':')[1].strip('>\n')
                        elif line.startswith('<NOTES:'):
                            qso['notes'] = line.split(':')[1].strip('>\n')
        except Exception as e:
            print(f"Error searching logs: {e}")
            QMessageBox.critical(self, "Error", "Failed to search logs.")

    def open_station_ui(self):
        self.station_ui = StationUI()
        self.station_ui.show()

    def exit_app(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())