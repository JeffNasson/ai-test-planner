from framework.validation.ai_validator import validate_test_cases


# Valid login should receive HIGH confidence.
def test_valid_login_is_high_confidence():

    # Arrange
    test_cases = [
        {
            "title": "Valid login",
            "steps": ["Go to page", "Enter creds", "Click login"],
            "expected": "User logs in",
            "assertion": {
                "type": "url_contains",
                "value": "/secure",
                "locator": ""
            },
            "type": "positive"
        }
    ]

    # Act
    results = validate_test_cases(test_cases)

    # Assert
    assert results[0]["confidence"] == "HIGH"
    assert results[0]["valid"] == True