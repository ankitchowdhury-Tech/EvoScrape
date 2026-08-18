import json
import os
import shutil
import time


WEBSITE = "website/index.html"
BACKUP = "website/index_backup.html"
CONFIG = "config/selectors.json"


def read_selector():

    if not os.path.exists(CONFIG):
        return None

    with open(CONFIG, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("price")


def show_status():

    selector = read_selector()

    print("\n================================")
    print("       EVOSCRAPE DEMO")
    print("================================")

    print("\n📋 Saved selector:")

    if selector:
        print(selector)
    else:
        print("None")


def restore_original():

    shutil.copy2(BACKUP, WEBSITE)

    print("\n🔄 Original website restored.")


def simulate_website_change():

    with open(WEBSITE, "r", encoding="utf-8") as file:
        html = file.read()

    old = """<span data-testid="price">
    ₹49,999
</span>"""

    new = """<div class="product-price">
    ₹49,999
</div>"""

    if old not in html:
        print("\n⚠️ Original price structure not found.")
        return False

    html = html.replace(old, new)

    with open(WEBSITE, "w", encoding="utf-8") as file:
        file.write(html)

    print("\n⚠️ WEBSITE CHANGE SIMULATED")
    print("Old: [data-testid=\"price\"]")
    print("New: .product-price")

    return True


if __name__ == "__main__":

    print("================================")
    print("     EVOSCRAPE DEMO TEST")
    print("================================")

    print("\n1️⃣ Restoring original website...")

    restore_original()

    show_status()

    print("\n2️⃣ Simulating website redesign...")

    if simulate_website_change():

        print("\n3️⃣ Website is now changed.")

        print("\nRun the following command:")
        print("python .\\ai\\auto_heal.py")
