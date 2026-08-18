from playwright.sync_api import sync_playwright


URL = "http://localhost:8000"


def validate_selector(selector, expected_value=None):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(URL)
            page.wait_for_load_state("networkidle")

            element = page.locator(selector)

            if element.count() == 0:
                return {
                    "valid": False,
                    "reason": "Selector found no elements"
                }

            text = element.first.inner_text().strip()

            if expected_value is not None and text != expected_value:
                return {
                    "valid": False,
                    "reason": "Element found, but value changed",
                    "actual_value": text,
                    "expected_value": expected_value
                }

            return {
                "valid": True,
                "value": text
            }

        except Exception as error:

            return {
                "valid": False,
                "reason": str(error)
            }

        finally:
            browser.close()


if __name__ == "__main__":

    selector = "#this-selector-does-not-exist"

    print("================================")
    print("      EVOSCRAPE VALIDATOR")
    print("================================")

    print("\n🔎 Testing selector:")
    print(selector)

    result = validate_selector(selector)

    if result["valid"]:

        print("\n✅ SELECTOR VALID")
        print("Value:", result["value"])

    else:

        print("\n❌ SELECTOR FAILED")
        print("Reason:", result["reason"])
