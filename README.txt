# 🎓 Grade Tracker

A clean and simple desktop app to help you track your university modules, assessments, and calculate your average grade — all in one place.

![Screenshot](./screenshots/dashboard.png) ( TO BE ADDED ) 

## Features

- Add and manage multiple modules and assessments
- Automatically calculate:
  - Module grades
  - Average of completed modules
  - Grade needed to reach a 70% average
- Dashboard with summary table and status indicators
- Support for in-progress and completed modules
- Dark mode with custom QSS styling

## Getting Started

### Requirements

- Python 3.7+
- PyQt5

### Install dependencies

```bash
pip install PyQt5

### Project Structure
Grade Tracker/
├── main.py
├── modules/
│   ├── storage.py
│   └── tracker.py
├── view/
│   ├── home_widget.py
│   └── module_widget.py
├── themes/
│   └── dark.qss
├── modules.json        
├── README.md
└── .gitignore

