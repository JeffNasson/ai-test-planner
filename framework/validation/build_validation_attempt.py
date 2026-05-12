# Build a structured telemetry snapshot for a single validation attempt.
# This keeps orchestration logic cleaner and centralizes validation telemetry formatting.
def build_validation_attempt(attempt: int, validation_results: list, validation_summary: dict, rule_frequency: dict, retry_count: int, passed_gate:bool) -> dict:
    # Return a structured snapshot object representing one validation cycle
    return{
        "attempt": attempt + 1, # Convert from 0-based index to human-readable numbering
        "passed_gate": passed_gate, # Whether this attempt passed validation + confidence gating
        "retry_count": retry_count, # Total retries so far in this workflow

        # Copy current telemetry state so historical attempts are preserved correctly.
        # Without .copy(), future mutations would overwrite previous attempt history.
        "validation_summary": validation_summary.copy(),

        # Copy rule frequency telemetry for this attempt snapshot
        "rule_frequency": rule_frequency.copy(),

        # Store detailed validation results for each generated test case
        "results": validation_results    
    }