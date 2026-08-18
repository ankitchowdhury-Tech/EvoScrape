import json
import os

from .healer import heal_selector
from .validator import validate_selector


URL = "http://localhost:8000"

CONFIG_FILE = "config/selectors.json"
LOG_FILE = "config/healing_log.json"


def save_selector(selector):

    os.makedirs("config", exist_ok=True)

    data = {
        "price": selector
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n💾 Selector saved!")
    print("File:", CONFIG_FILE)


def load_selector():

    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    return data.get("price")


def log_healing(
    old_selector,
    new_selector,
    expected_value,
    score,
    reasons
):

    os.makedirs("config", exist_ok=True)

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r", encoding="utf-8") as file:

            logs = json.load(file)

    else:

        logs = []

    logs.append({
        "field": "price",
        "old_selector": old_selector,
        "new_selector": new_selector,
        "old_value": expected_value,
        "new_value": expected_value,
        "confidence": score / 100,
        "reasons": reasons,
        "status": "healed"
    })

    with open(LOG_FILE, "w", encoding="utf-8") as file:

        json.dump(
            logs,
            file,
            indent=4,
            ensure_ascii=False
        )


def auto_heal(expected_value):

    old_selector = load_selector()

    if not old_selector:

        print("\n⚠️ No saved selector found.")

        return None

    print("\n🔎 Checking saved selector:")
    print(old_selector)

    result = validate_selector(
        old_selector,
        expected_value=expected_value
    )

    if result["valid"]:

        print("\n✅ Selector is working!")
        print("Value:", result["value"])

        return old_selector

    print("\n❌ Selector failed.")
    print("Reason:", result["reason"])

    print("\n🔧 AUTO-HEAL ACTIVATED")

    heal_result = heal_selector(expected_value)

    if not heal_result:

        print("\n🛑 Auto-Heal could not find a replacement.")

        return None

    new_selector = heal_result["selector"]
    score = heal_result["score"]
    reasons = heal_result["reasons"]

    print("\n🧪 Validating replacement selector...")

    healed_result = validate_selector(
        new_selector,
        expected_value=expected_value
    )

    if healed_result["valid"]:

        print("\n❤️ AUTO-HEAL SUCCESSFUL")

        print("Old:", old_selector)
        print("New:", new_selector)

        print("Score:", score)

        print(
            "Reasons:",
            ", ".join(reasons)
        )

        save_selector(new_selector)

        log_healing(
            old_selector,
            new_selector,
            expected_value,
            score,
            reasons
        )

        print("\n📊 Healing report saved!")
        print("File:", LOG_FILE)

        return new_selector

    print("\n❌ Replacement selector failed validation.")

    return None


if __name__ == "__main__":

    print("================================")
    print("       EVOSCRAPE AUTO-HEAL")
    print("================================")

    expected_value = "₹49,999"

    selector = auto_heal(expected_value)

    if selector:

        print("\n🚀 Scraper can continue using:")
        print(selector)

    else:

        print("\n🛑 Scraper could not recover.")
