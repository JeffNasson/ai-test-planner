from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
MODEL = "gpt-4o-mini"


# Houses prompting logic
def generate_test_cases(task: str, feedback: str = "") -> str:
    client = OpenAI()
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
                    "inputs": {{}},
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
        - Use the supplied Domain, Focus Areas, and Downstream Behaviors when generating test cases.
        - Expected results should incorporate relevant downstream behaviors when appropriate.
        - Inputs should contain fields relevant to the supplied requirement and domain.
        - Ensure the positive, negative, and edge cases cover the identified focus areas when applicable.
        - Prioritize the supplied Focus Areas over generic test generation.
        - Exactly 3 test cases
        - One must be positive
        - One must be negative
        - One must be an edge case
        - Each test case can have up to a maximum of 3 steps
        - Assertion must describe what is checked and match actual system behavior
        - Steps must be clear user actions in one sentence each
        - Expected result field must be one short sentence describing the ideal behavior of the test case
            - Empty fields -> "User should see required field validation"
        - Inputs must match the test type:
            - Edge -> empty or boundary values
        - Each test case must have a unique and correct assertion value
        - Edge cases (empty fields) must not reuse invalid credential messages
        - Edge cases must test boundary conditions or unusual but potentially valid inputs and must not reuse the same expected result or assertion as the negative test.
        - Use realistic messages for each scenario based on actual system behavior:
        - No extra text outside JSON

        Scenario: {task}

        Fix all listed issues from the previous attempt. Do not repeat them: 
        {feedback}
        Generate improved test cases.

        """,
        max_output_tokens=800
    )

    print("Done breaking task down!")
    print(f"Tokens used: {response.usage}")
    return response.output[0].content[0].text

