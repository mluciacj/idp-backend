from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class PageViewBase(BaseModel):
    session_id: UUID
    page_path: str
    page_title: Optional[str]
    referrer: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    viewport_width: Optional[int]
    viewport_height: Optional[int]
    page_load_time_ms: Optional[int]
    scroll_depth_percent: Optional[int]

class PageViewCreate(PageViewBase):
    pass

class PageViewOut(PageViewBase):
    id: UUID
    user_id: Optional[UUID]
    viewed_at: datetime
    exited_at: Optional[datetime]
    time_on_page_seconds: Optional[int]

    class Config:
        orm_mode = True
