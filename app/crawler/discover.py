from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.crawler.downloader import download_pdf
from typing import List
import os, requests

def find_all_pdfs(year: int) -> List[str]:
    base_url = (
        "https://www.gov.br/inep/pt-br/areas-de-atuacao/"
        "avaliacao-e-exames-educacionais/enade/"
        f"provas-e-gabaritos/{year}"
    )

    DOWNLOAD_DIR = f"data/pdfs/{year}"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    response = requests.get(base_url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    downloaded_files = []

    for link in soup.select('a[href$=".pdf"]'):
        full_url = urljoin(base_url, link["href"])
        filename = full_url.split("/")[-1]
        file_path = os.path.join(DOWNLOAD_DIR, filename)

        download_pdf(full_url, file_path)
        downloaded_files.append(file_path)

    return downloaded_files