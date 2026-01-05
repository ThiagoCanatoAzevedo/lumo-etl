from pathlib import Path
import re

class Settings():
    INEP_BASE_URL: str = "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enade/provas-e-gabaritos/"
    TMP_DIR: str = Path("data/tmp")
    STORAGE_DIR: str = Path("data/storage")
    

class Constants():
    IGNORE_TERMS: list = ["ampliada", "super", "ledor"]
    ACCEPT_TERMS: list = ["pv", "gb"]
    
class Patterns():
    QUESTION: str = re.compile(r"QUESTÃO\s+\d+", re.IGNORECASE)
    LAST_ALTERNATIVE: str = re.compile(r"^\s*[Ⓔ⊙●]?\s*E[\s\)]", re.MULTILINE)
    DISCURSIVE_QUESTION: str = re.compile(r"(QUESTÃO\s+DISCURSIVA\s+\d+)", re.IGNORECASE)
    # DISCURSIVA_REGEX = re.compile(r"(elabore|redija|discorra|texto dissertativo|resposta discursiva|padrão de resposta)", re.IGNORECASE) -- possible one
    PERCEPTION_QUESTION: str = re.compile(r"questionário\s+de\s+percepção", re.IGNORECASE)
    
    
settings = Settings()
constants = Constants()
patterns = Patterns()