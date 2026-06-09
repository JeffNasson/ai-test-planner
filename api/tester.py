import requests

# response = requests.post(
#     "http://127.0.0.1:8000/validate-tests",
#     json={
#         "test_cases": [
#             {
#                 "title":"Login Test"
#             }
#         ]
#     }
# )

response = requests.post(
    "http://127.0.0.1:8000/generate-tests",
    json={
        "requirements": ["Users can login"]
    }
)

print(response.status_code)
print(response.text)
