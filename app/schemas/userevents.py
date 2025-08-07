from pydantic import BaseModel
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime

class UserEventBase(BaseModel):
    session_id: UUID
    event_category: str
    event_action: str
    event_label: Optional[str] = None
    event_value: Optional[int] = None
    page_path: str
    element_id: Optional[str] = None
    element_class: Optional[str] = None
    additional_data: Optional[Dict] = None

class UserEventCreate(UserEventBase):
    pass

class UserEventOut(UserEventBase):
    id: UUID
    user_id: Optional[UUID]
    created_at: datetime

    class Config:
        orm_mode = True