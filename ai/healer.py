from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from .scorer import rank_candidates


URL = "http://localhost:8000"


def find_price_candidates():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(URL)
            page.wait_for_load_state("networkidle")

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            candidates = []

            for element in soup.find_all(["span", "div"]):

                text = element.get_text(" ", strip=True)

                if "₹" in text:

                    candidates.append({
                        "tag": element.name,
                        "text": text,
                        "data-testid": element.get("data-testid"),
                        "id": element.get("id"),
                        "class": element.get("class")
                    })

            return candidates

        finally:
            browser.close()


def create_selector(candidate):

    if candidate["data-testid"]:
        return f'[data-testid="{candidate["data-testid"]}"]'

    if candidate["id"]:
        return f'#{candidate["id"]}'

    if candidate["class"]:
        return "." + ".".join(candidate["class"])

    return candidate["tag"]


def heal_selector(expected_value):

    print("\n🔧 SELF-HEALING ACTIVATED")

    candidates = find_price_candidates()

    if not candidates:

        print("\n❌ No candidates found.")

        return None

    print("\n🔎 Candidates discovered:")

    ranked = rank_candidates(
        candidates,
        expected_value
    )

    for item in ranked:

        print("\nCandidate:")
        print(item["candidate"])

        print("Score:", item["score"])

        print(
            "Reasons:",
            ", ".join(item["reasons"])
        )

    best = ranked[0]

    candidate = best["candidate"]

    selector = create_selector(candidate)

    print("\n🏆 BEST REPLACEMENT")

    print("Element :", candidate["tag"])
    print("Value   :", candidate["text"])
    print("Selector:", selector)
    print("Score   :", best["score"])

    return {
    "selector": selector,
    "score": best["score"],
    "reasons": best["reasons"]
}


if __name__ == "__main__":

    print("================================")
    print("       EVOSCRAPE HEALER")
    print("================================")

    selector = heal_selector("₹49,999")

    if selector:

        print("\n❤️ HEALER READY")
        print("Replacement:", selector)

    else:

        print("\n💥 HEALING FAILED")