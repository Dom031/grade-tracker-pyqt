from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
)
from view.module_widget import ModuleWidget
from modules.storage import load_modules
from modules.tracker import calculate_completed_modules_average, calculate_module_grade

class HomeWidget(QWidget):
    def __init__(self, tab_widget):
        super().__init__()
        self.tab_widget = tab_widget

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("🎓 Welcome to your Grade Tracker Dashboard")
        self.layout.addWidget(self.title_label)

        self.module_name_input = QLineEdit()
        self.module_name_input.setPlaceholderText("Enter new module name")
        self.add_button = QPushButton("Add Module")
        self.add_button.clicked.connect(self.add_module)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.module_name_input)
        input_layout.addWidget(self.add_button)
        self.layout.addLayout(input_layout)

        self.summary_table = QTableWidget(0, 3)
        self.summary_table.setHorizontalHeaderLabels(["Module Name", "Status", "Overall (%)"])
        self.layout.addWidget(self.summary_table)

        self.average_label = QLabel("Calculating overall average...")
        self.layout.addWidget(self.average_label)

        self.update_dashboard()

    def add_module(self):
        name = self.module_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid Name", "Module name cannot be empty.")
            return

        # Check for duplicates
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i).lower() == name.lower():
                QMessageBox.warning(self, "Duplicate Module", f"A module named '{name}' already exists.")
                return

        module_tab = ModuleWidget(name, self.tab_widget)
        self.tab_widget.addTab(module_tab, name)
        self.tab_widget.setCurrentWidget(module_tab)
        self.module_name_input.clear()
        self.update_dashboard()

    def update_dashboard(self):
        self.summary_table.setRowCount(0)
        modules = load_modules()
        avg_data = calculate_completed_modules_average(modules)

        for name, module in modules.items():
            row_pos = self.summary_table.rowCount()
            self.summary_table.insertRow(row_pos)
            self.summary_table.setItem(row_pos, 0, QTableWidgetItem(name))

            grade_info = calculate_module_grade(module.get("assessments", []))
            overall = f"{grade_info['grade']:.2f}"

            if module.get("is_complete"):
                status = "✅ Module Complete"
            else:
                status = f"⏳ In Progress – So far: {overall}%"
                overall = overall if grade_info['grade'] > 0 else "-"

            self.summary_table.setItem(row_pos, 1, QTableWidgetItem(status))
            self.summary_table.setItem(row_pos, 2, QTableWidgetItem(overall))

        # Update average label
        if avg_data["count"] > 0:
            msg = f"Average of {avg_data['count']} completed module(s): {avg_data['average']:.2f}%"
            if avg_data['average'] >= 70:
                msg += "\n🎉 You're on track to hit your 70% goal!"
            else:
                msg += f"\n⚠️ You need to average {avg_data['needed']:.2f}% in your next module to hit 70%."
        else:
            msg = "No completed modules yet. Start by completing one to track your progress."

        self.average_label.setText(msg)


        if avg_data["count"] > 0:
            msg = f"Average of {avg_data['count']} completed module(s): {avg_data['average']:.2f}%"
            if avg_data['average'] >= 70:
                msg += " \n🎉 You're on track to hit your 70% goal!"
            else:
                msg += f" \n⚠️ You need to average {avg_data['needed']:.2f}% in your next module to hit 70%."
        else:
            msg = "No completed modules yet. Start by completing one to track your progress."

        self.average_label.setText(msg)