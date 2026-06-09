from framework.validation.ai_validator import ConfidenceLevel

def passes_quality_gate(validation_results: list) -> dict:

    all_valid = all(result["valid"] for result in validation_results)

    has_low_confidence = any(
        result["confidence"] == ConfidenceLevel.LOW
        for result in validation_results
        )
    
    return {
        "passed": all_valid and not has_low_confidence,
        "all_valid": all_valid,
        "has_low_confidence": has_low_confidence
    }