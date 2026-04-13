from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
MODEL = "gpt-4o-mini"


# Houses prompting logic
def generate_test_cases(task: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input = f"""
        You are a QA engineer. 

        Given the following feature or scenario, generate exactly 3 test cases.

        1 positive test case (valid behavior)
        1 negative test case (invalid behavior)
        1 edge case (boundary or unusual condition)

        Return only valid JSON in this format: {{
            "test_cases":[
                {{
                    "title": "short test case name",
                    "url": "https://www.example.com/login",
                    "type": "positive, negative, or edge",
                    "inputs": {{
                        "username": "string",
                        "password": "string"
                    }},
                    "steps": ["step 1","step 2","step 3"],
                    "expected": "expected result of test case",
                    "assertion": {{
                        "type": "url_contains | element_visible | text_present",
                        "value": "what to check",
                        "locator": "optional css selector"
                    }}
                }}
            ]
        }}

        Rules:
        - Exactly 3 test cases
        - One must be positive
        - One must be negative
        - One must be an edge case
        - Each test case can have up to a maximum of 3 steps
        - Assertion must describe what is checked
        - Steps must be clear user actions in one sentence each
        - Expected result must be one short sentence describing the expected outcome of the test case
        - Inputs must match the test type:
            - Positive -> valid credentials
            - Negative -> invalid credentials
            - Edge -> empty or boundary values
        - For the login page https://the-internet.herokuapp.com/login:
            - Success login redirects to "/secure"
            - User "/secure" for url_contains assertions
        - Each test case must have a unique and correct assertion value
        - Edge cases (empty fields) must not reuse invalid credential messages
        - Use realistic messages for each scenario:
            - Invalid login -> "Your username is invalid!"
            - Empty fields -> "Your username is required!"
        - No extra text outside JSON

        Scenario: {task}
        """,
        max_output_tokens=450
    )

    print("Done breaking task down!")
    print(f"Tokens used: {response.usage}")
    return response.output[0].content[0].text

