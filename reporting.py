from datetime import datetime
import json
import os

RESULTS_DIR = "test_results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

RESULTS_JSON_DIR = "test_results_json"
if not os.path.exists(RESULTS_JSON_DIR):
    os.makedirs(RESULTS_JSON_DIR)

def generate_report(results):
    # Calculate metrics
    total = len(results)
    passed = sum(1 for status, _ in results if status == "PASS") # Add 1 to the count for any (_) test case in results where the status is "PASS".
    failed = sum(1 for status, _ in results if status == "FAIL") # Add 1 to the count for any (_) test case in results where the status is "FAIL".
    errors = sum(1 for status, _ in results if status == "ERROR") # Add 1 to the count for any (_) test case in results where the status is "ERROR".

    pass_rate = (passed/total)*100 if total > 0 else 0 # Calculate pass rate as a percentage. If total is 0, set pass_rate to 0
    
    print("\n=== TEST SUMMARY ===\n")
    for status, title in results:
        print(f"{status}: {title}")
    
    print("\n--- METRICS ---")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"Pass Rate: {pass_rate:.2f}%")

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
    print(f"\nResults save to {filename}")

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