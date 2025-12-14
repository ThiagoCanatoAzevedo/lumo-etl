import requests

def download_pdf(url: str, path: str):
    print(f"Baixando PDF: {url}")
    response = requests.get(url)
    response.raise_for_status()

    with open(path, "wb") as f:
        f.write(response.content)
