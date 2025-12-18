from pathlib import Path
import requests, uuid

TMP_DIR = Path("data/tmp")

def download_temp(url: str) -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4()}.pdf"
    path = TMP_DIR / filename

    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()

        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return path
