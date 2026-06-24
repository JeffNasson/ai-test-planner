import os
from playwright.sync_api import sync_playwright
from framework.assertions.assertion_runner import run_real_assertion
from framework.data.test_data_manager import resolve_credentials
from config.config import get_base_url


def execute_tests(test_cases):
    results = []
    HEADLESS = os.getenv("CI", "false") == "true" # Set headless mode based on CI environment variable. This allows for faster execution in CI environments where a UI is not needed, while still allowing for visual debugging when running locally.

    with sync_playwright() as sp:
        browser = sp.chromium.launch(headless = HEADLESS)

        for case in test_cases:
            context = browser.new_context() # create a new browser context for each test case
            page = context.new_page() # create a new page within the context

            try:
                # Navigate to URL from test case
                page.goto(case["url"])

                print(f"\nTest Case ({case['type']}): {case['title']}")

                for i, step in enumerate(case["steps"], start =1):
                    print(f"{i}. {step}")
                print(f"Expected: {case['expected']}\n")
                print(f"Assertion: {case['assertion']}\n")
                
                # Set inputs based on test case type
                inputs = case["inputs"]
                username = inputs.get("username", "")
                password = inputs.get("password", "")

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