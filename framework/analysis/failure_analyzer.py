# Expected test_result shape:
# {
#     "status": "FAIL",
#     "title": "Login fails with invalid password",
#     "type": "negative",
#     "steps": [
#         "Navigate to login page",
#         "Enter valid username",
#         "Enter invalid password",
#         "Click submit"
#     ],
#     "expected": "User should see an invalid credentials message",
#     "assertion": {
#         "type": "text_present",
#         "locator": ".error-message",
#         "value": "Invalid credentials"
#     },
#     "error": "Expected text was not found on the page"
# }

# Analyze failed test execution results and provide structured diagnostics.
# This is a rule-based analysis layer that helps explain WHY a test failed.
def analyze_failures(test_result: dict) -> dict:
    
    # This is a default structured analysis response that serves as a template for how failure analysis results should be formatted. It includes fields for the type of failure, possible causes, and suggested actions. This structure allows for consistent reporting of failure analysis across different test cases and can be easily extended with specific rules and logic to populate these fields based on the details of the test result.
    analysis = {
        "failure_type": "UNKNOWN",
        "possible_causes": [],
        "suggested_actions": []
    }

    # Extract common execution metadata
    status = test_result.get("status") # e.g., "failed", "error", "passed"
    error = test_result.get("error", "").lower() # Error message details
    assertion = test_result.get("assertion", {}) # The assertion that was evaluated

    # If test passed, no analysis needed
    if status == "PASS":
        return analysis
    
    # Detect assertion failures
    if "assertion" in error:
        analysis["failure_type"] = "ASSERTION_FAILURE"

        analysis["possible_causes"].append("Expected UI behavior did not match actual result")
        analysis["possible_causes"].append("Application UI or API behavior may have changed")

        analysis["suggested_actions"].append("Review assertion expectations")
        analysis["suggested_actions"].append("Verify application behavior manually")


    # Detect timeout failures
    elif "timeout" in error:
        analysis["failure_type"] = "TIMEOUT_FAILURE"
        
        analysis["possible_causes"].append("Application response time exceeded timeout threshold")
        analysis["possible_causes"].append("Element selector may no longer exist")

        analysis["suggested_actions"].append("Verify selector validity")
        analysis["suggested_actions"].append("Increase timeout threshold if appropriate")
    

    # Detect locator failures
    elif "locator" in error:
        analysis["failure_type"] = "LOCATOR_FAILURE"
        
        analysis["possible_causes"].append("CSS selector or locator no longer matches UI")
        analysis["possible_causes"].append("Frontend structure may have changed")

        analysis["suggested_actions"].append("Inspect DOM structure")
        analysis["suggested_actions"].append("Update selector strategy")

    
    # Generic fallback analysis
    else: 
        analysis["failure_type"] = "UNKNOWN_FAILURE"

        analysis["possible_causes"].append("Unhandled execution failure")

        analysis["suggested_actions"].append("Review execution logs")
    
    return analysis