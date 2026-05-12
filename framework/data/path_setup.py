from config.config import (PLANS_DIR, PLANS_DIR_JSON, RESULTS_DIR, RESULTS_JSON_DIR, VALIDATION_LOGS_DIR)

def verify_directories_exist():
    for path in [PLANS_DIR, PLANS_DIR_JSON, RESULTS_DIR, RESULTS_JSON_DIR, VALIDATION_LOGS_DIR]:
        path.mkdir(parents = True, exist_ok = True)