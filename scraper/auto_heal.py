import json
from repair import find_repair

CONFIG_FILE = "scraper/config.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def auto_heal():

    print("\n🔎 Starting automatic repair...\n")

    # Ask the repair engine to find a working selector
    new_selector = find_repair()

    if not new_selector:
        print("\n❌ Automatic repair failed.")
        return False

    # Load current configuration
    config = load_config()

    old_selector = config["price"]

    # Update the price selector
    config["price"] = new_selector

    save_config(config)

    print("\n🔧 REPAIR APPLIED")
    print("Old selector:", old_selector)
    print("New selector:", new_selector)

    return True


if __name__ == "__main__":

    print("================================")
    print("      EVOSCRAPE AUTO HEAL")
    print("================================")

    auto_heal()