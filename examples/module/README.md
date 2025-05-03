# Controllers, routing and the module structure

FastAPIは型ヒントとPydanticを積極的に活用し、自動的なデータバリデーションやAPIドキュメント生成といったメリットを提供します。

FastAPIでは、

- コントローラーをAPIルーター
- サービスをビジネスロジックをカプセル化するクラスや関数
- DTO(Data Transfer Object)をPydanticモデル
- モジュールをPythonのモジュールやパッケージ

として表現します。

## Module Structure

ファイル構造は以下のようになります。

```
root/
├── posts/
│   ├── __init__.py       # Pythonパッケージとして認識させるための空ファイル
│   ├── models.py         # Pydanticモデル (DTOs/Interfaces)
│   ├── service.py        # ビジネスロジック (Service)
│   └── posts.py          # APIルーター (Controller)
└── main.py               # FastAPIアプリケーションのエントリーポイント
```

## Ref

- https://wanago.io/2020/05/11/nestjs-api-controllers-routing-module/

