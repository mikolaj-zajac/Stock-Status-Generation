import os

parent_directory = "/path/to/your/folder"
names = input()
names_final = []
for line in names.split("\n"):
    if line.split("\t")[1] == "x":
        names_final.append(line[0])

print(names_final)
for name in names_final:

    directory_name = "GFG"

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

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog, QWidget
from PyQt6.QtCore import Qt

class StockStatusGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Generator")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Paste your input text here")
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()


        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def openFileDialog(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file:
            with open(file, 'r') as f:
                text = f.read()
                self.text_edit.setText(text)
            self.process_text(text)

    def process_text(self, input_text):
        lines = input_text.split("\n")
        items_with_x = []

        for line in lines:
            if '\tx' in line:
                item_name = line.split('\t')[0]
                items_with_x.append(item_name)

        self.result_text.setText("\n".join(items_with_x))

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())

app = QApplication(sys.argv)

window = StockStatusGenerator()
window.show()

sys.exit(app.exec())