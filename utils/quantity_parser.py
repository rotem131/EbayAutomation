import re

def get_number_quantity(text: str) -> int | None:
    clean_text = " ".join(text.split()).lower()

    match = re.search(r"(\d+)\s*available", clean_text)
    if match:
        return int(match.group(1))

    if clean_text.startswith("last one"):
        return 1

    return None