from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, UUID, Text
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import DeclarativeBase, relationship

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

    # Relationships
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")  # ユーザーのイベント
    threads = relationship("Thread", back_populates="user", cascade="all, delete-orphan")  # ユーザーが作成したスレッド
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")  # ユーザーが投稿したコメント

class Event(Base):
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)  # イベント名（最大255文字）
    start_time = Column(TIMESTAMP, nullable=False)  # 開始日時
    end_time = Column(TIMESTAMP, nullable=False)  # 終了日時

    # Relationship back to user
    user = relationship("User", back_populates="events")

class Thread(Base):
    __tablename__ = "threads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(50), nullable=False)  # スレッドのタイトル（最大50文字）
    content = Column(String(1000), nullable=False)  # スレッドの内容（最大1000文字）
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="threads")  # 作成者
    comments = relationship("Comment", back_populates="thread", cascade="all, delete-orphan")  # スレッド内のコメント

class Comment(Base):
    __tablename__ = "comments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(500), nullable=False)  # コメントの内容（最大500文字）
    created_at = Column(TIMESTAMP, server_default=func.now())  # 作成日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # 更新日時

    # Relationships
    thread = relationship("Thread", back_populates="comments")  # コメントが属するスレッド
    user = relationship("User", back_populates="comments")  # コメントの作成者

