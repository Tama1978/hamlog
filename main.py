# main.py
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from ui_main import Ui_MainWindow
import sys
import csv

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setMinimumSize(850, 600)
        self.log_contact.clicked.connect(self.log_contact_clicked)
        self.clear_form.clicked.connect(self.clear_form_clicked)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionExport_as_CSV.triggered.connect(self.export_as_csv)
        self.actionErase_All_Logs.triggered.connect(self.erase_all_logs)
        self.load_logbook()

    def log_contact_clicked(self):
        date_time = self.dateTimeEdit.dateTime().toString()
        callsign = self.callsignEdit.text()
        name = self.nameEdit.text()
        location = self.locationEdit.text()
        station_type = self.stationTypeCombo.currentText()
        signal_report = self.signalReportEdit.text()
        comments = self.commentsEdit.toPlainText()
        frequency = self.frequencyEdit.value()
        unit = self.unitCombo.currentText()
        band = self.bandCombo.currentText()

        with open('logbook.csv', 'a', newline='') as csvfile:
            fieldnames = ['date_time', 'callsign', 'name', 'location', 'station_type', 'signal_report', 'comments', 'frequency', 'unit', 'band']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'date_time': date_time,
                'callsign': callsign,
                'name': name,
                'location': location,
                'station_type': station_type,
                'signal_report': signal_report,
                'comments': comments,
                'frequency': frequency,
                'unit': unit,
                'band': band
            })

        QMessageBox.information(self, "Contact Logged", "The contact has been logged successfully.")

    def clear_form_clicked(self):
        self.dateTimeEdit.setDateTime(self.dateTimeEdit.minimumDateTime())
        self.callsignEdit.clear()
        self.nameEdit.clear()
        self.locationEdit.clear()
        self.stationTypeCombo.setCurrentIndex(0)
        self.signalReportEdit.clear()
        self.commentsEdit.clear()
        self.frequencyEdit.setValue(0)
        self.unitCombo.setCurrentIndex(0)
        self.bandCombo.setCurrentIndex(0)

    def exit_app(self):
        QApplication.quit()

    def export_as_csv(self):
        with open('logbook.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            logbook = list(reader)

        with open('exported_logbook.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(logbook)

        QMessageBox.information(self, "Logbook Exported", "The logbook has been exported successfully.")

    def erase_all_logs(self):
        with open('logbook.csv', 'w') as csvfile:
            pass

        QMessageBox.information(self, "Logs Erased", "All logs have been erased successfully.")

    def load_logbook(self):
        self.model = QStandardItemModel(self.contact_table)
        self.model.setHorizontalHeaderItem(0, QStandardItem("Date/Time"))
        self.model.setHorizontalHeaderItem(1, QStandardItem("Callsign"))
        self.model.setHorizontalHeaderItem(2, QStandardItem("Name"))
        self.model.setHorizontalHeaderItem(3, QStandardItem("Location"))
        self.model.setHorizontalHeaderItem(4, QStandardItem("Station Type"))
        self.model.setHorizontalHeaderItem(5, QStandardItem("Signal Report"))
        self.model.setHorizontalHeaderItem(6, QStandardItem("Comments"))
        self.model.setHorizontalHeaderItem(7, QStandardItem("Frequency"))
        self.model.setHorizontalHeaderItem(8, QStandardItem("Unit"))
        self.model.setHorizontalHeaderItem(9, QStandardItem("Band"))

        with open('logbook.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row, data in enumerate(reader):
                for column, item in enumerate(data):
                    self.model.setItem(row, column, QStandardItem(item))

        self.contact_table.setModel(self.model)
        self.contact_table.horizontalHeader().setStretchLastSection(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())