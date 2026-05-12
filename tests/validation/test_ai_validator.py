from framework.validation.ai_validator import validate_test_cases

def run_validator_tests():
    test_cases = [
        # GOOD CASE
        {
            "title": "Valid login",
            "steps": ["Go to page", "Enter creds", "Click login"],
            "expected": "User logs in",
            "assertion": {
                "type": "url_contains",
                "value": "/secure",
                "locator": ""
            },
            "type": "positive"
        },

        # MISSING FIELD
        {
            "title": "Missing steps",
            "steps": [],
            "expected": "Fails",
            "assertion": {},
            "type": "negative"
        },

        # BAD EDGE LOGIC
        {
            "title": "Edge wrong expectation",
            "steps": ["Do thing"],
            "expected": "Invalid login message",
            "assertion": {
                "type": "text_present",
                "value": "invalid",
                "locator": "#flash"
            },
            "type": "edge"
        },

        # WEAK ASSERTION
        {
            "title": "Weak assertion",
            "steps": ["Do thing"],
            "expected": "Something",
            "assertion": {
                "type": "text_present",
                "value": "a",
                "locator": "#flash"
            },
            "type": "negative"
        }
    ]

    results = validate_test_cases(test_cases)

    for r in results:
        print("\n---")
        print(f"Title: {r['title']}")
        print(f"Score: {r['score']}")
        print(f"Valid: {r['valid']}")
        print(f"Issues: {r['issues']}")

if __name__ == "__main__":
    run_validator_tests()