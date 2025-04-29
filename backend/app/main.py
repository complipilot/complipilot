from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

# Import your database engine (created in app/db.py, for example)
# If it lives somewhere else, adjust the import accordingly.
from app.db import engine  # noqa: E402

# ---------------------------------------------------------------------------
# Lifespan handler -----------------------------------------------------------
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run once at startup / shutdown.

    * Creates all tables from the SQLModel metadata (idempotent).
    * Place any other one‑time startup work here (seed data, schedulers, etc.).
    """
    SQLModel.metadata.create_all(bind=engine)
    yield
    # --- shutdown logic goes here (if any) ---------------------------------

# ---------------------------------------------------------------------------
# FastAPI application instance ----------------------------------------------
# ---------------------------------------------------------------------------

app = FastAPI(
    title="CompliPilot API",
    version="0.1.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Simple sanity‑check endpoints ---------------------------------------------
# ---------------------------------------------------------------------------

@app.get("/health", tags=["utility"])
async def health() -> dict[str, str]:
    """Kubernetes‑friendly liveness/readiness probe."""
    return {"status": "ok"}


@app.get("/", tags=["utility"])
async def root() -> dict[str, str]:
    """Root welcome route until real UI is wired."""
    return {"message": "Welcome to the CompliPilot API 🚀"}

# ---------------------------------------------------------------------------
# Include additional routers below ------------------------------------------
# ---------------------------------------------------------------------------
# from app.api.v1.router import api_router as v1_router
# app.include_router(v1_router, prefix="/api/v1")

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
