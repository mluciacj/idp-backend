from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.data_models.user import User
from app.models.data_models.subscription import Subscription
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.get("/subscription")
def get_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.post("/subscribe")
def start_subscription(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Aqui você integraria com a API do Stripe e criaria uma sessão de checkout
    fake_subscription = Subscription(
        id=uuid4(),
        user_id=current_user.id,
        stripe_subscription_id="fake_stripe_id",
        plan_type="starter",
        billing_period="monthly",
        amount=29.99,
        currency="USD",
        status="active",
        current_period_start=datetime.utcnow(),
        current_period_end=datetime.utcnow() + timedelta(days=30)
    )
    db.add(fake_subscription)
    db.commit()
    return {"detail": "Subscription started (simulated Stripe session)."}

@router.post("/webhook")
def stripe_webhook():
    # Aqui você processaria eventos do Stripe (pagamento recebido, cancelamento, etc.)
    return {"detail": "Webhook received (not implemented)."}

@router.patch("/update-plan")
def update_plan(plan_type: str, billing_period: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.plan_type = plan_type
    subscription.billing_period = billing_period
    subscription.updated_at = datetime.utcnow()
    db.commit()
    return {"detail": "Subscription updated."}

@router.delete("/cancel")
def cancel_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = "canceled"
    subscription.canceled_at = datetime.utcnow()
    db.commit()
    return {"detail": "Subscription canceled."}

@router.get("/invoices")
def get_invoices():
    # Aqui você listaria as faturas do usuário via API do Stripe
    return {"detail": "List of invoices (not implemented)."}
