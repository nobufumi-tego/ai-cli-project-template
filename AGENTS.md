# ai-cli-project-template

Claude Code / Gemini CLI / Codex CLI に対応した Python・LaTeX・Word プロジェクトの汎用雛形。
`scripts/init-project.py` を対話形式で実行するだけで、用途別の AGENTS.md・CLAUDE.md・GEMINI.md 等を自動生成する。
uv 同梱インストーラー・環境診断スクリプト付き。英語・日本語対応。

## Commands
```bash
python3 scripts/init-project.py     # プロジェクト初期化（対話形式）
python3 scripts/check-setup.py      # 環境診断（uv・Node.js・AI CLI の確認）
uv run python src/main.py           # メイン処理実行
uv run python src/visualize.py      # 可視化処理実行
uv run pytest tests/ -v             # テスト実行
uv run ruff check src/ tests/       # リント実行
uv run mypy src/                    # 型チェック実行
```

## Architecture
- `src/data/`       - データ読み込み・前処理モジュール
- `src/models/`     - モデル定義モジュール
- `src/evaluation/` - 評価・メトリクスモジュール
- `src/utils/`      - 共通ユーティリティ
- `src/main.py`     - メインエントリーポイント
- `src/visualize.py`- 可視化処理
- `scripts/`        - 初期化・診断スクリプト（`init-project.py`, `check-setup.py`）
- `configs/`        - ハイパーパラメータ・実験設定 YAML
- `data/raw/`       - 元データ（読み取り専用・git管理外）
- `data/processed/` - 加工済みデータ（git管理外）
- `notebooks/`      - 実験・分析用 Jupyter Notebook
- `tests/`          - テストコード
- `docs/`           - ユーザー向けドキュメント（JA / EN）
- `.claude/`        - Claude Code 設定（commands / skills / rules）
- `.gemini/`        - Gemini CLI 設定（commands）
- `.codex/`         - Codex CLI 設定（config.toml）

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
- `data/raw/` は `.gitignore` で除外されているため、クローン直後は空フォルダ。サンプルデータは別途配置すること
- `scripts/init-project.py` は対話形式のため、パイプ実行（`echo | python3 ...`）では動作しない
- `uv run` は `.venv/` が存在しない場合に自動作成するが、初回は時間がかかる
- GPU / CPU 環境でモデルの数値結果が微妙に異なる場合がある（テストは許容誤差を設定すること）

---
> このファイルは `scripts/init-project.py` で自動生成されます。
> 直接編集してプロジェクト固有の情報に育てていってください。
