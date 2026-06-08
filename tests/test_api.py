import requests

def test_validate_tests_returns_200_for_valid_request(valid_test_case):
    response = requests.post(
        "http://127.0.0.1:8000/validate-tests",
        json={"test_cases": [valid_test_case]}
    )

    # Turn http response into json
    data = response.json()

    assert response.status_code == 200
    assert data[0]["valid"] is True


def test_validate_tests_returns_invalid_for_missing_fields():
    response = requests.post(
        "http://127.0.0.1:8000/validate-tests",
        json={
            "test_cases": [
                {
                    "title": "Login Test"
                }
            ]
        }
    )

    data = response.json()

    assert data[0]["valid"] is False
    assert any(
        issue["rule"] == "REQUIRED_FIELD_MISSING" for issue in data[0]["issues"]["critical"]
    ) is True
    assert len(data[0]["issues"]["critical"]) > 0



def test_validate_tests_returns_empty_list_for_empty_input():
    response = requests.post(
    "http://127.0.0.1:8000/validate-tests",
    json={
        "test_cases": []
    }
)
    assert response.status_code == 200
    data = response.json()
    assert data == []