from pydantic import BaseSettings

class Settings(BaseSettings):
    INEP_BASE_URL: str = "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enade/provas-e-gabaritos/"
    TMP_DIR: str = "data/tmp"
    STORAGE_DIR: str = "data/storage"
    
class Constants(BaseSettings):
    IGNORE_TERMS: list = ["ampliada", "super", "ledor"]
    ACCEPT_TERMS: list = ["pv", "gb"]
    
settings = Settings()
constants = Constants()