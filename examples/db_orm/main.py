from fastapi import FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from settings import settings
from models import Post
from schemas import PostCreate, PostUpdate, PostResponse

# FastAPI アプリインスタンスを作成
app = FastAPI(title="FastAPI with Tortoise ORM")

# Tortoise ORM を FastAPI アプリに登録
# これにより、起動時とシャットダウン時に接続設定が処理される
register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["models"]},  # モデルを含むモジュールを指定
    generate_schemas=True,  # モデルに基づいてテーブルを自動生成する。本番環境では False に設定
    add_exception_handlers=True  # DoesNotExist および IntegrityError のハンドラを追加
)


@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    """
    データベースに新しい投稿を作成する
    """
    try:
        # 検証済みのリクエストデータを使用して新しい Post オブジェクトを作成
        new_post = await Post.create(**post_data.model_dump())
        return new_post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"投稿の作成に失敗しました: {e}"
        )


@app.get("/posts", response_model=list[PostResponse])
async def get_all_posts():
    """
    データベースからすべての投稿を取得する
    """
    posts = await Post.all()
    return posts


@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: int):
    """
    ID によって単一の投稿を取得する
    投稿が見つからない場合のケースを処理する
    """
    try:
        post = await Post.get(id=post_id)
        return post
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {post_id} の投稿が見つかりません"
        )


@app.patch("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_data: PostUpdate):
    """
    既存の投稿を部分的に更新する (PATCH)
    リクエストボディで提供されたフィールドのみを更新する
    """
    try:
        # 既存の投稿を取得
        post = await Post.get(id=post_id)

        # 未設定のフィールドを除外して、新しいデータで投稿オブジェクトを更新
        update_data = post_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="更新するフィールドが提供されていません。"
            )

        # Tortoise の update_from_dict メソッドでフィールドを更新
        await post.update_from_dict(update_data)

        # 変更をデータベースに保存
        await post.save()
        return post
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {post_id} の投稿が見つかりません"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"投稿の更新に失敗しました: {e}"
        )


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    """
    ID によって投稿を削除する。
    成功時に 204 No Content を返す。
    """
    try:
        # 削除する前に投稿が存在することを確認するために取得
        post = await Post.get(id=post_id)
        # 投稿を削除
        deleted_count = await post.delete()  # delete() は削除された行数を返す

        # get() は DoesNotExist を発生させるが、このチェックは競合削除を想定
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {post_id} の投稿が見つかりません"
            )
        return None
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {post_id} の投稿が見つかりません"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"投稿の削除に失敗しました: {e}"
        )
