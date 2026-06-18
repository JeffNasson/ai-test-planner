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


PAYMENT_KEYWORDS = [
    "payment",
    "transfer",
    "transaction",
    "withdraw",
    "deposit"
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

DOMAINS = {
    "authentication": {
        "keywords": AUTH_KEYWORDS,
        "strategy": AUTH_STRATEGY
    },
    "payments": {
        "keywords": PAYMENT_KEYWORDS,
        "strategy": PAYMENT_STRATEGY
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
