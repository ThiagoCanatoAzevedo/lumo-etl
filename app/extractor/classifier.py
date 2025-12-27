from app.core.settings import constants


def classify_pdfs(pdf_path: str) -> str:
    name = pdf_path.lower()
    return "prova" if constants.ACCEPT_TERMS[0] in name else "gabarito"