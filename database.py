from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User


# 接続先DBの設定
DATABASE = 'postgresql+psycopg://user:postgres@localhost:5432/postgres'

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
