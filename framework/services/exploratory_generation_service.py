from framework.generation.exploratory_generator import generate_exploratory_scenarios
from framework.services.validation_service import validate
from framework.execution.test_executor import execute_tests
from framework.reporting.reporting import generate_report

def exploratory_generation_service(payload: dict):
   
    requirements = payload["requirements"]

    exploratory_tests = generate_exploratory_scenarios(requirements)

    validation_results = validate(exploratory_tests)

    execution_results = execute_tests(exploratory_tests["test_cases"])

    generate_report(execution_results)

    return {
        "test_cases": exploratory_tests["test_cases"],
        "validation_results": validation_results,
        "execution_results": execution_results
    }