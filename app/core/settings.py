from pathlib import Path
import re

class Settings():
    INEP_BASE_URL: str = "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enade/provas-e-gabaritos/"
    TMP_DIR: str = Path("data/tmp")
    
    
class Patterns():
    FIND_ALTERNATIVES: str = r"(?is)\bA\b.*?\bB\b.*?\bC\b.*?\bD\b.*?\bE\b|QUESTÃO\s+\d+"    
    FIND_QUESTION: str = r"QUESTÃO\s+\d+"
    # FIND_LAST_ALTERNATIVE: str = r"^\s*[Ⓔ⊙●]?\s*E[\s\)]"
    FIND_TRASH_TEXT: str = r"(?i)QUESTION[AÁ]RIO\s+DE\s+PERCEP[CÇ][AÃ]O|INSTRUÇÕES|QUESTÕES DISCURSIVAS"
    
    
    
settings = Settings()
patterns = Patterns()