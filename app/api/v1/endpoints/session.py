from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.models.data_models.session import UserSession
from app.models.data_models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", status_code=201)
def create_session(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    token = request.headers.get("Authorization").split(" ")[1]
    session = UserSession(
        user_id=current_user.id,
        session_token=token,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        device_type="unknown",
        browser="unknown",
        operating_system="unknown",
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=7),
        last_activity_at=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id}

@router.patch("/{session_id}/heartbeat")
def update_last_activity(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(UserSession).filter(UserSession.id == session_id, UserSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.last_activity_at = datetime.utcnow()
    db.commit()
    return {"detail": "Session heartbeat updated"}

@router.delete("/{session_id}")
def delete_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(UserSession).filter(UserSession.id == session_id, UserSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"detail": "Session deleted successfully"}