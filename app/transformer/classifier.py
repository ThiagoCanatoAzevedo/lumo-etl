from app.transformer.pdf_processor import get_metadata_pdf


def classify_pdfs(pdf_path: str) -> str:
    dict_metadata_pdf = get_metadata_pdf(pdf_path)
    return "exam" if dict_metadata_pdf.get('amount_pages') > 2 else "solution"