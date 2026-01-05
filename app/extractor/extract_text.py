import subprocess


def extract_texts_pdfs(pdf_path: str) -> str:
    result = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", pdf_path, "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    text = result.stdout.decode("utf-8", errors="ignore")
    return text