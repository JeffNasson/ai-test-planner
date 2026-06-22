from framework.generation.exploratory_scenarios import EXPLORATORY_SCENARIOS
from framework.generation.requirement_analyzer import analyze_requirement

def generate_exploratory_scenarios(requirements: list) -> dict:
    results = {
        "results": []
    }
    
    for requirement in requirements:
        
        # Analyze spec string for keywords and return domain strategy dict
        strategy = analyze_requirement(requirement)

        # Create variable equal to the domain strategy
        focus_areas = strategy["focus_areas"]

        # Create object based on expected output
        requirement_result = {
            "requirement": requirement,
            "domain": strategy["domain"],
            "focus_areas": {}
        }

        # Loop through each focus_area and set result to focus_areas in requirement_result
        for focus_area in focus_areas:
            requirement_result["focus_areas"][focus_area] = (
                EXPLORATORY_SCENARIOS.get(focus_area, [])
            )
        # append each result to results list
        results["results"].append(requirement_result)
    
    return results