from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
from validator import validate_selector
from healer import heal_selector





URL = "http://localhost:8000"


def get_real_html():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL)

        page.wait_for_load_state("networkidle")

        html = page.content()

        browser.close()

        return html


def analyze_html(html):

    soup = BeautifulSoup(html, "html.parser")

    candidates = []

    for element in soup.find_all(["span", "div"]):

        text = element.get_text(" ", strip=True)

        if re.fullmatch(
            r"₹\s*[\d,]+(?:\.\d{1,2})?",
            text
        ):

            candidates.append({
                "tag": element.name,
                "text": text,
                "data-testid": element.get("data-testid"),
                "class": element.get("class"),
                "id": element.get("id")
            })

    return candidates


def choose_best_candidate(candidates):

    if not candidates:
        return None

    for candidate in candidates:

        if candidate["data-testid"]:
            return candidate

    return candidates[0]


def create_selector(candidate):

    if candidate["data-testid"]:
        return f'[data-testid="{candidate["data-testid"]}"]'

    if candidate["id"]:
        return f'#{candidate["id"]}'

    if candidate["class"]:
        return "." + ".".join(candidate["class"])

    return candidate["tag"]


if __name__ == "__main__":

    print("================================")
    print("       EVOSCRAPE AI AGENT")
    print("================================")

    print("\n🌐 Inspecting real website...")

    html = get_real_html()

    candidates = analyze_html(html)

    print("\n🔎 Candidates found:")

    for candidate in candidates:
        print(candidate)

    best = choose_best_candidate(candidates)

    if not best:

        print("\n❌ No suitable candidate found.")

    else:

        selector = create_selector(best)

        print("\n🤖 AI Agent Recommendation")

        print("Element :", best["tag"])
        print("Value   :", best["text"])
        print("Selector:", selector)

        print("\n🧪 Validating selector...")

        result = validate_selector(
            selector,
            expected_value=best["text"]
        )

        if result["valid"]:

            print("\n✅ SELECTOR VALID")
            print("Value:", result["value"])

        else:

            print("\n❌ SELECTOR FAILED")
            print("Reason:", result["reason"])

            print("\n🔧 Starting self-healing...")

            new_selector = heal_selector(
                best["text"]
            )

            if new_selector:

                print("\n🧪 Validating healed selector...")

                healed_result = validate_selector(
                    new_selector,
                    expected_value=best["text"]
                )

                if healed_result["valid"]:

                    print("\n❤️ SELF-HEALING SUCCESSFUL")
                    print("Old selector:", selector)
                    print("New selector:", new_selector)

                else:

                    print("\n💥 HEALING FAILED")
                    print("Replacement selector:", new_selector)

            else:

                print("\n💥 No replacement selector found.")