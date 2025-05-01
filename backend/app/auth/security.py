from datetime import datetime, timedelta
import os
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

# ────────────────────────────────────────────────────────────
# 1. Config ─ pull from .env, fall back to dev-safe defaults
# ────────────────────────────────────────────────────────────
SECRET_KEY: str = os.getenv("JWT_SECRET", "change-me-in-prod")
ALGORITHM: str   = os.getenv("JWT_ALGO",  "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", 15))

# ────────────────────────────────────────────────────────────
# 2. Password hashing
# ────────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Return a bcrypt hash of the plaintext password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare plaintext vs stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

# ────────────────────────────────────────────────────────────
# 3. JWT helpers
# ────────────────────────────────────────────────────────────
def create_access_token(
    subject: Any,
    expires_delta: timedelta | None = None,
) -> str:
    """Generate a signed JWT; `sub` can be user id or email."""
    expire = datetime.utcnow() + (expires_delta or timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """
    Decode & verify a JWT, raising 401 if it’s invalid.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
