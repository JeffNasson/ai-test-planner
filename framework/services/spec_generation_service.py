from framework.generation.spec_generator import generate_from_requirements
from framework.services.validation_service import validate
from framework.validation.ai_validator import ConfidenceLevel
from framework.validation.feedback_builder import build_feedback
from framework.validation.quality_gate import passes_quality_gate

def spec_generation_service(payload: dict):
    requirements = payload["requirements"]

    test_cases = generate_from_requirements(requirements)

    # Convert test_cases to the expected format for validation
    validation_payload = {"test_cases": test_cases}

    validation_results = validate(validation_payload)

    # Run validation gate
    gate = passes_quality_gate(validation_results)

    if gate["passed"]:
        return{
            "attempts":[
                {
                    "attempt": 1,
                    "results": validation_results
                }
            ],
            "passed_gate": True
        }
    
    # If tests do not pass the gate, generate feedback, and generate the tests again using the feedback
    feedback = build_feedback(validation_results)
    test_cases = generate_from_requirements(requirements, feedback)
    validation_payload = {"test_cases": test_cases}
    validation_results = validate(validation_payload)
    retry_gate = passes_quality_gate(validation_results)

    if retry_gate["passed"]:
        return {
            "attempts": 2,
            "passed_gate": True,
            "results": validation_results
        }

    # Fail after max tries
    return {
        "attempts": 2,
        "passed_gate": False,
        "results": validation_results
    }