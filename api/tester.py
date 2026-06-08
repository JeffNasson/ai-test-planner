import requests

response = requests.post(
    "http://127.0.0.1:8000/validate-tests",
    json={
        "test_cases": [
            {
                "title":"Login Test"
            }
        ]
    }
)

print(response.status_code)
print(response.text)
