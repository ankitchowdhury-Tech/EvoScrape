import re


PRICE_PATTERN = re.compile(
    r"₹\s*[\d,]+(?:\.\d{1,2})?"
)


def selector_quality_score(candidate):
    """
    Estimate how reliable the generated CSS selector is.
    Higher score = more specific/stable selector.
    """

    score = 0
    reasons = []

    # data-testid is usually highly stable
    if candidate.get("data-testid"):
        score += 15
        reasons.append("stable data-testid selector")

    # ID is usually highly specific
    elif candidate.get("id"):
        score += 12
        reasons.append("specific id selector")

    # Classes provide useful structural information
    elif candidate.get("class"):

        classes = candidate.get("class") or []

        if len(classes) >= 2:
            score += 10
            reasons.append("multi-class selector")

        elif len(classes) == 1:
            score += 6
            reasons.append("class-based selector")

    # Tag-only selectors are weak
    else:
        score += 1
        reasons.append("generic tag selector")

    # Semantic price-related class improves selector quality
    classes = candidate.get("class") or []
    class_text = " ".join(classes).lower()

    if any(
        keyword in class_text
        for keyword in [
            "price",
            "cost",
            "amount",
            "mrp",
            "sale",
            "offer"
        ]
    ):
        score += 5
        reasons.append("semantic price selector")

    return score, reasons


def score_candidate(candidate, expected_value):

    score = 0
    reasons = []

    text = candidate.get("text", "").strip()

    classes = candidate.get("class") or []
    class_text = " ".join(classes).lower()

    # -----------------------------------------
    # 1. Exact value match
    # -----------------------------------------

    if text == expected_value:

        score += 40

        reasons.append(
            "exact value match"
        )

    # -----------------------------------------
    # 2. Price-like value
    # -----------------------------------------

    if PRICE_PATTERN.fullmatch(text):

        score += 25

        reasons.append(
            "price-like value"
        )

    elif PRICE_PATTERN.search(text):

        score += 10

        reasons.append(
            "contains price value"
        )

    # -----------------------------------------
    # 3. Semantic class detection
    # -----------------------------------------

    price_keywords = [
        "price",
        "cost",
        "amount",
        "mrp",
        "sale",
        "discount",
        "offer"
    ]

    matched_keywords = [
        keyword
        for keyword in price_keywords
        if keyword in class_text
    ]

    if matched_keywords:

        score += 20

        reasons.append(
            "price-related class"
        )

    # -----------------------------------------
    # 4. Stable data-testid
    # -----------------------------------------

    if candidate.get("data-testid"):

        score += 10

        reasons.append(
            "data-testid present"
        )

    # -----------------------------------------
    # 5. ID
    # -----------------------------------------

    if candidate.get("id"):

        score += 5

        reasons.append(
            "id present"
        )

    # -----------------------------------------
    # 6. Focused element
    # -----------------------------------------

    if len(text) <= 30:

        score += 5

        reasons.append(
            "focused element"
        )

    # -----------------------------------------
    # 7. Semantic HTML
    # -----------------------------------------

    if candidate.get("tag") == "span":

        score += 3

        reasons.append(
            "semantic inline element"
        )

    # -----------------------------------------
    # 8. Generic container penalty
    # -----------------------------------------

    generic_classes = [
        "container",
        "wrapper",
        "content",
        "item",
        "box",
        "row",
        "column"
    ]

    if any(
        generic in class_text
        for generic in generic_classes
    ):

        score -= 5

        reasons.append(
            "generic container penalty"
        )

    # -----------------------------------------
    # 9. Context-rich classes
    # -----------------------------------------

    if len(classes) >= 2:

        score += 2

        reasons.append(
            "context-rich class attributes"
        )

    # -----------------------------------------
    # 10. SELECTOR QUALITY
    # -----------------------------------------

    quality_score, quality_reasons = (
        selector_quality_score(candidate)
    )

    score += quality_score

    reasons.extend(
        quality_reasons
    )

    return {
        "score": score,
        "reasons": reasons,
        "selector_quality": quality_score
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
            "reasons": result["reasons"],
            "selector_quality": result["selector_quality"]
        })

    # Highest overall score first
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
            "class": ["price", "product-price"]
        },

        {
            "tag": "span",
            "text": "₹49,999",
            "data-testid": "price",
            "id": None,
            "class": ["price", "current"]
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
            "Selector Quality:",
            item["selector_quality"]
        )

        print(
            "Reasons:",
            ", ".join(item["reasons"])
        )