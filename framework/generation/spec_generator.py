# Business Logic Layer for generating test cases from requirements/specs
# Requirements/Specs -> Test Cases
# Adapter around AI engine

import json
from orchestrator.pipeline import break_down_task
from framework.generation.requirement_analyzer import analyze_requirement
from framework.generation.downstream_behavior_expectations import get_expected_downstream_behaviors

# Helper function for prompt logic
def build_requirement_prompt(requirement: str, strategy: dict, downstream_behaviors: list) -> str:

    focus_areas = "\n".join(
        f"- {area}" for area in strategy["focus_areas"]
    )

    focus_behaviors = "\n".join(
        f"- {behavior}" for behavior in downstream_behaviors
    )

    return f"""
Recommended Coverage: 
{focus_areas}

Additional Guidance:
- The generated positive, negative, and edge cases should collectively cover these focus areas whenever possible.
- Positive test cases must validate one or more supplied downstream behaviors when downstream behaviors exist.
- Expected results and assertions must reference downstream behaviors when relevant.
    
Requirement:
{requirement}

Domain:
{strategy["domain"]}

Focus Areas:
{focus_areas}

Downstream Behaviors:
{focus_behaviors}
"""


# Generate test cases using AI Prompt
def generate_from_requirements(requirements: list, feedback: str = "") -> dict:
    
    enriched_requirements = []

    for requirement in requirements:

        # Analyze spec string for keywords and return domain strategy dict
        strategy = analyze_requirement(requirement)

        # Analyze spec string for keywords and determine if downstream behaviors need to be triggered and return a list of downstream behaviors
        downstream_behaviors = get_expected_downstream_behaviors(requirement)

        # Build prompt for AI using spec requirement str, domain strategy dict, and downstream_behaviors list
        prompt = build_requirement_prompt(requirement, strategy, downstream_behaviors)
        
        # Append the prompt to enriched_requirements list
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