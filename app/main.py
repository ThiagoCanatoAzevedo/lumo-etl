from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Lumo ETL")

app.include_router(router, prefix="/lumo/enade-etl")

@app.get("/")
def healthcheck():
    return {"status": "ok"}
