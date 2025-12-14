from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Lumo ETL")

app.include_router(router, prefix="/etl")

@app.get("/")
def healthcheck():
    return {"status": "ok"}
