import json

from playwright.sync_api import sync_playwright


URL = "http://localhost:8000"
CONFIG_FILE = "config/selectors.json"


def load_price_selector():

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["price"]


def scrape_product():

    price_selector = load_price_selector()

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        try:

            page.goto(URL)
            page.wait_for_load_state("networkidle")

            product_name = page.locator(
                ".product-name"
            ).inner_text()

            price = page.locator(
                price_selector
            ).inner_text()

            rating = page.locator(
                ".product-rating"
            ).inner_text()

            return {
                "product": product_name.strip(),
                "price": price.strip(),
                "rating": rating.strip(),
                "selector": price_selector
            }

        finally:

            browser.close()


if __name__ == "__main__":

    print("================================")
    print("       EVOSCRAPE SCRAPER")
    print("================================")

    data = scrape_product()

    print("\n📦 PRODUCT DATA")

    print("Product :", data["product"])
    print("Price   :", data["price"])
    print("Rating  :", data["rating"])

    print("\n🔎 Price selector:")
    print(data["selector"])

    print("\n✅ EXTRACTION SUCCESSFUL")
