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



# Missing required fields should fail validation
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



# Empty steps array should fail validation
def test_empty_steps_are_rejected():
    # Arrange
    test_cases = [
        {
            "title": "Valid login",
            "steps": [],
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
    assert results[0]["valid"] == False
    assert any(
        issue["rule"] == "NO_STEPS" for issue in results[0]["issues"]["critical"]
    )


# Weak assertions reduce confidence
def test_weak_assertion_reduces_confidence():
    # Arrange
    test_cases = [
        {
            "title": "Valid login",
            "steps": ["Go to page", "Enter creds", "Click login"],
            "expected": "User logs in",
            "assertion": {
                "type": "text_present",
                "value": "a",
                "locator": "#flash"
            },
            "type": "positive"
        }
    ]

    # Act
    results = validate_test_cases(test_cases)

    # Assert
    assert results[0]["confidence"] == "MEDIUM"
    assert any(
        issue["rule"] == "ASSERTION_LENGTH" for issue in results[0]["issues"]["warning"]
    )