from tortoise import fields, models


class Post(models.Model):
    """
    データベース内の Post エントリを表す
    'posts' テーブルにマッピングされる
    """
    id = fields.IntField(pk=True)  # プライマリキー、自動インクリメント整数
    title = fields.CharField(max_length=255)
    content = fields.TextField()

    def __str__(self):
        return self.title

    class Meta:
        table = "posts"  # オプション: テーブル名を指定
