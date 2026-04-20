import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "dev")

BASE_URLS = {
    "dev": "https://the-internet.herokuapp.com",
    "staging": "https://staging.example.com",
    "prod": "https://prod.example.com"
}

def get_base_url():
    return BASE_URLS.get(ENV, BASE_URLS["dev"])