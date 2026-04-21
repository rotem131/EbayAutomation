import re


def extract_prices(price_texts: list[str]) -> list[float]:
    prices: list[float] = []

    for text in price_texts:
        price = extract_price(text)
        if price is not None:
            prices.append(price)
    return prices


def extract_price(price_text: str) -> float | None:
    if not price_text:
        return None

    cleaned_text = price_text.replace(",", "")
    match = re.search(r"\d+(?:\.\d+)?", cleaned_text)

    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None
