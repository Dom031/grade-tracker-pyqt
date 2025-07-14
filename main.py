import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from view.module_widget import ModuleWidget
from view.home_widget import HomeWidget
from modules.storage import load_modules

class GradeTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Tracker")
        self.setMinimumSize(800, 600)

        self.tab_widget = QTabWidget()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add Home Tab
        self.home_tab = HomeWidget(self.tab_widget)
        self.tab_widget.addTab(self.home_tab, "Home")

        self.layout.addWidget(self.tab_widget)

        # Load saved modules
        self.load_saved_modules()



    def load_saved_modules(self):
        modules_data = load_modules() 
        for module_name, module_data in modules_data.items():
            assessments = module_data.get("assessments", [])
            is_complete = module_data.get("is_complete", False)

            module_tab = ModuleWidget(module_name, self.tab_widget)
            module_tab.module_complete_checkbox.setChecked(is_complete)

            for a in assessments:
                module_tab.add_assessment(a)

            # 🔁 Connect save signal to refresh dashboard
            module_tab.module_saved.connect(self.home_tab.update_dashboard)

            self.tab_widget.addTab(module_tab, module_name)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ Apply Dark Theme from QSS
    with open("theme/dark.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = GradeTrackerApp()
    window.show()
    sys.exit(app.exec_())