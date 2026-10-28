"""HTTP API. Run: uv run uvicorn app.main:app --reload"""

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

from app.config import settings
from app.pipeline import assess
from app.rate_limit import RateLimiter
from app.schemas import Assessment
from app.store import connection_string

logger = logging.getLogger(__name__)
INDEX_HTML = Path(__file__).parent / "static" / "index.html"

app = FastAPI(
    title="Asset Permissibility Assistant",
    description="Checks whether an asset is permissible in an insurance policy, based on synthetic rules documents.",
)
engine = create_engine(connection_string(), pool_pre_ping=True)
limiter = RateLimiter(settings.rate_limit_per_minute, settings.rate_limit_per_day)


class AssessRequest(BaseModel):
    text: str = Field(
        min_length=1, max_length=10_000, description="Free-text request, e.g. an email from an RM."
    )


# Sync endpoints: FastAPI runs them in a thread pool, and the Anthropic and LlamaIndex clients we use are sync.
@app.post("/assess", response_model=Assessment)
def assess_endpoint(body: AssessRequest, request: Request) -> Assessment:
    # The app is served directly (no proxy in front), so the socket address is the client's IP.
    if not limiter.allow(request.client.host if request.client else "unknown"):
        raise HTTPException(status_code=429, detail="Too many requests, please try again later.")
    try:
        return assess(body.text).assessment
    except Exception as exc:
        logger.exception("Assessment failed")
        raise HTTPException(status_code=502, detail=f"Assessment failed: {type(exc).__name__}") from exc


@app.get("/health")
def health() -> dict:
    # Checks the database (the app cannot work without it) but not the LLM APIs, which would cost money.
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(INDEX_HTML)
