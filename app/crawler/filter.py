IGNORE_TERMS = ["ampliada", "super", "ledor"]
ACCEPT_TERMS = ["pv", "gb"]

def should_process(item: dict) -> bool:
    name = item["filename"]

    if any(term in name for term in IGNORE_TERMS):
        return False

    return any(term in name for term in ACCEPT_TERMS)
