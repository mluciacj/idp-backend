from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.data_models.user import User
from app.models.data_models.userevents import UserEvent
from app.core.security import get_current_user
from app.schemas.userevents import UserEventCreate, UserEventOut

router = APIRouter(prefix="/analytics", tags=["User Events"])

@router.post("/event", response_model=UserEventOut)
def create_user_event(
    event_data: UserEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = UserEvent(
        user_id=current_user.id,
        session_id=event_data.session_id,
        event_category=event_data.event_category,
        event_action=event_data.event_action,
        event_label=event_data.event_label,
        event_value=event_data.event_value,
        page_path=event_data.page_path,
        element_id=event_data.element_id,
        element_class=event_data.element_class,
        additional_data=event_data.additional_data,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event