from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="OCR Service", description="Сервис для распознавания документов")

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Go to /docs to use the API"}
