from playwright.sync_api import sync_playwright

def test_google():
    # Arrange
    with sync_playwright() as sp:
        browser = sp.chromium.launch(headless=False)
        page = browser.new_page()

        # Act
        page.goto("https://www.google.com")

        # Assert
        title = page.title()
        assert "Google" in title, f"Expected 'Google' to be in the page title but got {title}"

        print("PASS: Page title contains Google")

        browser.close()




if __name__ == "__main__":
    test_google()