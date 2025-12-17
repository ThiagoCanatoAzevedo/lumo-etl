import os
import requests

IGNORAR_TERMOS = [
    "ampliada",
    "super_ampliada",
    "super ampliada",
    "ledor"
]

TERMOS_VALIDOS = [
    "pv",
    "gb"
]

def download_pdf(url: str, path: str) -> bool:
    nome = os.path.basename(url).lower()

    if any(termo in nome for termo in IGNORAR_TERMOS):
        return False

    if not any(termo in nome for termo in TERMOS_VALIDOS):
        return False

    os.makedirs(os.path.dirname(path), exist_ok=True)

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    with open(path, "wb") as f:
        f.write(response.content)

    return True
