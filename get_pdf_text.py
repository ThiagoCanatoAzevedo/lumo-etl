import subprocess


def read_pdfs(pdf_path: str) -> str:
    result = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", pdf_path, "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    text = result.stdout.decode("utf-8", errors="ignore")
    return text

read_pdfs(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\questoes_pdfs\questão_28.pdf")