from fastapi import FastAPI

from .filemanager.router import router as filemanager_router

app = FastAPI(
    title="FastAPI + Docker + DevContainer",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(filemanager_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/", tags=["hello"])
def read_root():
    return {"message": "Hello from FastAPI running in Docker!"}
