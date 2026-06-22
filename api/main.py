from fastapi import FastAPI
from framework.services.validation_service import validate
from framework.services.spec_generation_service import spec_generation_service
from framework.generation.exploratory_generator import generate_exploratory_scenarios

app = FastAPI()

# Define a simple route to check if the API is running
# .get is HTTP method and Path is "/"
@app.get("/")
def root():
    return {"status": "Running"}

# app.post is route definition
@app.post("/validate-tests")
# Function name and param is the api endpoint/coordinator
def validate_tests(payload: dict):
   results = validate(payload)
   return results

# Receive spec and generate automated tests
@app.post("/generate-automated-tests")
def generate_automated_tests(payload: dict):
    results = spec_generation_service(payload)
    return results

# Receive spec and generate exploratory tests
@app.post("/generate-exploratory-tests")
def generate_exploratory_tests(payload: dict):
    results = generate_exploratory_scenarios(payload["requirements"])
    return results