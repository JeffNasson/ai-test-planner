# Business Logic Layer for generating test cases from requirements/specs
# Requirements/Specs -> Test Cases
# Adapter around AI engine

import json
from orchestrator.pipeline import break_down_task

def generate_from_requirements(requirements: list):
    
    # Strip array list
    task = "\n".join(requirements)

    # Run AI prompt and sanitize JSON response
    results = break_down_task(task)

    # Transform back to JSON to satisfy service requirements
    data = json.loads(results)

    return data["test_cases"]