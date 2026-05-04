attempt:int
test_cases:str

# Add an assertion confidence penalty bring the test down to 75 with a critical failure on the first test validation check. This will trigger the retry logic.
def force_weak_assertion(attempt, test_cases):
    if attempt == 0:
        test_cases[0]["assertion"]["value"] = ""