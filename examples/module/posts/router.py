# posts.py
# APIルーターを定義し、HTTPリクエストを処理します。

from fastapi import APIRouter, Depends, HTTPException, status, Response
from .models import Post, PostCreate, PostUpdate
from .service import get_posts_service

# APIRouterインスタンスを作成
# prefix: このルーターのすべてのパスの前に付加されるプレフィックス
# tags: OpenAPIドキュメント（Swagger UIなど）でグループ化するためのタグ
router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[Post])
async def get_all_posts(posts_service=Depends(get_posts_service)):
    """
    すべてのポストを取得するエンドポイント。
    """
    return posts_service.get_all_posts()


@router.get("/{post_id}", response_model=Post)
async def get_post_by_id(
        post_id: int,  # パスパラメータからIDを取得
        posts_service=Depends(get_posts_service)
):
    """
    指定されたIDのポストを取得するエンドポイント。
    見つからない場合は404エラーを返します。
    """
    post = posts_service.get_post_by_id(post_id)
    return post


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
        post_data: PostCreate,  # リクエストボディをPydanticモデルで受け取り、バリデーション
        posts_service=Depends(get_posts_service)
):
    """
    新しいポストを作成するエンドポイント。
    成功時にはステータスコード 201 Created を返します。
    """
    return posts_service.create_post(post_data)


@router.put("/{post_id}", response_model=Post)
async def replace_post(
        post_id: int,
        post_data: PostUpdate,
        posts_service=Depends(get_posts_service)
):
    """
    指定されたIDのポストを更新するエンドポイント。
    見つからない場合は404エラーを返します。
    """
    # post_data.id と post_id が一致するかチェック
    if post_data.id != post_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post ID in URL and body do not match",
        )
    return posts_service.replace_post(post_id, post_data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: int,
        posts_service=Depends(get_posts_service)
):
    """
    指定されたIDのポストを削除するエンドポイント。
    成功時にはステータスコード 204 No Content を返します。
    見つからない場合は404エラーを返します。
    """
    posts_service.delete_post(post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
