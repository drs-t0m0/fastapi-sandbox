# service.py
# ビジネスロジックをカプセル化します。
from fastapi import HTTPException, status
from .models import Post, PostCreate, PostUpdate


class PostsService:
    def __init__(self):
        """
        サービスを初期化し、インメモリのポストリストと最後のIDをセットアップします。
        """
        self.posts: list[Post] = []  # ポストを格納するリスト
        self.last_post_id: int = 0  # ポストIDを生成するためのカウンター

    def _get_post(self, post_id: int) -> Post:
        """
        指定されたIDのポストを取得します。
        Args:
            post_id (int): 検索するポストのID。
        Returns:
            Post: 見つかったポスト。
        Raises:
            HTTPException: ポストが見つからない場合 (404 NOT_FOUND)。
        """
        for post in self.posts:
            if post.id == post_id:
                return post
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    def get_all_posts(self) -> list[Post]:
        """
         すべてのポストを取得します。
         Returns:
            list[Post]: ポストのリスト。
         """
        return self.posts

    def get_post_by_id(self, post_id: int) -> Post:
        """
        指定されたIDのポストを取得します。
        Args:
            post_id (int): 取得するポストのID。
        Returns:
            Post: 見つかったポスト。
        Raises:
            HTTPException: ポストが見つからない場合 (404 NOT_FOUND)。
        """
        return self._get_post(post_id)

    def create_post(self, post_data: PostCreate) -> Post:
        """
        新しいポストを作成します。
        Args:
            post_data (PostCreate): 作成するポストのデータ。
        Returns:
            Post: 作成された新しいポスト。
        """
        self.last_post_id += 1
        new_post = Post(id=self.last_post_id, **post_data.model_dump())
        self.posts.append(new_post)
        return new_post

    def replace_post(self, post_id: int, post_data: PostUpdate) -> Post:
        """
        指定されたIDのポストを更新します。
        Args:
            post_id (int): 更新するポストのID。
            post_data (PostUpdate): 新しいポストのデータ。
        Returns:
            Post: 更新されたポスト。
        Raises:
            HTTPException: ポストが見つからない場合 (404 NOT_FOUND)。
        """
        post = self._get_post(post_id)
        updated_post = Post(**post_data.model_dump())
        index = self.posts.index(post)
        self.posts[index] = updated_post
        return updated_post

    def delete_post(self, post_id: int) -> None:
        """
         指定されたIDのポストを削除します。
         Args:
             post_id (int): 削除するポストのID。
         Returns:
             None
         Raises:
             HTTPException: ポストが見つからない場合 (404 NOT_FOUND)。
         """
        post = self._get_post(post_id)
        self.posts.remove(post)


# サービスインスタンスをシングルトンとして作成
# アプリケーション全体で同じサービスインスタンスが共有されます。
posts_service = PostsService()


# 依存性注入用の関数
def get_posts_service() -> PostsService:
    """
    PostsServiceのインスタンスを返す依存性注入用の関数。
    """
    return posts_service
