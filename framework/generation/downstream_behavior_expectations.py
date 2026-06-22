# Full flow
# Requirement/Spec string is received
# Loop through EXPECTATION_SCENARIOS searching for KEYWORDS
# If any KEYWORDS match with EXPECTATION_SCENARIOS add that scenarios expectations to a set
# Turn the set into a list and return it


from copy import deepcopy

DOWNSTREAM_BEHAVIOR_EXPECTATIONS = {
    "temperature_threshold_exceeded":[
        "alert_created",
        "notification_sent",
        "dashboard_updated"
    ],
    "sensor_offline":[
        "sensor_marked_offline",
        "notification_sent",
        "dashboard_updated"
    ]
}

TEMPERATURE_KEYWORDS = [
    "temperature",
    "hot",
    "cold"
]

OFFLINE_KEYWORDS = [
    "offline",
    "silent",
    "missing"
]

EXPECTATION_SCENARIOS = {
    "temperature_threshold_exceeded": {
        "keywords": TEMPERATURE_KEYWORDS,
        "expectations": DOWNSTREAM_BEHAVIOR_EXPECTATIONS["temperature_threshold_exceeded"]
    },
    "sensor_offline": {
        "keywords": OFFLINE_KEYWORDS,
        "expectations": DOWNSTREAM_BEHAVIOR_EXPECTATIONS["sensor_offline"]
    }
}

UNKNOWN_EXPECTATION = ["no_downstream_behavior_defined"]


def get_expected_downstream_behaviors(requirement: str) -> list:
    requirement = requirement.lower()

    matches = set()

    for scenario in EXPECTATION_SCENARIOS.values():
        for keyword in scenario["keywords"]:
            if keyword in requirement:
                matches.update(scenario["expectations"])

    if len(matches) > 0:
        return list(matches)
    else:
        return deepcopy(UNKNOWN_EXPECTATION)