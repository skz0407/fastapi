import uuid

from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


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
    # Relationship for accessing user's events
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)  # イベント名
    start_time = Column(TIMESTAMP, nullable=False)  # 開始日時
    end_time = Column(TIMESTAMP, nullable=False)  # 終了日時

    # Relationship back to user
    user = relationship("User", back_populates="events")
