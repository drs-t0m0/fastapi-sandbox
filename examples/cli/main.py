import typer
from datetime import datetime, timedelta, timezone, date
from typing import Annotated
import sys  # 標準エラー出力のため

# Typerアプリケーションを作成
app = typer.Typer()


def parse_date_string(date_str: str) -> datetime | None:
    """
    ISO 8601形式の日付・時刻文字列をパースする。
    'YYYY-MM-DD' 形式も受け付ける。
    パースできない場合はNoneを返す。
    """
    try:
        # datetime.fromisoformat は日付 ('YYYY-MM-DD') と
        # 日時 ('YYYY-MM-DDTHH:MM:SS', タイムゾーン付きも可) を処理できる
        parsed_dt = datetime.fromisoformat(date_str)
        # タイムゾーン情報がない場合はUTCとみなす
        if parsed_dt.tzinfo is None:
            parsed_dt = parsed_dt.replace(tzinfo=timezone.utc)
            print(f"警告: 入力日付 '{date_str}' にタイムゾーン情報が含まれていません。UTCとして扱います。",
                  file=sys.stderr)
        return parsed_dt
    except ValueError:
        # YYYY-MM-DD 形式を試す (datetime.fromisoformatが日付のみを処理しない古いPythonバージョンの場合)
        try:
            parsed_date_only = date.fromisoformat(date_str)
            # 時刻部分を 00:00:00 としてdatetimeオブジェクトに変換し、UTCとする
            parsed_dt = datetime.combine(parsed_date_only, datetime.min.time(), tzinfo=timezone.utc)
            print(f"警告: 入力日付 '{date_str}' は日付のみです。時刻を00:00:00 UTCとして扱います。", file=sys.stderr)
            return parsed_dt
        except ValueError:
            return None  # どちらの形式でもパースできなかった場合


@app.command()
def get_date(
        date_str: Annotated[
            str | None,
            typer.Argument(
                help="フォーマットする日付文字列 (ISO 8601形式: 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS[+HH:MM]')。省略時は現在日時。")
        ] = None,
        time: Annotated[
            bool,
            typer.Option("-t", "--time", help="出力に時刻を含める。")
        ] = False,
        timezone_offset: Annotated[
            int | None,
            typer.Option("-z", "--timezone-offset",
                         help="UTCからのタイムゾーンオフセット(分単位)。例: 540 (JST), -60 (UTC-1)。入力文字列にオフセットがある場合はそちらが優先されます。")
        ] = None
):
    """
    指定された日付(または現在日時)を指定されたフォーマットとタイムゾーンで表示します。
    """
    parsed_date: datetime

    # 1. 日付文字列のパース
    if date_str:
        parsed_date_result = parse_date_string(date_str)
        if parsed_date_result is None:
            typer.echo(
                f"エラー: 無効な日付形式です: '{date_str}'。ISO 8601形式 (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS[+HH:MM]) で入力してください。",
                err=True)
            raise typer.Exit(code=1)
        parsed_date = parsed_date_result
    else:
        # 日付文字列が指定されていない場合は現在日時を使用 (UTC)
        parsed_date = datetime.now(timezone.utc)

    # 2. タイムゾーンオフセットの適用
    # 入力文字列にタイムゾーンが指定されておらず、かつオフセットオプションが指定されている場合のみ適用
    if (timezone_offset is not None
            and parsed_date.tzinfo is not None
            and parsed_date.tzinfo.utcoffset(parsed_date) is None
            and date_str is not None):
        print(
            f"情報: 入力日付 '{date_str}' にタイムゾーン情報がないため、指定されたオフセット {timezone_offset}分 を適用します。",
            file=sys.stderr)
        try:
            target_timezone = timezone(timedelta(minutes=timezone_offset))
            parsed_date = parsed_date.astimezone(target_timezone)
        except ValueError:
            typer.echo(f"エラー: 無効なタイムゾーンオフセット(分)です: {timezone_offset}", err=True)
            raise typer.Exit(code=1)
    elif timezone_offset is not None and date_str is None:
        # 日付入力がなく、オフセット指定がある場合は、現在時刻(UTC)にオフセットを適用
        try:
            target_timezone = timezone(timedelta(minutes=timezone_offset))
            parsed_date = parsed_date.astimezone(target_timezone)
        except ValueError:
            typer.echo(f"エラー: 無効なタイムゾーンオフセット(分)です: {timezone_offset}", err=True)
            raise typer.Exit(code=1)
    elif date_str is None and timezone_offset is None:
        # 日付入力もオフセット指定もない場合はローカルタイムゾーンを使用
        parsed_date = parsed_date.astimezone()

    # 3. 出力フォーマット
    output_format = "%Y-%m-%d"
    if time:
        if parsed_date.tzinfo is not None and parsed_date.tzinfo.utcoffset(parsed_date) is not None:
            output_format += " %H:%M:%S %Z%z"
        else:
            output_format += " %H:%M:%S"  # タイムゾーン情報がない場合

    formatted_date = parsed_date.strftime(output_format)

    # 4. 結果の表示
    typer.echo(formatted_date)


# スクリプトが直接実行された場合にTyperアプリケーションを実行
if __name__ == '__main__':
    app()
