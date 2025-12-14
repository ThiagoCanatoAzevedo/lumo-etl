from fastapi import APIRouter
from app.crawler.discover import find_first_pdf

router = APIRouter()

@router.post("/start")
def start_etl():
    pdf_path = find_first_pdf()
    return {
        "message": "ETL executado com sucesso",
        "pdf_baixado": pdf_path
    }
