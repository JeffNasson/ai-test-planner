import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

ENV = os.getenv("ENV", "dev")

# ENV URLs
BASE_URLS = {
    "dev": "https://the-internet.herokuapp.com",
    "staging": "https://staging.example.com",
    "prod": "https://prod.example.com"
}

# Base environment
def get_base_url():
    return BASE_URLS.get(ENV, BASE_URLS["dev"])

# File paths for logs
BASE_DIR = Path(__file__).resolve().parent.parent

PLANS_DIR = BASE_DIR / "tests" / "test_cases_txt"
PLANS_DIR_JSON = BASE_DIR / "tests" / "test_cases_json"

RESULTS_DIR = BASE_DIR / "results" / "test_results_txt"
RESULTS_JSON_DIR = BASE_DIR / "results" / "test_results_json"

VALIDATION_LOGS_DIR = BASE_DIR / "validation_logs"
