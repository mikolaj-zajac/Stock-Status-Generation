import sys
import os
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget, \
    QHBoxLayout, QLabel, QGridLayout
from PyQt6.QtGui import QColor

class FileDialogExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_directory = None

    def initUI(self):
        self.setWindowTitle("Stock Status Generator")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        button_layout = QGridLayout()

        self.button = QPushButton("Open Files", self)
        self.button.setFixedSize(250, 50)
        self.button.clicked.connect(self.openFileDialog)
        button_layout.addWidget(self.button, 0, 0)

        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.setFixedSize(250, 50)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button, 0, 1)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def clean_name(self, name, delete):
        name_upper = name.upper()
        for item in delete:
            if item.upper() in name_upper:
                name = name.replace(item, "")
        return name.strip()
    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open Files")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            extracted_data = []
            output_text = ""

            for file_path in selected_files:
                if file_path.lower().endswith('.csv'):
                    try:
                        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                            reader = csv.DictReader(file, delimiter=',', quotechar='"')

                            for row in reader:
                                name = row.get('/description/name[pol]', 'N/A')
                                status = row.get('/sizes/size/stock@stock_id', 'N/A')
                                sizes = row.get('/sizes/size/stock@size_id', 'N/A')
                                quantity = row.get('/sizes/size/stock@quantity', 'N/A')
                                size_status = ""
                                quantity_status = ""
                                if "Å" in name:
                                    name = name.replace("Å", "ł")
                                if "Å¼" in name:
                                    name = name.replace("Å¼", "ż")
                                if "Ć³" in name:
                                    name = name.replace("Ć³", "ó")
                                if "Ä" in name:
                                    name = name.replace("Ä", "ą")
                                if "Zestaw" in name:
                                    print(name)
                                    continue
                                if "Kask" in name:
                                    name = ' '.join(name.split("Kask", 1)[1].split()[2:])



                                if "3" in status or "1" in status:
                                    status = status.split('\n')
                                    sizes = sizes.split('\n')
                                    quantity = quantity.split('\n')

                                    for index, s in enumerate(status):
                                        if s == "3" or s == "1":
                                            size_status = sizes[index]
                                            quantity_status = quantity[index]

                                            size_mapping = {
                                                "509": "509???",
                                                "510": "XXS",
                                                "511": "XS",
                                                "512": "S",
                                                "513": "M",
                                                "514": "L",
                                                "515": "XL",
                                                "516": "XXL",
                                                "517": "517??",
                                                "": ""
                                            }
                                            if quantity_status == "0.000":
                                                quantity_status = "0"

                                            size_status = size_mapping.get(size_status,
                                                                           "Unknown")

                                            output_text += f"{name}\t{size_status}\t{quantity_status}\n"
                                            extracted_data.append([name, size_status, quantity_status])

                                else:
                                    status = ""






                    except Exception as e:
                        print(f"Error reading {file_path}: {e}\n")
                else:
                    print(f"{file_path} is not a CSV (.csv) file. Skipping.\n")

            if extracted_data:
                output_file = 'extracted_data.csv'
                with open(output_file, mode='w', newline='', encoding='utf-8') as output:
                    writer = csv.writer(output)
                    writer.writerow(['Product Name', 'Size', 'Quantity'])
                    writer.writerows(extracted_data)

                print(f"Data has been saved to '{output_file}'.\n")

            self.text_edit.setText(output_text)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())


def main():
    app = QApplication(sys.argv)
    window = FileDialogExample()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
