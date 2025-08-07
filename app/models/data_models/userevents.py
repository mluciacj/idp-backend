from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from app.core.database import Base

class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("user_sessions.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    event_category = Column(String(50), nullable=False)
    event_action = Column(String(100), nullable=False)
    event_label = Column(String(255), nullable=True)
    event_value = Column(Integer, nullable=True)
    page_path = Column(String(255), nullable=False)
    element_id = Column(String(100), nullable=True)
    element_class = Column(String(100), nullable=True)
    additional_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)