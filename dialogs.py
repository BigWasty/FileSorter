from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class GroupNameDialog(QDialog):
    
    def __init__(self, groups, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Group Names")
        self.groupNames = groups
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.inputs = {}
        for group_name, group_value in self.groupNames.items():
            label = QLabel(f"Group {group_name}")
            layout.addWidget(label)
            
            inputField = QLineEdit(group_value)
            self.inputs[group_name] = inputField
            layout.addWidget(inputField)
        
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveNames)
        layout.addWidget(saveButton)
        
        self.setLayout(layout)
        
    def get_group_name(self):
        return self.groupNames
        
    def saveNames(self):
        for group_name, inputField in self.inputs.items():
            self.groupNames[group_name] = inputField.text()
        self.accept()