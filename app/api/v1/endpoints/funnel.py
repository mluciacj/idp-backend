from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.models.data_models.user import User
from app.models.data_models.funnel import ConversionFunnel
from app.schemas.funnel import (
    ConversionFunnelCreate,
    ConversionFunnelUpdate,
    ConversionFunnelOut
)
from app.core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Conversion Funnel"])

@router.post("/funnel-step", response_model=ConversionFunnelOut)
def create_funnel_step(
    data: ConversionFunnelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    funnel_step = ConversionFunnel(
        user_id=current_user.id,
        session_id=data.session_id,
        funnel_step=data.funnel_step,
        step_order=data.step_order
    )
    db.add(funnel_step)
    db.commit()
    db.refresh(funnel_step)
    return funnel_step

@router.patch("/funnel-step/{funnel_id}", response_model=ConversionFunnelOut)
def update_funnel_step(
    funnel_id: UUID,
    update: ConversionFunnelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    funnel_step = db.query(ConversionFunnel).filter(
        ConversionFunnel.id == funnel_id,
        ConversionFunnel.user_id == current_user.id
    ).first()

    if not funnel_step:
        raise HTTPException(status_code=404, detail="Funnel step not found")

    for field, value in update.dict(exclude_unset=True).items():
        setattr(funnel_step, field, value)

    db.commit()
    db.refresh(funnel_step)
    return funnel_step
