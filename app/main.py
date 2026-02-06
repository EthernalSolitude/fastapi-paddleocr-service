import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  
from app.api.routes import router


RESULTS_DIR = "static/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

app = FastAPI(title="OCR Service", description="Сервис для распознавания документов")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Go to /docs to use the API"}
