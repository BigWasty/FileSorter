import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QListWidget, QCheckBox, QFileDialog, QHBoxLayout, QDialog, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from dialogs import GroupNameDialog


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.chosenFolder = ""
        self.chosenFiles = []
        self.group1 = []
        self.group2 = []
        self.group3 = []
        self.group4 = []
        self.group5 = []
        self.file_paths = {}
        self.initUI()

    def recolor_and_add_to_list(self, color, groupList):
        selected_items = self.listbox.selectedItems()
        groupList.clear()
        for item in selected_items:
            groupList.append(item.text())
            item.setBackground(QColor(color))

    def choose_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Choose Files", "", "All Files (*);;Python Files (*.py)", options=options)
        if files:
            for file in files:
                self.chosenFiles.append(file)
                file_name = os.path.basename(file)
                self.file_paths[file_name] = file
                self.listbox.addItem(file_name)

    group_names = {
        "Group1": "Group 1",
        "Group2": "Group 2",
        "Group3": "Group 3",
        "Group4": "Group 4",
        "Group5": "Group 5",
    }
    
    def open_group_name_dialog(self):
        
        dialog = GroupNameDialog(self.group_names)
        if dialog.exec_() == QDialog.Accepted:  # Zkontroluje, zda uživatel klikl na "Save"
            group_name = dialog.get_group_name()  # Získá text z inputu
            print(f"Group name set to: {group_name}")
            # Uložte nebo použijte group_name dle potřeby
            self.group_names = group_name
        else:
            print("Dialog was canceled")

    def choose_folder(self):
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Choose Folder", "", options=options)
        if folder:
            self.chosenFolder = folder
            print(f"Chosen folder: {folder}")

    def group(self, button):
        buttonGroup = button.text().split(" ")[1]
        match buttonGroup:
            case "1":
                self.recolor_and_add_to_list(Qt.yellow, self.group1)
            case "2":
                self.recolor_and_add_to_list(Qt.red, self.group2)
            case "3":
                self.recolor_and_add_to_list(Qt.green, self.group3)
            case "4":
                self.recolor_and_add_to_list(Qt.cyan, self.group4)
            case "5":
                self.recolor_and_add_to_list(Qt.magenta, self.group5)

        self.listbox.clearSelection()

    def connect_buttons(self):
        for i in range(self.button_row_layout.count()):
            button = self.button_row_layout.itemAt(i).widget()
            if isinstance(button, QPushButton):
                button.clicked.connect(lambda checked, btn=button: self.group(btn))

    def execute(self):
        if not self.chosenFolder:
            print("No folder chosen for saving files.")
            return

        groups = {
            self.group_names["Group1"]: self.group1,
            self.group_names["Group2"]: self.group2,
            self.group_names["Group3"]: self.group3,
            self.group_names["Group4"]: self.group4,
            self.group_names["Group5"]: self.group5,
        }

        for group_name, group_files in groups.items():
            if not group_files:
                continue
            
            if self.checkbox.isChecked():
                group_folder = os.path.join(self.chosenFolder, group_name)
                os.makedirs(group_folder, exist_ok=True)  # Vytvoří podsložku, pokud neexistuje

            counter = 1
            
            for file_name in group_files:
                source_path = self.file_paths.get(file_name)
                if source_path:
                    file_extension = os.path.splitext(file_name)[1]
                    destination_path = os.path.join(group_folder, f"{group_name}_{counter}{file_extension}") if self.checkbox.isChecked() else os.path.join(self.chosenFolder, f"{group_name}_{counter}{file_extension}")
                    shutil.copy(source_path, destination_path)
                    print(f"Copied {file_name} to {destination_path}")
                    counter += 1

    def initUI(self):
        vbox = QVBoxLayout()
        self.button_row_layout = QHBoxLayout()

        # Vytvoření tlačítek skupin
        for i in range(5):
            button = QPushButton(f"Group {i+1}")
            self.button_row_layout.addWidget(button)

        self.connect_buttons()
        vbox.addLayout(self.button_row_layout)

        # ListBox pro soubory
        self.listbox = QListWidget()
        self.listbox.setSelectionMode(QAbstractItemView.MultiSelection)
        vbox.addWidget(self.listbox)

        # Tlačítko pro výběr souborů
        self.button1 = QPushButton('Choose Files')
        self.button1.clicked.connect(self.choose_files)
        vbox.addWidget(self.button1)

        # CheckBox
        self.checkbox = QCheckBox('Sort into folders')
        vbox.addWidget(self.checkbox)
        
        # Tlačítko přejmenování skupin
        self.button = QPushButton('Rename Groups')
        self.button.clicked.connect(self.open_group_name_dialog)
        vbox.addWidget(self.button)
        
        # Tlačítko pro výběr složky
        self.button2 = QPushButton('Choose Folder')
        self.button2.clicked.connect(self.choose_folder)
        vbox.addWidget(self.button2)

        # Tlačítko Execute
        self.button3 = QPushButton('Execute')
        self.button3.clicked.connect(self.execute)
        vbox.addWidget(self.button3)

        self.setLayout(vbox)
        self.setWindowTitle('PyQt5 Layout')
        self.resize(800, 600)
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    ex = MyApp()
    app.exec_()
