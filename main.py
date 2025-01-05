from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from database import (
    get_db,
    get_user_from_db,
    update_user_in_db,
    get_user_events,
    create_event_for_user,
    update_event_for_user,
    delete_event_for_user
)
from models import User, Event

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    google_id: str
    email: str
    username: str
    avatar_url: str

class GetUser(BaseModel):
    id: str  # UUIDを文字列として返す
    google_id: str
    username: str
    email: str
    avatar_url: str
    created_at: str
    updated_at: str

class UserUpdate(BaseModel):
    username: str
    email: str
    avatar_url: str

class GoogleIdRequest(BaseModel):
    google_id: str

# Event Pydantic Models
class EventBase(BaseModel):
    title: str
    start_time: str  # ISO8601形式で日時
    end_time: str  # ISO8601形式で日時

class EventCreate(EventBase):
    user_id: str  # UUID形式

class EventUpdate(EventBase):
    pass

class EventResponse(EventBase):
    id: str


@app.get("/users/{user_id}", response_model=GetUser)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user_from_db(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(user.id),
        "google_id": user.google_id,
        "username": user.username,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }

# PUT: ユーザー情報更新
@app.put("/users/{user_id}")
def update_user(user_id: str, user_data: UserUpdate,  db: Session = Depends(get_db)):
    updated_user = update_user_in_db(user_id, user_data.dict(), db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(updated_user.id),
        "username": updated_user.username,
        "email": updated_user.email,
        "avatar_url": updated_user.avatar_url,
        "created_at": updated_user.created_at.isoformat(),
        "updated_at": updated_user.updated_at.isoformat(),
    }

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    """
    テーブルに登録されているすべてのユーザーを取得
    """
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "google_id": user.google_id,
            "username": user.username,
            "email": user.email,
            "avatar_url": user.avatar_url,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        }
        for user in users
    ]



@app.post("/auth/google")
def create_or_get_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # ログ出力
    print("受信したデータ:", user_data.dict())
    
    user = db.query(User).filter(User.google_id == user_data.google_id).first()
    if user:
        print("既存のユーザーが見つかりました:", user)
        return {"message": "User already exists", "user": user_data.dict()}

    new_user = User(
        google_id=user_data.google_id,
        email=user_data.email,
        username=user_data.username,
        avatar_url=user_data.avatar_url,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("新しいユーザーが作成されました:", new_user)
    return {"message": "User created successfully", "user": user_data.dict()}

@app.post("/auth/google-id")
def get_user_id_by_google_id(request: GoogleIdRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.google_id == request.google_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id}

# ユーザーのイベント一覧を取得
@app.get("/users/{user_id}/events", response_model=List[EventResponse])
def get_events(user_id: str, db: Session = Depends(get_db)):
    events = get_user_events(user_id, db)
    return [
        EventResponse(
            id=str(event.id),
            title=event.title,
            start_time=event.start_time.isoformat(),
            end_time=event.end_time.isoformat(),
        )
        for event in events
    ]

# イベントを作成
@app.post("/users/{user_id}/events", response_model=EventResponse)
def create_event(user_id: str, event_data: EventCreate, db: Session = Depends(get_db)):
    event_data_dict = event_data.dict()
    event_data_dict["user_id"] = user_id
    new_event = create_event_for_user(event_data_dict, db)
    return EventResponse(
        id=str(new_event.id),
        title=new_event.title,
        start_time=new_event.start_time.isoformat(),
        end_time=new_event.end_time.isoformat(),
    )

# イベントを更新
@app.put("/users/{user_id}/events/{event_id}", response_model=EventResponse)
def update_event(user_id: str, event_id: str, event_data: EventUpdate, db: Session = Depends(get_db)):
    updated_event = update_event_for_user(event_id, user_id, event_data.dict(), db)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(
        id=str(updated_event.id),
        title=updated_event.title,
        start_time=updated_event.start_time.isoformat(),
        end_time=updated_event.end_time.isoformat(),
    )

# イベントを削除
@app.delete("/users/{user_id}/events/{event_id}")
def delete_event(user_id: str, event_id: str, db: Session = Depends(get_db)):
    event = delete_event_for_user(event_id, user_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}
