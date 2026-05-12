import json

# Force validator gate retry timeouts. Place inside of break_down_task in ListParent.py
force_failure = json.dumps({
        "test_cases": [
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
    })