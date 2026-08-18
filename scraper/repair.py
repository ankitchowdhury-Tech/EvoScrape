from playwright.sync_api import sync_playwright
import re

URL = "http://localhost:8000"


def looks_like_price(text):
    """
    Check whether the extracted text looks like a single price.
    """

    text = text.strip()

    # Examples:
    # ₹49,999
    # ₹49999
    # ₹1,299.50

    pattern = r"^₹\s*[\d,]+(?:\.\d{1,2})?$"

    return re.match(pattern, text) is not None


def generate_selector(element):
    """
    Generate a useful CSS selector for an element.
    """

    test_id = element.get_attribute("data-testid")

    if test_id:
        return f'[data-testid="{test_id}"]'

    element_id = element.get_attribute("id")

    if element_id:
        return f"#{element_id}"

    class_name = element.get_attribute("class")

    if class_name:

        classes = class_name.split()

        if classes:
            return "." + ".".join(classes)

    tag = element.evaluate(
        "(el) => el.tagName.toLowerCase()"
    )

    return tag


def find_repair():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL)

        elements = page.locator("span, div").all()

        for element in elements:

            try:

                text = element.inner_text().strip()

                # Ignore parent elements containing multiple pieces of data
                if not looks_like_price(text):
                    continue

                selector = generate_selector(element)

                print("\nCandidate found")
                print("Text:", text)
                print("Generated selector:", selector)

                # Test the selector
                extracted = page.locator(
                    selector
                ).inner_text(timeout=3000).strip()

                if looks_like_price(extracted):

                    print("Extracted:", extracted)
                    print("🟢 REPAIR VALIDATED")

                    browser.close()

                    return selector

            except Exception:
                continue

        browser.close()

        print("\n🔴 No valid repair found.")

        return None


if __name__ == "__main__":

    print("\n----- EvoScrape Automatic Repair -----")

    selector = find_repair()

    if selector:

        print("\nFinal repair selector:", selector)