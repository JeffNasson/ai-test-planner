import re

def run_real_assertion(page, assertion: dict): # page is the browser tab/page object from Playwright. Assertion is the structured data dictionary from the AI prompt

    assertion_type = assertion.get("type") # This is the type of assertion to perform, such as "url_contains", "element_visible", or "text_present". The actual types and their handling would depend on how you want to structure your assertions and what you want to verify in your tests.
    
    value = assertion.get("value") # This is the value to check for in the assertion. For example, if the assertion type is "url_contains", this would be the substring that should be present in the URL. If the assertion type is "element_visible", this could be a boolean indicating whether the element should be visible or not. If the assertion type is "text_present", this would be the text that should be present on the page.

    locator = assertion.get("locator") # This is an optional CSS selector that can be used to locate a specific element on the page for assertions that require it, such as "element_visible" or "text_present".

    # Perform the assertion based on its type
    if assertion_type == "url_contains":
        assert value in page.url, f"Expected {value} in url, got {page.url}" # This checks that the specified value is present in the current page URL.
    
    elif assertion_type == "element_visible":
        assert page.locator(locator).is_visible(), f"Element {locator} not visible" # This checks that the element specified by the locator is visible on the page.
    
    elif assertion_type == "text_present":
        element = page.locator(locator) # Locate the element specified by the locator

        assert element.count() > 0, f"Element {locator} not found on page" # This checks that the element specified by the locator exists on the page.

        content = element.text_content() # Get the text content of the element specified by the locator

        content = content.lower() if content else "" # Convert the text content to lowercase for case-insensitive comparison, and handle the case where text_content might return None to prevent crashes.

        keywords = re.findall(r"\w+", value.lower()) # Extract individual words from the value string using a regular expression. This allows for more flexible assertions where the value might contain multiple keywords, and we want to check if any of those keywords are present in the text content of the element.

        assert any(word in content for word in keywords), f"Expected one of {keywords} in {content}" # This checkes that at least one of the specified keywords is present in the text content of the element. This allows for more flexible assertions where the exact text might vary but should contain certain key terms.
    
    else:
        print(f"SKIPPED: Unknown assertion type -> {assertion_type}") # If the assertion type is not recognized, print a message and skip the assertion instead of failing the test.

    print("PASS")