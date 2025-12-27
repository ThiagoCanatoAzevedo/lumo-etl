def is_prova_from_name(filename: str) -> bool:
    name = filename.lower()
    return "pv" in name and "gb" not in name

def is_gabarito_from_name(filename: str) -> bool:
    return "gb" in filename.lower()

def classify_pdf(pdf_path: str) -> str:
    name = pdf_path.lower()

    if is_prova_from_name(name):
        return "prova"
    if is_gabarito_from_name(name):
        return "gabarito"

    return "prova"