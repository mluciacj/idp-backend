from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ConversionFunnelBase(BaseModel):
    session_id: UUID
    funnel_step: str
    step_order: int

class ConversionFunnelCreate(ConversionFunnelBase):
    pass

class ConversionFunnelUpdate(BaseModel):
    exited_at: Optional[datetime] = None
    completed: Optional[bool] = None
    conversion_time_seconds: Optional[int] = None
    abandoned_at_field: Optional[str] = None

class ConversionFunnelOut(ConversionFunnelBase):
    id: UUID
    user_id: Optional[UUID]
    entered_at: datetime
    exited_at: Optional[datetime] = None
    completed: bool = False
    conversion_time_seconds: Optional[int] = None
    abandoned_at_field: Optional[str] = None

    class Config:
        orm_mode = True