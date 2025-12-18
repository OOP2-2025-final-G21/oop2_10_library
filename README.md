# アプリ名:図書館/本の貸出管理システム
> アプリ名は、プロジェクトの顔でもあるので、適切な命名を行ってください。

概要:
> 図書館の貸出管理システムを作成します。
図書館を利用する会員情報や書籍情報，貸出状況などを管理します．

## アピールポイント

この部分に、発表に替わる内容を書きます。
アプリケーション動作のサンプル動画などを貼り付けられると良いです。
※動画の貼り付けは、GIFアニメーションなどでも可です。

## 動作条件: require

> 動作に必要な条件を書いてください。

```bash
必要なファイル / モジュール

models パッケージ:
initialize_database() 関数が存在し、呼び出し可能であること（DB 初期化／テーブル作成）。
routes パッケージ:
blueprints 変数が定義され、Flask の Blueprint オブジェクトのイテラブルであること。
index.html が存在していること（render_template が参照）。
他のテンプレートや静的ファイルは各 Blueprint に準拠。
実行時の動作（現在の app.py の設定）

Flask アプリを作成し、initialize_database() を呼び出す。
routes.blueprints にある Blueprint を全て登録する。
ルート "/" は index.html をレンダリングして返す。
開始設定: host='0.0.0.0', port=8080, debug=True
ポート 8080 が使用中だと起動に失敗する（Address already in use）。
想定されるエラーと対処

ModuleNotFoundError: peewee など依存が未インストール → pip でインストール
テンプレートが無い → index.html を作成
routes.blueprints が未定義または型不一致 → __init__.py を確認
ポート競合 → 別ポートで起動するか競合プロセスを停止
```

## 使い方: usage

> このリポジトリのアプリを動作させるために行う手順を詳細に書いてください。

```bash
$ python app.py
# Try accessing "http://localhost:8080" in your browser.
```
