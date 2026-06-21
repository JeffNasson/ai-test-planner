# Business Logic Layer for generating test cases from requirements/specs
# Requirements/Specs -> Test Cases
# Adapter around AI engine

import json
from orchestrator.pipeline import break_down_task
from framework.generation.requirement_analyzer import analyze_requirement

# Helper function for prompt logic
def build_requirement_prompt(requirement: str, strategy: dict) -> str:

    focus_areas = "\n".join(
        f"- {area}" for area in strategy["focus_areas"]
    )

    return f"""
Recommended Coverage: 
{focus_areas}

The generated positive, negative, and edge cases should collectively cover these focus areas whenever possible.
    
Requirement:
{requirement}

Domain:
{strategy["domain"]}

Focus Areas:
{focus_areas}
"""


# Generate test cases using AI Prompt
def generate_from_requirements(requirements: list, feedback: str = ""):
    
    enriched_requirements = []

    for requirement in requirements:
        strategy = analyze_requirement(requirement)

        prompt = build_requirement_prompt(requirement, strategy)
        
        enriched_requirements.append(prompt)
    
    task = "\n\n".join(enriched_requirements) 

    print("\n ==== GENERATED TASK ====")
    print(task)
    print("======== \n")


    # Run AI prompt, sanitize JSON response, and produce feedback string for prompt if needed
    results = break_down_task(task, feedback)

    print("\n=== RAW AI RESPONSE ===")
    print(results)
    print("=======================\n")

    # Transform back to JSON to satisfy service requirements
    data = json.loads(results)

    return data["test_cases"]