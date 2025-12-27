from pathlib import Path


class Settings():
    INEP_BASE_URL: str = "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enade/provas-e-gabaritos/"
    TMP_DIR: str = Path("data/tmp")
    STORAGE_DIR: str = Path("data/storage")
    

class Constants():
    IGNORE_TERMS: list = ["ampliada", "super", "ledor"]
    ACCEPT_TERMS: list = ["pv", "gb"]
    
settings = Settings()
constants = Constants()