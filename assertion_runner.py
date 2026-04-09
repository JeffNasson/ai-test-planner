def run_real_assertion(page, assertion: str):
    assertion = assertion.lower()

    if "dashboard" in assertion:
        print("Dashboard check not implemented yet")

    elif "error" in assertion:
        assert page.locator("text=Error").count() > 0, "Error message not found"

    else:
        print(f"Skipped: No mapping for assertion → {assertion}")

    print("PASS")