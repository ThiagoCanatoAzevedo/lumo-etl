import subprocess
from typing import Optional


def extract_texts_pdfs(pdf_path: str, page: Optional[int] = None) -> str:
    command = ["pdftotext", "-enc", "UTF-8"]

    if page is not None:
        command.extend(["-f", str(page), "-l", str(page)])

    command.extend([pdf_path, "-"])

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    return result.stdout.decode("utf-8", errors="ignore")
