from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv()


class Settings(BaseSettings):
    """
    環境変数から読み込まれるアプリケーション設定
    検証には Pydantic を使用
    """
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str
    app_port: int = 8000  # .env で設定されていない場合のデフォルトポート

    # Pydantic が .env ファイルから読み込むように設定
    # 環境変数が大文字の場合に postgres_user と一致させるために case_sensitive を False に設定
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    @property
    def database_url(self) -> str:
        """非同期データベース URL を構築する。"""
        return f"postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


# 設定をインスタンス化
settings = Settings()
