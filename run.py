from ai.auto_heal import auto_heal
from ai.scraper import scrape_product


EXPECTED_PRICE = chr(8377) + "49,999"


def main():

    print("================================")
    print("        EVOSCRAPE AI")
    print("================================")

    print("\n🔧 Checking scraper health...")

    selector = auto_heal(EXPECTED_PRICE)

    if not selector:

        print("\n🛑 Scraper could not recover.")

        return

    print("\n🚀 Starting extraction...")

    data = scrape_product()

    print("\n================================")
    print("       EVOSCRAPE RESULT")
    print("================================")

    print("\n📦 Product :", data["product"])
    print("💰 Price   :", data["price"])
    print("⭐ Rating  :", data["rating"])

    print("\n🔎 Selector :", data["selector"])

    print("\n✅ SCRAPING COMPLETE")


if __name__ == "__main__":
    main()