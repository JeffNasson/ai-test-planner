from playwright.sync_api import sync_playwright
from assertion_runner import run_real_assertion

# Simulate API create user function. In an enterprise application we want to do this via internal API and send credentials securely
def create_test_user():
    return {
        "username": "tomsmith",
        "password": "SuperSecretPassword!"
    }

def execute_tests(test_cases):
    results = []

    with sync_playwright() as sp:
        browser = sp.chromium.launch(headless=False)

        for case in test_cases:
            context = browser.new_context() # create a new browser context for each test case
            page = context.new_page() # create a new page within the context

            try:
                # Navigate
                url = case.get("url", "https://the-internet.herokuapp.com/login")
                page.goto(url)

                print(f"\nTest Case ({case['type']}): {case['title']}")

                for i, step in enumerate(case["steps"], start =1):
                    print(f"{i}. {step}")
                print(f"Expected: {case['expected']}\n")
                print(f"Assertion: {case['assertion']}\n")
                
                # Set inputs based on test case type
                inputs = case.get("inputs", {})
                if case['type'] == "positive": 
                    user = create_test_user()
                    username = user["username"]
                    password = user["password"]
                else:
                    username = inputs.get("username","")
                    password = inputs.get("password","")

                page.fill("#username", username)
                page.fill("#password", password)
                page.click("button[type='submit']")

                # Run assertion
                run_real_assertion(page, case["assertion"])

                results.append(("PASS", case["title"]))
            
            except AssertionError as e:
                print(f"\nFail: {e}")
                results.append(("FAIL", case["title"]))
            
            except Exception as e:
                print(f"\nERROR: {e}")
                results.append(("ERROR", case["title"]))
            
            context.close() # Close the context after each test case to ensure isolation
        browser.close()
    
    return results