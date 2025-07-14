def calculate_module_grade(assessments):
    weighted_sum = 0
    total_weight = 0

    for a in assessments:
        percentage = (a["score"] / a["max"]) * 100
        contribution = percentage * (a["weight"] / 100)
        weighted_sum += contribution
        total_weight += a["weight"]

    result = {
        "grade": weighted_sum,
        "remaining_weight": max(0, 100 - total_weight),
        "needed_for_70": None
    }

    if total_weight < 100:
        remaining = 100 - total_weight
        result["needed_for_70"] = max(0, (70 - weighted_sum) / (remaining / 100))

    return result

def calculate_completed_modules_average(modules: dict, target: float = 70.0) -> dict:
    completed = []
    for name, module in modules.items():
        if module.get("is_complete", False):
            grade_info = calculate_module_grade(module["assessments"])
            completed.append(grade_info["grade"])

    if not completed:
        return {
            "average": 0,
            "count": 0,
            "needed": None
        }

    avg = sum(completed) / len(completed)

    return {
        "average": avg,
        "count": len(completed),
        "needed": max(0, (target * (len(completed) + 1) - sum(completed)))  # Needed avg for next module
    }
