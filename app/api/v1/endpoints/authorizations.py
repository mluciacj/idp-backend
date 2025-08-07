from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from uuid import uuid4

from app.core.database import get_db
from app.models.data_models.user import User
from app.models.data_models.session import UserSession
from app.schemas.auth import (
    UserCreate, UserOut, Token, 
    EmailVerification, PasswordResetRequest, PasswordResetConfirm
)
from app.core.security import (
    create_access_token, create_refresh_token, verify_password,
    get_password_hash, get_current_user, create_reset_token,
    verify_reset_token, send_reset_email
)

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", response_model=UserOut)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        password_hash=get_password_hash(user_in.password),
        marketing_consent=user_in.marketing_consent
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    session = UserSession(
        user_id=user.id,
        session_token=refresh_token,
        ip_address="0.0.0.0",  # you can extract from request.client.host
        user_agent="Unknown",
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(session)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    token = request.headers.get("Authorization").split(" ")[1]
    session = db.query(UserSession).filter(UserSession.session_token == token).first()
    if session:
        db.delete(session)
        db.commit()
    return {"detail": "Logged out successfully"}

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/refresh-token", response_model=Token)
def refresh_token(request: Request, db: Session = Depends(get_db)):
    old_token = request.headers.get("Authorization").split(" ")[1]
    try:
        payload = jwt.decode(old_token, "SECRET_KEY", algorithms=["HS256"])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/verify-email")
def verify_email(data: EmailVerification, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email_verified = True
    db.commit()
    return {"detail": "Email verified."}

@router.post("/request-password-reset")
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = create_reset_token(str(user.id))
    send_reset_email(user.email, reset_token)
    return {"detail": "Password reset link sent."}

@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    user_id = verify_reset_token(data.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password_hash = get_password_hash(data.new_password)
    db.commit()
    return {"detail": "Password reset successfully."}
