from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QMenu, QAction, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import *
from fpdf import FPDF
from main_ui import HamRadioLogbook
from station_ui import StationUI
import sys
import csv
import os

class MainWindow(HamRadioLogbook):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.log_button.clicked.connect(self.log_contact_clicked)
        self.clear_button.clicked.connect(self.clear_form_clicked)
        self.create_menu_bar_connections()
        self.create_logbook_file()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Date"))
        self.table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Time"))
        self.table_widget.setHorizontalHeaderItem(2, QTableWidgetItem("Callsign"))
        self.table_widget.setHorizontalHeaderItem(3, QTableWidgetItem("Name"))
        self.table_widget.setHorizontalHeaderItem(4, QTableWidgetItem("Frequency"))
        self.table_widget.setHorizontalHeaderItem(5, QTableWidgetItem("Unit"))
        self.table_widget.setHorizontalHeaderItem(6, QTableWidgetItem("Band"))
        self.table_widget.setHorizontalHeaderItem(7, QTableWidgetItem("Notes"))
        self.load_logbook()

    def erase_all_logs(self):
        if os.path.exists('logbook.csv'):
            try:
                os.remove('logbook.csv')
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

    def create_menu_bar_connections(self):
        menu_bar = self.menuBar()
        logbook_menu = menu_bar.findChild(QMenu, "Logbook")
        export_logs_action = self.find_action(logbook_menu, "Export Logs")
        if export_logs_action:
            export_logs_action.triggered.connect(self.export_logs)

        erase_all_logs_action = self.find_action(logbook_menu, "Erase All Logs")
        if erase_all_logs_action:
            erase_all_logs_action.triggered.connect(self.erase_all_logs)

        my_station_action = self.find_action(menu_bar, "My Station")
        if my_station_action:
            my_station_action.triggered.connect(self.open_station_ui)

    def open_station_ui(self):
        # Create an instance of the StationUI class and show it
        self.station_ui = StationUI()
        self.station_ui.show()

    def export_logs(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Logs", "", "PDF Files (*.pdf)")
        if file_name:
            try:
                self.save_pdf(file_name)
            except Exception as e:
                print(f"Error exporting logs: {e}")

    def save_pdf(self, file_name):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=15)
            pdf.cell(200, 10, txt="Ham Radio Logbook", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=10)
            for row in range(self.table_widget.rowCount()):
                for column in range(self.table_widget.columnCount()):
                    pdf.cell(40, 10, txt=self.table_widget.item(row, column).text(), border=1, align='C')
                pdf.ln(10)
            pdf.output(file_name)
        except Exception as e:
            print(f"Error saving PDF: {e}")

    def create_logbook_file(self):
        if not os.path.exists('logbook.csv'):
            try:
                with open('logbook.csv', 'w', newline='') as csvfile:
                    fieldnames = ['date', 'time', 'callsign', 'name', 'frequency', 'unit', 'band', 'notes']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
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
        unit = self.unit_combo.currentText()
        band = self.band_combo.currentText()
        notes = self.notes_input.toPlainText()

        if not callsign or not name:
            QMessageBox.critical(self, "Error", "Please enter all the required information.")
            self.logging_in_progress = False
            return

        try:
            with open('logbook.csv', 'a', newline='') as csvfile:
                fieldnames = ['date', 'time', 'callsign', 'name', 'frequency', 'unit', 'band', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writerow({
                    'date': date,
                    'time': time,
                    'callsign': callsign,
                    'name': name,
                    'frequency': frequency,
                    'unit': unit,
                    'band': band,
                    'notes': notes
                })
        except Exception as e:
            print(f"Error writing to logbook file: {e}")

        # Reload the logbook from the CSV file
        self.load_logbook()

        QMessageBox.information(self, "Contact Logged", "The contact has been logged successfully.")
        QTimer.singleShot(100, self.clear_form_clicked_and_reset_flag)

    def clear_form_clicked_and_reset_flag(self):
        self.clear_form_clicked()
        self.logging_in_progress = False

    def load_logbook(self):
        try:
            with open('logbook.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                self.table_widget.setRowCount(0)

                for row, data in enumerate(reader):
                    if row == 0:
                        continue
                    self.table_widget.insertRow(row - 1)
                    for column, item in enumerate(data):
                        self.table_widget.setItem(row - 1, column, QTableWidgetItem(item))
        except Exception as e:
            print(f"Error loading logbook file: {e}")
            QMessageBox.critical(self, "Error", "Failed to load logbook file.")

    def clear_form_clicked(self):
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())
        self.callsign_input.clear()
        self.name_input.clear()
        self.frequency_input.setValue(0)
        self.unit_combo.setCurrentIndex(0)
        self.band_combo.setCurrentIndex(0)
        self.notes_input.clear()

    def exit_app(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())