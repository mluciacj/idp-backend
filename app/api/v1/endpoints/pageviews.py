from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models.data_models.user import User
from app.models.data_models.pageviews import PageView
from app.core.security import get_current_user
from app.schemas.pageviews import PageViewCreate, PageViewOut

router = APIRouter(prefix="/analytics", tags=["Page Views"])

@router.post("/page-view", response_model=PageViewOut)
def create_page_view(data: PageViewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    page_view = PageView(
        user_id=current_user.id,
        session_id=data.session_id,
        page_path=data.page_path,
        page_title=data.page_title,
        referrer=data.referrer,
        ip_address=data.ip_address,
        user_agent=data.user_agent,
        viewport_width=data.viewport_width,
        viewport_height=data.viewport_height,
        page_load_time_ms=data.page_load_time_ms,
        scroll_depth_percent=data.scroll_depth_percent
    )
    db.add(page_view)
    db.commit()
    db.refresh(page_view)
    return page_view

@router.patch("/page-view/{page_view_id}")
def update_page_view(page_view_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    page_view = db.query(PageView).filter(PageView.id == page_view_id, PageView.user_id == current_user.id).first()
    if not page_view:
        raise HTTPException(status_code=404, detail="Page view not found")
    page_view.exited_at = datetime.utcnow()
    if page_view.viewed_at:
        duration = (page_view.exited_at - page_view.viewed_at).total_seconds()
        page_view.time_on_page_seconds = int(duration)
    db.commit()
    return {"detail": "Page view updated"}

