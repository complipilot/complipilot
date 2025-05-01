from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.db import engine                    # Database engine
from app.auth.routes import router as auth 

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth.security import decode_token  # <-- new import


# ---------------------------------------------------------------------------
# Lifespan handler -----------------------------------------------------------
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code in this block runs once on startup, and again on shutdown.

    • Creates all tables from SQLModel metadata (idempotent).
    • Put other one-time startup / teardown tasks here.
    """
    SQLModel.metadata.create_all(bind=engine)
    yield
    # --- shutdown logic (if any) -------------------------------------------


# ---------------------------------------------------------------------------
# FastAPI application instance ----------------------------------------------
# ---------------------------------------------------------------------------

app = FastAPI(
    title="CompliPilot API",
    version="0.1.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Register routers -----------------------------------------------------------
# ---------------------------------------------------------------------------

app.include_router(auth, prefix="/auth")      # /auth/register, /auth/login …

# JWT-backed “who am I” endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.get("/me", summary="Get current user", tags=["auth"])
async def read_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return {"email": payload["sub"]}

# TODO: from app.api.v1.router import api_router as v1_router
# app.include_router(v1_router, prefix="/api/v1")

# ---------------------------------------------------------------------------
# Utility / sanity-check endpoints ------------------------------------------
# ---------------------------------------------------------------------------

@app.get("/health", tags=["utility"])
async def health() -> dict[str, str]:
    """Kubernetes-friendly liveness & readiness probe."""
    return {"status": "ok"}


@app.get("/", tags=["utility"])
async def root() -> dict[str, str]:
    """Temporary landing route until the real UI is wired up."""
    return {"message": "Welcome to the CompliPilot API 🚀"}


# ---------------------------------------------------------------------------
# Allow `python -m app.main` convenience ------------------------------------
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=False,
        log_level="info",
    )
