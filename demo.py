import json
import os
import subprocess
import sys


VERSION_FILE = "website/version.txt"
CONFIG_FILE = "config/selectors.json"


TESTS = [
    ("1", ".price-new"),
    ("2", ".price-updated"),
    ("3", ".product-cost"),
    ("4", ".price-final"),
]


def set_version(version):

    with open(VERSION_FILE, "w", encoding="utf-8") as file:
        file.write(version)


def set_selector(selector):

    os.makedirs("config", exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"price": selector},
            file,
            indent=4
        )


def get_selector():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data["price"]


def run_evoscrape():

    env = os.environ.copy()

    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    result = subprocess.run(
        [sys.executable, "run.py"],
        env=env
    )

    return result.returncode


def selector_matches(expected, actual):

    # Exact match
    if actual == expected:
        return True

    # EvoScrape may generate a more specific selector
    # such as .price.price-updated
    if actual == ".price" + expected:
        return True

    return False


def main():

    print("================================")
    print("     EVOSCRAPE DEMO TEST")
    print("================================")

    # Start with original website
    set_version("1")
    set_selector(".price-new")

    for version, website_selector in TESTS:

        print("\n================================")
        print(f"TEST {version}")
        print("================================")

        print(
            "Website selector :",
            website_selector
        )

        print(
            "Saved selector   :",
            get_selector()
        )

        return_code = run_evoscrape()

        if return_code != 0:

            print(
                f"\n❌ TEST {version} FAILED"
            )

            return

        # Read selector after EvoScrape
        healed_selector = get_selector()

        print(
            "\nCurrent saved selector:",
            healed_selector
        )

        # Test 1
        if version == "1":

            if healed_selector == ".price-new":

                print(
                    "✅ ORIGINAL SELECTOR WORKING"
                )

            else:

                print(
                    "❌ TEST 1 SELECTOR CHECK FAILED"
                )

                print(
                    "Expected: .price-new"
                )

                print(
                    "Found   :",
                    healed_selector
                )

                return

        # Tests 2, 3 and 4
        else:

            if selector_matches(
                website_selector,
                healed_selector
            ):

                print(
                    "✅ AUTO-HEAL VERIFIED"
                )

            else:

                print(
                    "❌ HEALING VERIFICATION FAILED"
                )

                print(
                    "Expected:",
                    website_selector
                )

                print(
                    "Found   :",
                    healed_selector
                )

                return

        # Move to next website redesign
        if version != "4":

            next_version = str(
                int(version) + 1
            )

            set_version(next_version)

    print("\n================================")
    print("       DEMO COMPLETE")
    print("================================")

    print(
        "\n🏆 ALL TESTS PASSED"
    )

    print(
        "✅ EvoScrape survived 3 website redesigns."
    )

    print(
        "✅ Selectors were automatically repaired."
    )

    print(
        "✅ Product extraction remained successful."
    )


if __name__ == "__main__":
    main()