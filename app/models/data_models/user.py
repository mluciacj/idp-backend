# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    company = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    stripe_customer_id = Column(String(100), unique=True, nullable=True)
    client_id = Column(UUID(as_uuid=True), unique=True, nullable=True)
    email_verified = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    status = Column(String(20), default='active')  # active, suspended, deleted
