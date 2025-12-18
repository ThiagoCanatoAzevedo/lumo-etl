from pathlib import Path
import requests
from urllib.parse import urlparse, unquote


TMP_DIR = Path("data/tmp")

def download_pdfs(url: str) -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    
    parsed_url = urlparse(url)
    filename = unquote(Path(parsed_url.path).name)
    
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    path = TMP_DIR / filename
    
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=10240):
                if chunk:
                    f.write(chunk)
    return path