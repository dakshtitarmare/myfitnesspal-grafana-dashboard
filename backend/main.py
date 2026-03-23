import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .database import Base, engine
    from .routers.uploads import router as uploads_router
except ImportError:
    from database import Base, engine
    from routers.uploads import router as uploads_router

app = FastAPI(
    title="MyFitnessPal CSV Analytics API",
    description="Upload and preprocess MyFitnessPal exports for Grafana dashboards.",
    version="1.0.0",
)

frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3001,http://127.0.0.1:3001,http://localhost:3000",
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


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(uploads_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
