from framework.generation.spec_generator import generate_from_requirements
from framework.services.validation_service import validate

def spec_generation_service(payload: dict):
    requirements = payload["requirements"]

    test_cases = generate_from_requirements(requirements)

    # Convert test_cases to the expected format for validation
    validation_payload = {"test_cases": test_cases}

    # Return validation results
    return validate(validation_payload)