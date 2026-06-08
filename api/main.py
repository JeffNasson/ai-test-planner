from fastapi import FastAPI
from framework.services.validation_service import validate

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

# Receive spec 
@app.post("/generate-tests")
def generate_tests(payload: dict):
    # For now, just return the received payload
    return {"received_spec": payload}