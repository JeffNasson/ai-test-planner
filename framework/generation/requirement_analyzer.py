# Full flow
# Requirement/Spec string is received
# Loop through DOMAINS searching for KEYWORDS
# If any KEYWORDS match with a DOMAIN return that DOMAINS STRATEGY dictionary which can now be used in generation prompt

# Current issue(s):
#   1. If the same keyword is shared between domains, whichever domain that is evaluated first wins and gets the test
#       a. Fix idea: Implement a weighted scoring system so the most relevant domain is selected

from copy import deepcopy

AUTH_STRATEGY = {
    "domain": "authentication",
    "focus_areas": [
        "authentication",
        "authorization",
        "session_management",
        "account_lockout"
    ]
}

AUTH_KEYWORDS = [
    "login",
    "logout",
    "password",
    "authenticate",
    "authorization"
]

PAYMENT_STRATEGY = {
    "domain": "payments",
    "focus_areas": [
        "balance_validation",
        "transfer_limits",
        "insufficient_funds",
        "audit_trail"
    ]
}

PAYMENT_KEYWORDS = [
    "payment",
    "transfer",
    "transaction",
    "withdraw",
    "deposit"
]

EVENT_STRATEGY = {
    "domain": "iot_events",
    "focus_areas": [
        "schema_validation",
        "missing_fields",
        "boundary_values",
        "event_ordering",
        "duplicate_events"
    ]
}

EVENT_KEYWORDS = [
    "sensor",
    "device",
    "event",
    "telemetry",
    "temperature",
    "humidity"
]

DOMAINS = {
    "authentication": {
        "keywords": AUTH_KEYWORDS,
        "strategy": AUTH_STRATEGY
    },
    "payments": {
        "keywords": PAYMENT_KEYWORDS,
        "strategy": PAYMENT_STRATEGY
    },
    "event":{
        "keywords": EVENT_KEYWORDS,
        "strategy": EVENT_STRATEGY
    }
}

UNKNOWN_STRATEGY = {
    "domain": "unknown",
    "focus_areas": [
        "general_functionality",
        "validation",
        "error_handling"
    ]
}

def analyze_requirement(requirement: str) -> dict:
    requirement = requirement.lower()

    for domain in DOMAINS.values():
        for keyword in domain["keywords"]:
            if keyword in requirement:
                return deepcopy(domain["strategy"])
    
    # if no valid strategy found
    return deepcopy(UNKNOWN_STRATEGY)
