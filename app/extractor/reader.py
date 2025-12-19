import pypdf

def read_pdfs(pdf_path: str) -> str:
    reader = pypdf.PdfReader(pdf_path)

    text_parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)

    return "\n".join(text_parts)
