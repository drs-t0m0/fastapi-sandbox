from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


# 投稿作成用の Pydantic モデル(リクエストボディ)
class PostCreate(PostBase):
    pass


# 投稿更新用の Pydantic モデル(リクエストボディ)
# PATCH 動作のため、すべてのフィールドはオプショナル
class PostUpdate(PostBase):
    title: str | None
    content: str | None


# レスポンスで投稿を表す Pydantic モデル
class PostResponse(PostBase):
    id: int
