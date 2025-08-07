from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base

class ConversionFunnel(Base):
    __tablename__ = "conversion_funnel"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("user_sessions.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    funnel_step = Column(String(50), nullable=False)  # e.g., landing, pricing, payment, completed
    step_order = Column(Integer, nullable=False)
    entered_at = Column(DateTime, default=datetime.utcnow)
    exited_at = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    conversion_time_seconds = Column(Integer, nullable=True)
    abandoned_at_field = Column(String(100), nullable=True)