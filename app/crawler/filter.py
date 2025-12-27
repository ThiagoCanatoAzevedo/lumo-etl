from app.core.settings import constants


def filter_downloadable_pdfs(item: dict) -> bool:
    name = item["filename"]
    if any(term in name for term in constants.IGNORE_TERMS):
        return False
    return any(term in name for term in constants.ACCEPT_TERMS)