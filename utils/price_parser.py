import re


def extract_prices(price_texts: list[str]) -> list[float]:
    prices: list[float] = []

    for text in price_texts:
        cleaned_text = text.replace(",", "")
        matches = re.findall(r"\d+(?:\.\d+)?", cleaned_text)

        for match in matches:
            try:
                prices.append(float(match))
            except ValueError:
                continue

    return prices