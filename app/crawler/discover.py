import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def discover_pdfs(year: int) -> list[dict]:
    base_url = (
        "https://www.gov.br/inep/pt-br/areas-de-atuacao/"
        "avaliacao-e-exames-educacionais/enade/"
        f"provas-e-gabaritos/{year}"
    )

    response = requests.get(base_url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for link in soup.select('a[href$=".pdf"]'):
        url = urljoin(base_url, link["href"])
        filename = url.split("/")[-1].lower()

        results.append({
            "year": year,
            "url": url,
            "filename": filename
        })

    return results
