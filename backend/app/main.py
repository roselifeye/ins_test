from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import evaluation

settings = get_settings()

app = FastAPI(title="Inspection Agent API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluation.router, prefix=f"{settings.api_prefix}/evaluation", tags=["evaluation"])


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
