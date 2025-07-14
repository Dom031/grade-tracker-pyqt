from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QDoubleSpinBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from modules.tracker import calculate_module_grade
from modules.storage import save_modules, load_modules

class ModuleWidget(QWidget):
    module_saved = pyqtSignal()  # ✅ Define the signal

    def __init__(self, module_name, tab_widget):
        super().__init__()
        self.module_name = module_name
        self.tab_widget = tab_widget
        self.assessments = []

        self.layout = QVBoxLayout()
        self.module_complete_checkbox = QCheckBox("Mark Module as Complete")

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Assessment", "Score", "Max", "Weight (%)", "Graded?"])

        self.init_ui()

    def init_ui(self):
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Assessment")
        delete_btn = QPushButton("Delete Selected Row")
        calc_btn = QPushButton("Calculate Grade")
        save_btn = QPushButton("Save Module")

        add_btn.clicked.connect(self.add_assessment)
        delete_btn.clicked.connect(self.delete_assessment)
        calc_btn.clicked.connect(self.calculate)
        save_btn.clicked.connect(self.save)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(calc_btn)
        button_layout.addWidget(save_btn)

        # Layout structure
        self.layout.addWidget(QLabel(f"Module: {self.module_name}"))
        self.layout.addWidget(self.module_complete_checkbox)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def add_assessment(self, data=None):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Name
        name_item = QTableWidgetItem(data["name"] if data else "")
        self.table.setItem(row, 0, name_item)

        # Score
        score_input = QDoubleSpinBox()
        score_input.setRange(0, 1000)
        score_input.setValue(data["score"] if data else 0)
        self.table.setCellWidget(row, 1, score_input)

        # Max mark
        max_input = QDoubleSpinBox()
        max_input.setRange(1, 1000)
        max_input.setValue(data["max"] if data else 100)
        self.table.setCellWidget(row, 2, max_input)

        # Weight
        weight_input = QDoubleSpinBox()
        weight_input.setRange(0, 100)
        weight_input.setValue(data["weight"] if data else 0)
        self.table.setCellWidget(row, 3, weight_input)

        # Graded?
        graded_checkbox = QCheckBox()
        graded_checkbox.setChecked(data["graded"] if data and "graded" in data else False)
        self.table.setCellWidget(row, 4, graded_checkbox)

    def delete_assessment(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)

    def collect_assessment_data(self):
        data = []
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            name = name_item.text() if name_item else f"Assessment {row+1}"
            score = self.table.cellWidget(row, 1).value()
            max_mark = self.table.cellWidget(row, 2).value()
            weight = self.table.cellWidget(row, 3).value()
            graded = self.table.cellWidget(row, 4).isChecked()

            data.append({
                "name": name,
                "score": score,
                "max": max_mark,
                "weight": weight,
                "graded": graded
            })
        return data

    def calculate(self):
        try:
            assessments = self.collect_assessment_data()
            result = calculate_module_grade(assessments)

            msg = QMessageBox()
            msg.setWindowTitle("Module Grade")
            msg.setText(
                f"Overall Grade: {result['grade']:.2f}%\n"
                + (f"You need {result['needed_for_70']:.2f}% on the remaining {result['remaining_weight']:.2f}% "
                   f"to reach 70%" if result['needed_for_70'] is not None else "Module fully graded.")
            )
            msg.exec_()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def save(self):
        assessments = self.collect_assessment_data()
        is_complete = self.module_complete_checkbox.isChecked()
        save_modules(self.module_name, assessments, is_complete)
        QMessageBox.information(self, "Saved", "Module data saved!")
        self.module_saved.emit()  # ✅ Emit the signal so dashboard refreshes

    def load_data(self):
        all_modules = load_modules()
        if self.module_name in all_modules:
            module_data = all_modules[self.module_name]
            self.module_complete_checkbox.setChecked(module_data.get("is_complete", False))
            for assessment in module_data.get("assessments", []):
                self.add_assessment(assessment)
