from pathlib import Path
import re

class Settings():
    INEP_BASE_URL: str = "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enade/provas-e-gabaritos/"
    TMP_DIR: str = Path("data/tmp")
    STORAGE_DIR: str = Path("data/storage")
    
    
class Patterns():
    FIND_SEQUENCE_ALTERNATIVES: str = [r'\n\s*A\s+[A-Za-z]', r'(\n|^)\s*A\s+[^\n]+[\.\n]\s*B\s+']
    EXTRACT_ALTERNATIVES: str = r'\b([A-E])\s+(.*?)(?=\s+[A-E]\s+|$)'
    
    FIND_QUESTION: str = r"QUESTÃO\s+\d+",
    FIND_LAST_ALTERNATIVE: str = r"^\s*[Ⓔ⊙●]?\s*E[\s\)]"
    
    
settings = Settings()
patterns = Patterns()