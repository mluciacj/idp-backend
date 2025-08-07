from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.models.data_models.user import User
from app.models.data_models.billing_address import BillingAddress
from app.core.security import get_current_user
from app.schemas.billing_address import BillingAddressCreate, BillingAddressUpdate, BillingAddressOut
from datetime import datetime

router = APIRouter(prefix="/billing", tags=["Billing Address"])

@router.get("/address", response_model=BillingAddressOut)
def get_billing_address(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = db.query(BillingAddress).filter(BillingAddress.user_id == current_user.id, BillingAddress.is_primary == True).first()
    if not address:
        raise HTTPException(status_code=404, detail="Billing address not found")
    return address

@router.post("/address", response_model=BillingAddressOut)
def create_billing_address(address_in: BillingAddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = BillingAddress(**address_in.dict(), user_id=current_user.id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

@router.patch("/address/{address_id}")
def update_billing_address(address_id: UUID, new_data: BillingAddressUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = db.query(BillingAddress).filter(BillingAddress.id == address_id, BillingAddress.user_id == current_user.id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Billing address not found")

    for key, value in new_data.dict(exclude_unset=True).items():
        setattr(address, key, value)

    db.commit()
    return {"detail": "Billing address updated."}