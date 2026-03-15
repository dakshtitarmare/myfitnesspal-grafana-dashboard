import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.uploads import router as uploads_router

app = FastAPI(
    title="MyFitnessPal CSV Analytics API",
    description="Upload and preprocess MyFitnessPal exports for Grafana dashboards.",
    version="1.0.0",
)

frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "*",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(uploads_router)
