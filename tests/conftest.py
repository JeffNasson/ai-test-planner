import pytest

@pytest.fixture
def valid_test_case():
    return {
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