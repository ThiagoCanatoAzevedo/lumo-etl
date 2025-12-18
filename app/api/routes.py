# uvicorn app.main:app --reload

from fastapi import APIRouter, HTTPException
from app.crawler.discover import discover_pdfs
from app.crawler.pipeline import run_pipeline
from app.state import etl_stop_event
import os

router = APIRouter()


@router.post("/run/{year}")
def run_etl(year: int):
    result = run_pipeline(year)
    return {
        "message": "ETL executado com sucesso",
        "result": result
    }


@router.post("/stop")
def stop_etl():
    etl_stop_event.set()
    return {"message": "Sinal de parada enviado"}


@router.get("/discover/{year}")
def discover(year: int):
    try:
        items = discover_pdfs(year)
        return {
            "year": year,
            "total_encontrados": len(items),
            "arquivos": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))