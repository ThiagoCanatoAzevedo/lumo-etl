# uvicorn app.main:app --reload

from fastapi import APIRouter, HTTPException
from app.crawler.discover import discover_pdfs
from app.pipeline import run_pipeline
from app.state import etl_stop_event

router = APIRouter()


# start complete enade etl
@router.post("/start/{year}")
def run_etl(year: int):
    try:
        if etl_stop_event.is_set():
            etl_stop_event.clear()

        result = run_pipeline(year)

        return {
            "status": "completed" if not result["stopped"] else "stopped",
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# stop all etl - using Event
@router.post("/stop")
def stop_etl():
    etl_stop_event.set()
    return {"message": "Stop signal sent"}


# discover pdfs downloadable - only for analysis
@router.get("/discover/{year}")
def discover(year: int):
    try:
        items = discover_pdfs(year)
        return {
            "year": year,
            "total_found": len(items),
            "files": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
