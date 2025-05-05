# Setting up a PostgreSQL database with TypeORM

このコードは、下記の概念をPythonエコシステムにマッピングします。

- 環境変数
- Validation
- データベース接続
- エンティティ/モデル
- CRUD操作

まず、コードの構造と各コンポーネントについて説明します。

- .env ファイル: データベース接続情報などの設定を保存します。
- settings.py: Pydanticを使用して環境変数を読み込み、検証します。
- models.py: Tortoise ORMを使用してデータベースモデル(Post)を定義します。
- schemas.py: Pydanticを使用してAPIリクエストとレスポンスのデータ構造(スキーマ)を定義します。
- main.py: FastAPIアプリケーションを作成し、Tortoise ORMを初期化し、APIエンドポイント(CRUD操作)を定義します。

## Docker with PostgreSQL database

```
$ docker compose up -d
```

```
$ docker compose ps
```

```
$ docker compose down
```

### Create database

```sql
-- データベースを作成 (所有者を .env ファイルのユーザーに設定)
CREATE DATABASE fastapi_tortoise OWNER admin;
```

## Ref

- https://wanago.io/2020/05/18/api-nestjs-postgresql-typeorm/
