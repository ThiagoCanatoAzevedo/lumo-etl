import pypdf


def is_prova_from_name(filename: str) -> bool:
    name = filename.lower()
    return "pv" in name and "gb" not in name


def is_gabarito_from_name(filename: str) -> bool:
    return "gb" in filename.lower()


def is_prova_from_content(pdf_path: str) -> bool:
    reader = pypdf.PdfReader(pdf_path)
    first_page = reader.pages[0].extract_text().lower()

    if "gabarito" in first_page:
        return False

    if "caderno de prova" in first_page or "questão" in first_page:
        return True

    return False


def classify_pdf(pdf_path: str) -> str:
    """Retorna: 'prova' | 'gabarito' | 'unknown'"""
    name = pdf_path.lower()

    if is_prova_from_name(name):
        return "prova"
    if is_gabarito_from_name(name):
        return "gabarito"

    # fallback conteúdo
    return "prova" if is_prova_from_content(pdf_path) else "gabarito"
