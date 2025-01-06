import os
from sqlalchemy import create_engine, select, join
from sqlalchemy.orm import sessionmaker
from models import User, Event, Thread, Comment
from dotenv import load_dotenv

load_dotenv()

# 接続先DBの設定
DATABASE = os.getenv("DATABASE_URL")

# Engine の作成
Engine = create_engine(
  DATABASE,
  echo=True
)

# Sessionの作成
SessionLocal = sessionmaker(
  autocommit = False,
  autoflush = True,
  bind = Engine
)

# データベースセッションを取得する依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_from_db(user_id: str, db):
    return db.query(User).filter(User.id == user_id).first()

# ユーザー情報を更新
def update_user_in_db(user_id: str, user_data: dict, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# ユーザーのイベント一覧を取得
def get_user_events(user_id: str, db):
    return db.query(Event).filter(Event.user_id == user_id).all()

# 特定のイベントを取得
def get_event_by_id(event_id: str, user_id: str, db):
    return db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()

# イベントを作成
def create_event_for_user(event_data: dict, db):
    new_event = Event(**event_data)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# イベントを更新
def update_event_for_user(event_id: str, user_id: str, event_data: dict, db):
    event = db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
    if not event:
        return None
    for key, value in event_data.items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

# イベントを削除
def delete_event_for_user(event_id: str, user_id: str, db):
    event = db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
    if event:
        db.delete(event)
        db.commit()
    return event


# 新しいスレッドを作成
def create_thread(thread_data: dict, db):
    thread = Thread(**thread_data)
    db.add(thread)
    db.commit()
    db.refresh(thread)
    return thread

# スレッドを取得
def get_thread(thread_id: str, db):
    return db.query(Thread).filter(Thread.id == thread_id).first()


def get_threads_by_user(user_id: str, db):
    """
    ユーザーが作成したスレッドまたはコメントしたスレッドを取得
    """
    # ユーザーが作成したスレッド
    created_threads = db.query(Thread).filter(Thread.user_id == user_id).all()

    # ユーザーがコメントしたスレッド
    commented_threads = (
        db.query(Thread)
        .join(Comment, Thread.id == Comment.thread_id)
        .filter(Comment.user_id == user_id)
        .all()
    )

    # 重複を排除して返す
    all_threads = {thread.id: thread for thread in created_threads + commented_threads}
    return list(all_threads.values())

# 全スレッドを取得
def get_threads_with_usernames(db):
    stmt = select(
        Thread.id,
        Thread.title,
        Thread.content,
        Thread.user_id,
        Thread.created_at,
        Thread.updated_at,
        User.username  # JOINでusernameを取得
    ).join(User, Thread.user_id == User.id)
    return db.execute(stmt).fetchall()

# 新しいコメントを作成
def create_comment(comment_data: dict, db):
    comment = Comment(**comment_data)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

# コメントを取得
def get_comments_with_usernames(thread_id: str, db):
    stmt = select(
        Comment.id,
        Comment.content,
        Comment.created_at,
        User.username  # JOINでusernameを取得
    ).join(User, Comment.user_id == User.id).filter(Comment.thread_id == thread_id)
    return db.execute(stmt).fetchall()