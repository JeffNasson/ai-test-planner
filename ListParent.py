from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from assertion_runner import run_real_assertion

DEBUG = False

PLANS_DIR = "test_cases"
if not os.path.exists(PLANS_DIR):
    os.makedirs(PLANS_DIR)

load_dotenv()
client = OpenAI()
MODEL = "gpt-4o-mini"



# Search for list files
def list_plans():
    # files returns a list of all files in the test_plans directory that start with "plan_"
    files = [f for f in os.listdir(PLANS_DIR) if f.startswith("plan_")]
    
    # if not files checks if the list is empty. If it is empty, it prints "No deathstar plans found." and returns an empty list. This is to handle the case where there are no plans saved yet.
    if not files:
        print("No deathstar plans found.")
        return[]
    
    print("\nSaved Deathstar Plans:")

    # enumerate(files, start=1) gives us both the index (starting from 1) and the filename for each file in the list. We can then print them in a numbered list format.
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    
    return files

# read the file
def read_plan(filename:str):
    filepath = os.path.join(PLANS_DIR, filename)
    try:
        with open(filepath,"r") as file:
            content=file.read()
            print("\n--- Plan Content ---\n")
            print(content)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    input("\nPress Enter to continue...")



# Houses prompting logic
# This function takes a task description as input and uses the OpenAI API to generate test cases based on that task. It sends a prompt to the model asking it to create 3 test cases (positive, negative, and edge) in a specific JSON format. The response is then cleaned and returned as a string. The function also includes debug prints to help with troubleshooting and understanding the AI's response.
def break_down_task(task: str) -> str:
    print("Breaking task down...")
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
                    "title":"short test case name",
                    "url": "https://www.example.com/login",
                    "type": "positive, negative, or edge",
                    "steps":["step 1","step 2","step 3"],
                    "expected": "expected result of test case",
                    "assertion": "What should be verified"
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
        - No extra text outside JSON

        Scenario: {task}
        """,
        max_output_tokens=350
    )

    print("Done breaking task down!")
    print(f"Tokens used: {response.usage}")
    raw_text = response.output[0].content[0].text

    if DEBUG:
        print("\n--- RAW AI RESPONSE ---\n")
        print(raw_text)
    
    cleaned = raw_text.strip() # Remove leading and trailing whitespace. Whitespace can cause issues when trying to parse JSON

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json","").replace("```","").strip() # If the response is wrapped in markdown code blocks, remove them.
    
    if DEBUG:
        print("\n--- CLEANED JSON ---\n")
        print(cleaned)

    return cleaned

def run_test_cases(test_cases):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as sp:
        browser = sp.chromium.launch(headless=False)

        for case in test_cases:
            print(f"\nTest Case ({case['type']}): {case['title']}")
            input("\nPress Enter to see steps...\n")

            context = browser.new_context() # create a new browser context for each test case to ensure isolation
            page = context.new_page() # create a new page within the context

            url = case.get("url","https://www.google.com") # get the url from the test case, or default to google if not provided
            page.goto("https://the-internet.herokuapp.com/login") # navigate to herokuapp login page for demo purposes. In a real application, you would use the url provided in the test case.

            for i, step in enumerate(case["steps"], start =1):
                print(f"{i}. {step}")
                time.sleep(.5) # add a small delay between steps for better readability. (Don't use in prod for obvious reasons, but it helps with readability in this demo.)
            print(f"Expected: {case['expected']}\n")
            print(f"Assertion: {case['assertion']}\n")

            try:
                if case["type"] == "positive":
                    username = "tomsmith"
                    password = "SuperSecretPassword!"

                elif case["type"] == "negative":
                    username = "tomsmithfail"
                    password = "wrongpassword"
                
                elif case["type"] == "edge":
                    username = ""
                    password = ""

                # Fill login form
                page.fill("#username", username)
                page.fill("#password", password)
                # Submit form
                page.click("button[type='submit']")

                run_real_assertion(page, case['assertion'])
            except AssertionError as e:
                print(f"\nFail: {e}\n") # If test fails, print a failure message and execute the next test case instead of stopping the whole process.
            context.close() # close the context to clean up after the test case
        browser.close() # close the browser after all test cases have been executed

def job_helper(task: str) -> str:
    print("\nGenerating test cases...")

    breakdown = break_down_task(task)

    if DEBUG:
        print("\n--- FINAL JSON BEING PARSED ---\n")
        print(breakdown)
        print(f"\nTYPE: {type(breakdown)}")
    
    if not breakdown.strip().endswith("}"):
        print("Incomplete AI response, likely token limit hit.\n")
        print(breakdown)
        return "Error: Incomplete AI response."

    try:
        data = json.loads(breakdown) #json.loads() takes json data and deserializes it into a python object (in this case, a dictionary). We can then access the "steps" key to get the list of steps.
        test_cases = data.get("test_cases", [])[:3] # take only the first 3 test cases to ensure we don't exceed our token limit when printing steps. Return an empty array if test_cases does not exist. In a real application, you would want to handle this more robustly, perhaps by paginating the output or allowing the user to select which test cases to view.
    except json.JSONDecodeError:
        print("Failed to parse AI response as JSON. \n")
        print(breakdown)
        return "Error: AI response was not valid JSON"
    
    run_test_cases(test_cases)

    safe_task = "".join(character for character in task.lower() if character.isalnum() or character == " ").strip().replace(" ","_")[:50] # remove special characters, replace spaces with underscores, and limit filename length to 50 characters
    filename = f"plan_{safe_task}.txt"
    filename = os.path.join(PLANS_DIR, f"plan_{safe_task}.txt") # save the file in the test_plans directory

        # opens a file called plan.txt in write mode. If the file doesn't exist, it will be created. If it does exist, it will be overwritten.
        # "w" writes to the file, "a" appends to the file, "r" reads the file. We use a context manager (the with statement) to ensure that the file is properly closed after we're done writing to it.
    with open(filename,"w") as file: 
        file.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        file.write(f"Generated by AI QA Assistant\n")
        file.write(f"Task: {task}\n")
        file.write(f"\n\n=== Test Cases ===\n")
        for case in test_cases:
            file.write(f"\nTest Case ({case['type']}): {case['title']}\n")
            for i, step in enumerate(case["steps"], start=1):
                file.write(f"{i}. {step}\n")
            file.write(f"Expected: {case['expected']}\n")
            file.write(f"Assertion: {case['assertion']}\n")

    return ""


# Execution
if __name__ == "__main__":
    while True:
        print("\n=== Deathstar Planner ===")
        print("1. Create new plan")
        print("2. View saved plans")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter a task: ")
            result = job_helper(task)
            print(result)
        
        elif choice == "2":
            files = list_plans()

            # If no files are found, print a message and skip to the next iteration of the loop
            if not files:
                continue

            file_choice = input("\nEnter number to view: ")

            # Check if the input is a numeric digit and within the valid range of file indices
            if not file_choice.isdigit():
                print("invalid input.")
                continue
            
            # set index to the integer value of file_choice minus 1 to account for 0-based indexing of the files list
            index = int(file_choice) - 1

            # Check if the entered index is valid when compared to the length of the files list. If it is valid, call read_plan with the selected file.
            if 0 <= index < len(files):
                read_plan(files[index])
            else:
                print("Invalid selection.")

        elif choice == "3":
            print("Goodbye")
            break
        
        else:
            print("Invalid choice, try again.")
