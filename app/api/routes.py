# uvicorn app.main:app --reload

from fastapi import APIRouter, HTTPException
from app.crawler.discover import discover_pdfs
from app.crawler.pipeline import run_pipeline
from app.state import etl_stop_event


router = APIRouter()

# start etl pipeline
@router.post("/run/{year}")
def run_etl(year: int):
    result = run_pipeline(year)
    return {
        "message": "ETL started successfully",
        "result": result
    }


# stop etl pipeline
@router.post("/stop")
def stop_etl():
    etl_stop_event.set()
    return {"message": "Sent a stop signal"}


# return all pdfs found in determined year
@router.get("/discover/{year}")
def discover(year: int):
    try:
        items = discover_pdfs(year)
        return {
            "year": year,
            "total_founded": len(items),
            "files": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))