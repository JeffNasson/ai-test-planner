from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime

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

# Determine if task is easy or hard. If it's easy, we can do it right away. If it's hard, we need to break it down into smaller steps.
def analyze_task(task:str)->str:
    response = client.responses.create(
        model=MODEL,
        input=f"in one short sentence, decide if task is easy or hard this format: 'Easy: reason' or 'Hard: reason' -> {task}",
        max_output_tokens=50
    )
    return response.output[0].content[0].text


# Transformation function which is called if the task is hard, to break it down into smaller steps.
def break_down_task(task: str) -> str:
    print("Breaking task down...")
    response = client.responses.create(
        model=MODEL,
        input = f"""
        You are a QA engineer. 

        Given the follow feature or scenario, generate exactly 2 test cases.

        Return only valid JSON in this format: {{
            "test_cases":[
                {{
                    "title":"short test case name",
                    "steps":["step 1","step 2","step 3"],
                    "expected": "expected result of test case
                }}
            ]
        }}

        Rules:
        - Exactly 3 test cases
        - Each test case must have 3 steps
        - Steps must be clear user actions in one sentence each
        - Expected result must be one short sentence describing the expected outcome of the test case
        - No extra text outside JSON

        Scenario: {task}
        """,
        max_output_tokens=150
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


def job_helper(task: str) -> str:
    analysis = analyze_task(task)

    print(f"{analysis}\n\nGenerating test cases...")

    breakdown = break_down_task(task)

    if DEBUG:
        print("\n--- FINAL JSON BEING PARSED ---\n")
        print(breakdown)
        print(f"\nTYPE: {type(breakdown)}")

    try:
        data = json.loads(breakdown) #json.loads() takes json data and deserializes it into a python object (in this case, a dictionary). We can then access the "steps" key to get the list of steps.
        test_cases = data["test_cases"][:2] # take only the first 2 test cases to ensure we don't exceed our token limit when printing steps. In a real application, you would want to handle this more robustly, perhaps by paginating the output or allowing the user to select which test cases to view.
    except json.JSONDecodeError:
        print("Failed to parse AI response as JSON. \n")
        print(breakdown)
        return "Error: AI response was not valid JSON"
    
    for case in test_cases:
        print(f"\nTest Case: {case['title']}")
        input("Press Enter to see steps...")

        for step in case["steps"]:
            print(f"- {step}")
            time.sleep(.5) # add a small delay between steps for better readability. (Don't use in prod for obvious reasons, but it helps with readability in this demo.)
        print(f"Expected: {case['expected']}\n")

    safe_task = "".join(character for character in task.lower() if character.isalnum() or character == " ").strip().replace(" ","_")[:50] # remove special characters, replace spaces with underscores, and limit filename length to 50 characters
    filename = f"plan_{safe_task}.txt"
    filename = os.path.join(PLANS_DIR, f"plan_{safe_task}.txt") # save the file in the test_plans directory

        # opens a file called plan.txt in write mode. If the file doesn't exist, it will be created. If it does exist, it will be overwritten.
        # "w" writes to the file, "a" appends to the file, "r" reads the file. We use a context manager (the with statement) to ensure that the file is properly closed after we're done writing to it.
    with open(filename,"w") as file: 
        file.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        file.write(f"Generated by AI QA Assistant\n")
        file.write(f"Task: {task}\n")
        file.write(f"{analysis}\n\n=== Test Cases ===\n")
        for case in test_cases:
            file.write(f"\nTest Case: {case['title']}\n")
            for step in case["steps"]:
                file.write(f"- {step}\n")
            file.write(f"Expected: {case['expected']}\n")

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
