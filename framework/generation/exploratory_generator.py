import json
from orchestrator.pipeline import break_down_task
from framework.generation.exploratory_themes import EXPLORATORY_THEMES
from framework.generation.requirement_analyzer import analyze_requirement
from framework.generation.exploratory_prompt_builder import build_exploratory_prompt

def generate_exploratory_scenarios(requirements: list, feedback: str = "", mode: str = "exploratory") -> dict:
    enriched_requirements = []
    
    for requirement in requirements:
        
        # Analyze spec string for keywords and return domain strategy dict
        strategy = analyze_requirement(requirement)

        themes = []

        # Loop through each focus_area and add it to themes list
        for focus_area in strategy["focus_areas"]:
            themes.extend(
                EXPLORATORY_THEMES.get(focus_area, [])
            )

        # Build prompt for AI using spec requirement str, domain strategy dict, and themes list
        prompt = build_exploratory_prompt(requirement, strategy, themes)

        # Append the prompt to enriched_requirements list
        enriched_requirements.append(prompt)
    
    task = "\n\n".join(enriched_requirements)

    print("\n ==== GENERATED TASK ====")
    print(task)
    print("======== \n")

    # Run AI prompt, sanitize JSON response, produce feedback string for prompt if needed, and set mode to exploratory
    results = break_down_task(task, feedback, mode)

    print("\n=== RAW AI RESPONSE ===")
    print(results)
    print("=======================\n")

    # Transform back to JSON to satisfy service requirements
    data = json.loads(results)

    
    return data