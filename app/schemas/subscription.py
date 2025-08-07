from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class SubscriptionBase(BaseModel):
    plan_type: str
    billing_period: str
    amount: float
    currency: str
    status: str
    trial_start_date: Optional[datetime]
    trial_end_date: Optional[datetime]
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: Optional[bool] = False
    canceled_at: Optional[datetime]

class SubscriptionCreate(SubscriptionBase):
    stripe_subscription_id: str

class SubscriptionOut(SubscriptionBase):
    id: UUID
    user_id: UUID
    stripe_subscription_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True