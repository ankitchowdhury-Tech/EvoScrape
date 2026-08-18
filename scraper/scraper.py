import json
from playwright.sync_api import sync_playwright

URL = "http://localhost:8000"
CONFIG_FILE = "scraper/config.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def scrape_product():

    config = load_config()

    print("Using selectors:")
    print("Name   :", config["name"])
    print("Price  :", config["price"])
    print("Rating :", config["rating"])

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL)

        name = page.locator(config["name"]).inner_text()
        price = page.locator(config["price"]).inner_text()
        rating = page.locator(config["rating"]).inner_text()

        browser.close()

        return {
            "name": name,
            "price": price,
            "rating": rating
        }


if __name__ == "__main__":

    product = scrape_product()

    print("\n----- EvoScrape Result -----")
    print("Product :", product["name"])
    print("Price   :", product["price"])
    print("Rating  :", product["rating"])
    