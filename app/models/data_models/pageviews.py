from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, INET
from datetime import datetime
import uuid
from app.core.database import Base

class PageView(Base):
    __tablename__ = "page_views"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("user_sessions.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    page_path = Column(String(255), nullable=False)
    page_title = Column(String(255))
    referrer = Column(String)
    ip_address = Column(INET)
    user_agent = Column(String)
    viewport_width = Column(Integer)
    viewport_height = Column(Integer)
    page_load_time_ms = Column(Integer)
    time_on_page_seconds = Column(Integer)
    scroll_depth_percent = Column(Integer)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    exited_at = Column(DateTime, nullable=True)