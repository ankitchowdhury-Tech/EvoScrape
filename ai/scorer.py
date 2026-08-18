import re


PRICE_PATTERN = re.compile(
    r"₹\s*[\d,]+(?:\.\d{1,2})?"
)


def score_candidate(candidate, expected_value):

    score = 0
    reasons = []

    text = candidate.get("text", "").strip()

    # 1. Exact value match
    if text == expected_value:
        score += 40
        reasons.append("exact value match")

    # 2. Price-like value
    if PRICE_PATTERN.search(text):
        score += 25
        reasons.append("price-like value")

    # 3. Semantic class
    classes = candidate.get("class") or []

    class_text = " ".join(classes).lower()

    if "price" in class_text:
        score += 20
        reasons.append("price-related class")

    # 4. Stable data-testid
    if candidate.get("data-testid"):
        score += 10
        reasons.append("data-testid present")

    # 5. ID
    if candidate.get("id"):
        score += 5
        reasons.append("id present")

    return {
        "score": score,
        "reasons": reasons
    }


def rank_candidates(candidates, expected_value):

    ranked = []

    for candidate in candidates:

        result = score_candidate(
            candidate,
            expected_value
        )

        ranked.append({
            "candidate": candidate,
            "score": result["score"],
            "reasons": result["reasons"]
        })

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked


if __name__ == "__main__":

    candidates = [

        {
            "tag": "div",
            "text": "Gaming Laptop ₹49,999 4.5",
            "data-testid": None,
            "id": None,
            "class": ["product"]
        },

        {
            "tag": "div",
            "text": "₹49,999",
            "data-testid": None,
            "id": None,
            "class": ["product-price"]
        }
    ]

    expected_value = "₹49,999"

    ranked = rank_candidates(
        candidates,
        expected_value
    )

    print("================================")
    print("       EVOSCRAPE SCORER")
    print("================================")

    for item in ranked:

        print("\nCandidate:")
        print(item["candidate"])

        print("Score:", item["score"])

        print(
            "Reasons:",
            ", ".join(item["reasons"])
        )