# main.py
# FastAPIアプリケーションのインスタンスを作成し、ルーターを登録します。
# アプリケーションのエントリーポイントとなります。

from fastapi import FastAPI
from posts.router import router as posts_router

# FastAPIアプリケーションインスタンスを作成
app = FastAPI(
    title="Posts API",
    description="FastAPIを使用したシンプルな投稿API",
    version="0.1.0",
)

# postsルーターをアプリケーションに含める
# これにより、/posts プレフィックスを持つエンドポイントが利用可能になります。
app.include_router(posts_router)
