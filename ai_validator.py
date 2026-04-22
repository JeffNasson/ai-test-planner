def validate_test_cases(test_cases):
    results = []

    for test_case in test_cases:
        issues = []

        # Rule 1: Required fields check
        required_fields = ["title", "steps", "expected", "assertion"] # These are the fields that must be present and non-empty in each test case. The 'assertion' field is also required to ensure that there is a clear check for the expected behavior of the test case.
        for field in required_fields:
            if not test_case.get(field):
                issues.append(f"Missing required field: {field}")
        
        # Rule 2: Steps must exist
        if len(test_case.get("steps", [])) == 0: # This checks if the 'steps' field is present and contains at least one step.
            issues.append("No steps provided")
        
        # Rule 3: Assertion logic check
        assertion = test_case.get("assertion", {}) # This retrieves the 'assertion' field from the test case, or an empty dictionary if it is not present.
        if assertion.get("type") == "text_present" and not assertion.get("locator"): # This checks if the assertion type is 'text_present' and if the 'locator' field is missing.
            issues.append("Missing locator for text_present")
        
        # Rule 4: Edge case logic check
        if test_case.get("type") == "edge":
            if "invalid" in test_case.get("expected", "").lower(): # This checks if the test case is categorized as an edge case and if the expected result contains the word 'invalid', which would indicate that it is not properly categorized as an edge case.
                issues.append("Edge case reusing negative expectation")

        results.append({
            "title": test_case.get("title"),
            "valid": len(issues) == 0,
            "issues": issues
        })
    
    return results
