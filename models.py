from sqlalchemy import Column, String, TIMESTAMP, UUID
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    google_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)
    avatar_url = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())