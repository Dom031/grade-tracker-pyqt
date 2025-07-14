import json
import os

SAVE_FILE = "data/modules.json"

def load_modules():
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            raw = json.loads(content)
            formatted = {}
            for module_name, module_data in raw.items():
                if isinstance(module_data, list):
                    formatted[module_name] = {
                        "assessments": module_data,
                        "is_complete": False
                    }
                else:
                    formatted[module_name] = module_data
            return formatted
    except json.JSONDecodeError:
        print("❌ Invalid JSON format. Starting fresh.")
        return {}



def save_modules(module_name, assessments, is_complete=False):
    os.makedirs("data", exist_ok=True)

    data = load_modules()
    data[module_name] = {
        "is_complete": is_complete,
        "assessments": assessments
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
