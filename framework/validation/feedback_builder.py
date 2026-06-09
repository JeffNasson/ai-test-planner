# Convert validation results into AI feedback

from framework.validation.ai_validator import ConfidenceLevel

def build_feedback(validation_results: list) -> str:
    # Build feedback loop for invalid and low confidence and place findings in feedback variable
    feedback = ""
        
    for result in validation_results:
        if not result["valid"] or result["confidence"] == ConfidenceLevel.LOW:
            feedback += f"\nTest Case: {result['title']}\n"

            for issue in result["issues"]["critical"]:
                feedback += f"- {issue['message']}\n"

            if result["confidence"] == ConfidenceLevel.LOW:
                feedback += "- Improve test clarity, assertions, or completeness\n"
    return feedback
        
