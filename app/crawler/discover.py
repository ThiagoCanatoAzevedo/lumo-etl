import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.crawler.downloader import download_pdf

BASE_URL = "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enade/provas-e-gabaritos/2025"
DOWNLOAD_DIR = "data/pdfs"

def find_first_pdf():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue

        full_url = urljoin(BASE_URL, href)

        if full_url.lower().endswith(".pdf"):
            filename = full_url.split("/")[-1]
            file_path = os.path.join(DOWNLOAD_DIR, filename)

            download_pdf(full_url, file_path)
            return file_path

    return "Nenhum PDF encontrado"
