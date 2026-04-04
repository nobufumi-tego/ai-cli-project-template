# ai-cli-project-template

Claude Code / Gemini CLI / Codex CLI に対応した Python プロジェクトの汎用雛形。
`scripts/init-project.py` を実行するだけで、用途に合わせた AI 指示ファイルとプロジェクト構成が自動生成されます。

## クイックスタート

```bash
# 1. このテンプレートからリポジトリを作成（GitHub の "Use this template" ボタン）
# 2. クローン
git clone https://github.com/<your-name>/<your-repo>.git
cd <your-repo>

# 3. 初期化スクリプトを実行（対話形式でプロジェクト情報を設定）
python scripts/init-project.py

# 4. 依存パッケージをインストール
uv sync

# 5. テスト実行で動作確認
uv run pytest tests/ -v
```

## 生成されるファイル

`init-project.py` を実行すると以下が上書き生成されます：

| ファイル | 内容 |
|---|---|
| `AGENTS.md` | 3ツール共通のプロジェクト指示書 |
| `CLAUDE.md` | Claude Code 用（`@AGENTS.md` インポート） |
| `GEMINI.md` | Gemini CLI 用（`@AGENTS.md` インポート） |
| `README.md` | プロジェクト概要（このファイルが上書きされます） |
| `pyproject.toml` | プロジェクト名・説明を更新 |

## テンプレートに含まれるもの

```
.
├── AGENTS.md                    # AI CLI 共通指示書（3ツール共通）
├── CLAUDE.md                    # Claude Code 用（@AGENTS.md）
├── GEMINI.md                    # Gemini CLI 用（@AGENTS.md）
├── scripts/
│   └── init-project.py          # ★ 初期化スクリプト
├── .claude/
│   ├── settings.json            # Hooks・権限設定
│   ├── commands/
│   │   ├── test-run.md          # /project:test-run コマンド
│   │   └── check-conventions.md # /project:check-conventions コマンド
│   ├── rules/
│   │   └── python-conventions.md # Python 規約詳細
│   └── skills/
│       └── ml-research/SKILL.md  # ML研究スキル（サンプル）
├── .gemini/commands/
├── .codex/
├── src/                         # ソースコード骨格
├── tests/                       # テスト骨格
├── notebooks/                   # Jupyter Notebook 用
├── data/
│   ├── raw/                     # 元データ（git管理外）
│   └── processed/               # 加工済みデータ
├── configs/                     # 設定ファイル（YAML）
└── pyproject.toml               # uv プロジェクト設定
```

## 対応プロジェクト種別

`init-project.py` の選択肢：

| No. | 種別 | 主な用途 |
|---|---|---|
| 1 | Python ML / AI 研究 | 機械学習・深層学習・実験管理 |
| 2 | データ分析 | pandas・Notebook・可視化 |
| 3 | Web API (FastAPI) | REST API・バックエンド |
| 4 | CLIツール | コマンドラインアプリ |
| 5 | Pythonライブラリ | パッケージ開発・公開 |
| 6 | カスタム | 全項目を手動入力 |

## 主なコマンド（生成後）

| コマンド | 内容 |
|---|---|
| `uv run pytest tests/ -v` | テスト実行 |
| `uv run ruff check src/ tests/` | リント |
| `uv run mypy src/` | 型チェック |
| `/project:test-run` | Claude Code でテスト実行＆サマリー |
| `/project:check-conventions` | Claude Code で規約チェック |

## セキュリティについて

- `.env` / `.env.*` はすべて `.gitignore` 済み
- `settings.local.json`（個人フック設定）は `.gitignore` 済み
- `data/raw/` は `.gitignore` 済み（元データをコミットしない）
- 大容量ファイル（`*.pt`, `*.pkl`, `*.mp4` 等）は `.gitignore` 済み

## ライセンス

MIT
