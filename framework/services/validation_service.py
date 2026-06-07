from framework.validation.ai_validator import validate_test_cases
from framework.events.event_publisher import publish_event

def validate(payload: dict):
    test_cases = payload["test_cases"]

    results = validate_test_cases(test_cases)

    publish_event("ValidationCompleted", results)

    return results 