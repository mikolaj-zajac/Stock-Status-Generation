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

        self.directory_label = QLabel("Directory: NOT SELECTED!", self)
        self.directory_label.setStyleSheet("color: red;")
        layout.addWidget(self.directory_label)

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

        self.select_directory_button = QPushButton("Select Directory", self)
        self.select_directory_button.setFixedSize(250, 50)
        self.select_directory_button.clicked.connect(self.select_directory)
        button_layout.addWidget(self.select_directory_button, 1, 0)

        self.create_folders_button = QPushButton("Create Folders", self)
        self.create_folders_button.setFixedSize(250, 50)
        self.create_folders_button.clicked.connect(self.create_folders)
        button_layout.addWidget(self.create_folders_button, 1, 1)

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
                                quantity = row.get('/sizes/size/stock@quantity', 'N/A')
                                if "Å" in name:
                                    name = name.replace("Å", "ł")
                                if "Å¼" in name:
                                    name = name.replace("Å¼", "ż")
                                if "Ć³" in name:
                                    name = name.replace("Ć³", "ó")
                                if "Ä" in name:
                                    name = name.replace("Ä", "ą")
                                if "butów" in name:
                                    print(name)
                                    continue
                                if ", Wyprzedaż" in name:
                                    name = name.split(", Wyprzedaż")[0]
                                if ", Przecena" in name:
                                    name = name.split(", Przecena")[0]
                                if "REV’IT!" in name:
                                    name = name.split("REV’IT!")[1]
                                if "Daytona" in name:
                                    name = name.split("Daytona")[1]
                                if "Falco" in name:
                                    name = name.split("Falco")[1]
                                if "Dainese" in name :
                                    name = name.split("Dainese")[1]
                                if "DAINESE" in name:
                                    name = name.split("DAINESE")[1]
                                if "ALPINESTARS" in name.upper():
                                    # jebani idioci z alpinestars
                                    delete = ["Buty motocyklowe wyścigowe",
                                              "Motocyklowe Buty wyścigowe",
                                              "Buty wyścigowe",
                                              "Motocyklowe Buty turystyczne",
                                              "Motocyklowe Buty sportowe",
                                              "Buty motocyklowe",
                                              "Buty motocyklowe",
                                              "Buty turystyczne",
                                              "Motocyklowe Buty",
                                              "Buty codzienne",
                                              "Buty sportowe",
                                              "ALPINESTARS",
                                              "Alpinestars",
                                              "wyścigowe",
                                              "sportowe"]
                                    name = self.clean_name(name, delete)

                                if "3" in status or "1" in status:
                                    status = status.split('\n')
                                    quantity = quantity.split('\n')

                                    for index, s in enumerate(status):
                                        if s == "3" or s == "1":
                                            if float(quantity[index]) > 0:
                                                status = "x"
                                                break
                                            else:
                                                status = ""
                                else:
                                    status = ""
                                output_text += f"{name}\t{status}\n"
                                extracted_data.append([name, status])

                    except Exception as e:
                        print(f"Error reading {file_path}: {e}\n")
                else:
                    print(f"{file_path} is not a CSV (.csv) file. Skipping.\n")

            if extracted_data:
                output_file = 'extracted_data.csv'
                with open(output_file, mode='w', newline='', encoding='utf-8') as output:
                    writer = csv.writer(output)
                    writer.writerow(['Product Name', 'In Stock'])
                    writer.writerows(extracted_data)

                print(f"Data has been saved to '{output_file}'.\n")

            self.text_edit.setText(output_text)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.selected_directory = directory
            self.directory_label.setText(f"Directory: {directory}")
            self.directory_label.setStyleSheet("color: black;")
        else:
            self.directory_label.setText("Directory: NOT SELECTED!")
            self.directory_label.setStyleSheet("color: red;")

    def create_folders(self):
        previous_output = self.text_edit.toPlainText()
        if previous_output:
            if not self.selected_directory:
                print("No directory selected. Please select a directory first.")
                return

            names_final = []
            for line in previous_output.split("\n"):
                parts = line.split("\t")
                if len(parts) > 1 and parts[1] == "x":
                    names_final.append(parts[0])

            parent_directory = self.selected_directory
            for name in names_final:
                directory_name = name
                if(name[0] == " "):
                    directory_name = name[1:]

                full_path = os.path.join(parent_directory, directory_name)

                try:
                    os.mkdir(full_path)
                    print(f"Directory '{directory_name}' created successfully at '{parent_directory}'.")
                except FileExistsError:
                    print(f"Directory '{directory_name}' already exists at '{parent_directory}'.")
                except PermissionError:
                    print(f"Permission denied: Unable to create '{directory_name}' at '{parent_directory}'.")
                except Exception as e:
                    print(f"An error occurred: {e}")


def main():
    app = QApplication(sys.argv)
    window = FileDialogExample()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
