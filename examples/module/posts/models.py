# models.py
# Pydanticモデルを定義し、データ構造とバリデーションを行います。

from pydantic import BaseModel


# ポストの基本構造を定義するベースモデル
class PostBase(BaseModel):
    title: str
    content: str


# ポスト作成時に受け取るデータモデル
class PostCreate(PostBase):
    pass


# ポスト更新時に受け取るデータモデル
class PostUpdate(PostBase):
    id: int


# APIレスポンスや内部処理で使用するポストモデル
class Post(PostBase):
    id: int

    # Pydanticモデルをデータベースモデル等に変換可能にする設定
    class Config:
        from_attributes = True
