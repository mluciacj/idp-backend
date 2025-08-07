from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class BillingAddressBase(BaseModel):
    street_address: str
    city: str
    state: str
    zip_code: str
    country: str = Field(default="US", min_length=2, max_length=2)
    is_primary: Optional[bool] = True

class BillingAddressCreate(BillingAddressBase):
    pass

class BillingAddressUpdate(BaseModel):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_primary: Optional[bool] = None

class BillingAddressOut(BillingAddressBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
