from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db import get_session
from . import models, schemas, security

router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=schemas.UserRead, status_code=201)
def register(payload: schemas.UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(models.User).where(models.User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        email=payload.email,
        hashed_password=security.hash_password(payload.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)):
    user = session.exec(select(models.User).where(models.User.email == form.username)).first()
    if not user or not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    token = security.create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}
