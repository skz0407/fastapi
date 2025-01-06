from pydantic import BaseModel, Field

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

class EventBase(BaseModel):
    title: str = Field(..., max_length=255)  # タイトル最大255文字
    start_time: str  # ISO8601形式で日時
    end_time: str  # ISO8601形式で日時

class EventCreate(EventBase):
    user_id: str  # UUID形式

class EventUpdate(EventBase):
    pass

class EventResponse(EventBase):
    id: str

class ThreadBase(BaseModel):
    title: str = Field(..., max_length=50)  # タイトル最大50文字
    content: str = Field(..., max_length=1000)  # コンテンツ最大1000文字
    user_id: str  # UUID形式

class ThreadCreate(ThreadBase):
    pass

class ThreadResponse(BaseModel):
    id: str
    title: str
    content: str
    username: str  # 作成者のユーザー名
    created_at: str
    updated_at: str

class CommentBase(BaseModel):
    content: str = Field(..., max_length=500)  # コメント最大500文字
    thread_id: str  # UUID形式
    user_id: str  # UUID形式

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: str
    username: str  # 作成者のusernameを含む
    created_at: str