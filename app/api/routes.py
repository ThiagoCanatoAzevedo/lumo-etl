from fastapi import APIRouter
from app.crawler.discover import find_all_pdfs

router = APIRouter()

@router.post("/extract/{year}")
def start_etl(year: int):
    pdf_paths = find_all_pdfs(year)
    return {
        "message": "ETL executado com sucesso",
        "pdfs_baixados": pdf_paths
    }
    
    

# uvicorn app.main:app --reload