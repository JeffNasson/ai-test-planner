import pytest

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



# Missing required fields fails the test
@pytest.mark.parametrize(
    "test_case",
    [
        # title missing
        {
            "steps": ["Step 1"],
            "expected": "Success",
            "assertion": {
                "type": "text_present",
                "value": "Success",
                "locator": "#flash"
            }
        },
        # Steps missing
        {
            "title": "Login Test",
            "expected": "Success",
            "assertion": {
                "type": "text_present",
                "value": "Success",
                "locator": "#flash"
            }
        },
        # Expected missing
        {
            "title": "Login Test",
            "steps": ["Step 1"],
            "assertion": {
                "type": "text_present",
                "value": "Success",
                "locator": "#flash"
            }
        },
        # Assertion missing
        {
            "title": "Login Test",
            "steps": ["Step 1"],
            "expected": "Success"
        }
    ]
)
def test_missing_required_fields_are_rejected(test_case):
    
    # Act
    results = validate_test_cases([test_case])

    # Assert
    assert results[0]["valid"] == False