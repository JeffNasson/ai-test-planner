def validate_test_cases(test_cases):
    results = []

    for test_case in test_cases:
        issues = {
            "critical": [],
            "warning": [],
            "info": []
        }
        score:int = 100 # Start with a perfect score of 100 for each test case and deduct points for each issue found.
        critical_failure:bool = False # This flag can be used to immediately mark a test case as invalid if a critical issue is found (e.g., missing required fields).

        # Rule 1: Required fields check (-25 points for each missing required field)
        required_fields = ["title", "steps", "expected", "assertion"] # These are the fields that must be present and non-empty in each test case. The 'assertion' field is also required to ensure that there is a clear check for the expected behavior of the test case.
        for field in required_fields:
            if not test_case.get(field):
                score -= 25
                issues["critical"].append(f"Missing required field: {field}")
                critical_failure = True # If a required field is missing, we can consider this a critical failure and mark the test case as invalid immediately.
        
        # Rule 2: Steps must exist (-20 points if not steps provided)
        if len(test_case.get("steps", [])) == 0: # This checks if the 'steps' field is present and contains at least one step.
            issues["critical"].append("No steps provided")
            score -= 20
            critical_failure = True
        
        # Rule 3: Assertion logic check (-20 points for missing locator in text_present assertions)
        assertion = test_case.get("assertion", {}) # This retrieves the 'assertion' field from the test case, or an empty dictionary if it is not present.
        if assertion.get("type") == "text_present" and not assertion.get("locator"): # This checks if the assertion type is 'text_present' and if the 'locator' field is missing.
            issues["warning"].append("Missing locator for text_present")
            score -= 20
        
        # Rule 4: Edge case logic check (-15 points for edge cases reusing negative expectations)
        if test_case.get("type") == "edge":
            if "invalid" in test_case.get("expected", "").lower(): # This checks if the test case is categorized as an edge case and if the expected result contains the word 'invalid', which would indicate that it is not properly categorized as an edge case.
                issues["critical"].append("Edge case reusing negative expectation")
                score -= 15
                critical_failure = True 
        
        # Rule 5: Weak assertion value (20-25 points for poor quality assertions)
        value = assertion.get("value","").strip()

        if not value:
            score -= 25
            issues["critical"].append("Assertion value is empty")
            critical_failure = True
        elif len(value) < 5:
            score -= 20
            issues["warning"].append("Assertion value too short to be meaningful")
        
        # Normalize score
        score = max(score, 0) # Ensure that the score does not go below 0.

        confidence:str = ""
        if score >= 90:
            confidence = "HIGH" # Test is reliable
        elif score >= 75: 
            confidence = "MEDIUM" # Passable but has some issues
        else:
            confidence = "LOW" # Weak test


        results.append({
            "title": test_case.get("title"),
            "score": score,
            "confidence": confidence,
            "valid": score >= 70 and not critical_failure, # A test case is considered valid if it has a score of 70 or above and does not have any critical failures (e.g., missing required fields).
            "issues": issues
        })
    
    return results
