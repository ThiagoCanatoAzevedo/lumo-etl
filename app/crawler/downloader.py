from pathlib import Path
from urllib.parse import urlparse, unquote
from app.core.settings import settings
import requests


def download_pdfs(url: str) -> Path:
    settings.TMP_DIR.mkdir(parents=True, exist_ok=True)
    
    parsed_url = urlparse(url)
    filename = unquote(Path(parsed_url.path).name)
    
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    path = settings.TMP_DIR / filename
    
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=10240):
                if chunk:
                    f.write(chunk)
    return path