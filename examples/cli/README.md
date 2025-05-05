# Creating CLI applications with Typer

このコードは、Typerのシンプルで宣言的な方法でCLIを構築できます。

## Run command

```
$ python main.py
$ python main.py "2023-10-27"
$ python main.py "2023-10-27T15:30:00"
$ python main.py --time
$ python main.py "2023-10-27" --time
$ python main.py --timezone-offset 60 # UTC+1
$ python main.py --time --timezone-offset -120 # UTC-2
$ python main.py "2023-10-27T10:00:00+09:00" -t # JST
$ python main.py "2023-10-27T10:00:00" -t -z 540 # JST (UTC+9)
```

## Ref

- https://wanago.io/2024/02/05/api-nestjs-cli-nest-commander/
