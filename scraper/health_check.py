from playwright.sync_api import sync_playwright

URL = "http://localhost:8000"


def check_scraper():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL)

        fields = {
            "name": ".product-name",
            "price": ".product-price",
            "rating": ".product-rating"
        }

        results = {}

        for field, selector in fields.items():

            try:
                value = page.locator(selector).inner_text(timeout=3000)

                results[field] = {
                    "status": "SUCCESS",
                    "value": value
                }

            except Exception:

                results[field] = {
                    "status": "FAILED",
                    "value": None
                }

        browser.close()

        return results


if __name__ == "__main__":

    result = check_scraper()

    print("\n----- EvoScrape Health Check -----\n")

    for field, data in result.items():

        print(field.upper(), ":", data["status"])

        if data["value"]:
            print("Value:", data["value"])

        print()