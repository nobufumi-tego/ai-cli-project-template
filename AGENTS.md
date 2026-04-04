# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Commands
{{COMMANDS}}

## Architecture
{{ARCHITECTURE}}

## Conventions
- 型ヒント必須（Python 3.10+）
- すべての関数・クラスにdocstringを書く（Google スタイル）
- 数値の単位はコメントまたは変数名で明記（例: `duration_sec`, `size_mb`）
- マジックナンバーはすべて定数化（各モジュール先頭または `configs/` に定義）
- エラーハンドリングを省略しない
- `os.path` ではなく `pathlib.Path` を使う
- 絶対パスをハードコードしない

## Do / Don't
DO:
- 変更前に `uv run pytest` を実行して既存テストが通ることを確認する
- 新しい機能を追加したらテストも同時に追加する
- data/raw/ のファイルは読み取りのみ。加工結果は data/processed/ へ

DON'T:
- 大容量ファイル（動画・モデルチェックポイント等）をgit管理しない（.gitignore 設定済み）
- GPU/CPU環境依存のハードコードをしない
- data/raw/ のファイルを直接編集しない

## Watch out for
{{WATCH_OUT_FOR}}

---
> このファイルは `scripts/init-project.py` で自動生成されます。
> 直接編集してプロジェクト固有の情報に育てていってください。
