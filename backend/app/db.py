from __future__ import annotations

"""Database engine & session helpers.

✓ Reads DATABASE_URL from your .env (already loaded by main).
✓ Exposes a global `engine` object.
✓ Provides a fast‑api‑friendly `get_session` dependency.
"""

import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# ---------------------------------------------------------------------------
# Load .env so this module works when imported directly ---------------------
# (uvicorn/poetry already runs in the project root, but this is extra‑safe.)
# ---------------------------------------------------------------------------
load_dotenv()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:dev@localhost:5432/complipilot",  # sensible default
)

# Echo=True prints SQL in the log – handy for dev; set False in prod.
engine = create_engine(DATABASE_URL, echo=True)

# ---------------------------------------------------------------------------
# Dependency helper for FastAPI routes --------------------------------------
# ---------------------------------------------------------------------------

def get_session():
    """Yield a SQLModel Session that is closed after request/usage."""
    with Session(engine) as session:
        yield session

# ---------------------------------------------------------------------------
# Optional CLI convenience ---------------------------------------------------
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Quick smoke‑test: can we connect and list tables?
    from sqlalchemy import inspect

    inspector = inspect(engine)
    print("Connected! Current tables:", inspector.get_table_names())
