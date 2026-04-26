from datetime import datetime
import json
import os


RESULTS_DIR = "test_results"
os.makedirs(RESULTS_DIR, exist_ok=True) # Create the txt results directory if it doesn't exist

RESULTS_JSON_DIR = "test_results_json"
os.makedirs(RESULTS_JSON_DIR, exist_ok=True) # Create the JSON results directory if it doesn't exist

LOG_DIR = "validation_logs"
os.makedirs(LOG_DIR, exist_ok=True) # Create the validation logs directory if it doesn't exist

def generate_report(results):
    # Calculate metrics
    total = len(results)
    passed = sum(1 for status, _ in results if status == "PASS") # Add 1 to the count for any (_) test case in results where the status is "PASS".
    failed = sum(1 for status, _ in results if status == "FAIL") # Add 1 to the count for any (_) test case in results where the status is "FAIL".
    errors = sum(1 for status, _ in results if status == "ERROR") # Add 1 to the count for any (_) test case in results where the status is "ERROR".

    pass_rate = (passed/total)*100 if total > 0 else 0 # Calculate pass rate as a percentage. If total is 0, set pass_rate to 0
    
    print("\n=== TEST SUMMARY ===\n")
    for status, title in results:
        print(f"{status}: {title}") # Local readability of test results.

        # CI Reporting
        if status == "PASS":
            print(f"::notice tile=PASS::{title}") # GitHub Actions annotation for passed test case
        elif status == "FAIL":
            print(f"::error title=FAIL::{title}") # GitHub Actions annotation for failed test case
        elif status == "ERROR":
            print(f"::error title=ERROR::{title}") # GitHub Actions annotation for errored test case


    print("\n--- METRICS ---")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"Pass Rate: {pass_rate:.2f}%")

    if failed > 0 or errors > 0: 
        exit(1) # Adds a non-zero count of failed or errored test cases to trigger a failure in CI pipeline

    # Save results to txt file
    filename = os.path.join(RESULTS_DIR, f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt") 

    with open(filename,"w") as f:
        f.write("=== TEST RESULTS ===\n\n")

        for status, title in results:
            f.write(f"{status}: {title}\n")

        f.write("\n--- METRICS ---\n")
        f.write(f"Total: {total}\n")
        f.write(f"Passed: {passed}\n")
        f.write(f"Failed: {failed}\n")
        f.write(f"Errors: {errors}\n")
        f.write(f"Pass Rate: {pass_rate:.2f}%\n")
    print(f"\nResults saved to {filename}")

    # Save results file to JSON format for easier parsing in an enterprise application. This allows for integration with other tools, such as dashboards or test management systems, that can consume JSON data.
    base_name = os.path.basename(filename).replace(".txt",".json")
    json_filename = os.path.join(RESULTS_JSON_DIR, base_name)

    data = {
        "results": [
            {
                "status": status,
                "title": title
            }
            for status, title in results
        ],
        "metrics":{
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": pass_rate
        }
    }
    with open(json_filename,"w") as f:
        json.dump(data, f, indent=4)
    print(f"Results saved to {json_filename}")


def log_validation_results(validation_results):
    filename = os.path.join(LOG_DIR, f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    data = {
        "timestamp": datetime.now().isoformat(),
        "results": validation_results
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Validation log saved to {filename}")