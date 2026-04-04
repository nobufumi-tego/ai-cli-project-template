# ai-cli-project-template

Claude Code / Gemini CLI / Codex CLI に対応した Python・LaTeX・Word プロジェクトの汎用雛形。
`scripts/init-project.py` を実行するだけで、用途に合わせた AI 指示ファイルとプロジェクト構成が自動生成されます。

**対応 OS**: Windows 11 / macOS / Linux

## クイックスタート

```bash
# 1. このテンプレートからリポジトリを作成（GitHub の "Use this template" ボタン）

# 2. クローン
git clone https://github.com/<your-name>/<your-repo>.git
cd <your-repo>

# 3. 初期化スクリプトを実行（uv がなければ自動インストールを案内）
python  scripts/init-project.py   # Windows
python3 scripts/init-project.py   # macOS / Linux
```

スクリプトが対話形式で以下を設定します：
- プロジェクト種別の選択（8種類）
- プロジェクト名・説明の入力
- AGENTS.md・README.md 等を自動生成

## uv について

`scripts/init-project.py` は **uv がインストールされていなくても起動できます**。
Python プロジェクトを選択した場合、スクリプトが uv の有無を確認し、
未インストールであれば OS に応じてインストールを支援します。

| OS | 自動インストール方法 |
|---|---|
| Windows 11 | PowerShell の `irm \| iex` を使用 |
| macOS | curl でインストール（または `brew install uv`） |
| Linux | curl でインストール |

## 対応プロジェクト種別

| No. | 種別 | 必要ツール |
|---|---|---|
| 1 | Python ML / AI 研究 | uv（自動インストール対応） |
| 2 | データ分析 | uv（自動インストール対応） |
| 3 | Web API (FastAPI) | uv（自動インストール対応） |
| 4 | CLIツール | uv（自動インストール対応） |
| 5 | Pythonライブラリ | uv（自動インストール対応） |
| 6 | **LaTeX 論文執筆** | TeX Live / MiKTeX |
| 7 | **Word 論文執筆** | Microsoft Word / LibreOffice |
| 8 | カスタム（全項目手動入力） | 任意 |

## 生成されるファイル

`init-project.py` を実行すると以下が上書き生成されます：

| ファイル | Python | LaTeX | Word |
|---|---|---|---|
| `AGENTS.md` | ✓ | ✓ | ✓ |
| `CLAUDE.md` | ✓ | ✓ | ✓ |
| `GEMINI.md` | ✓ | ✓ | ✓ |
| `README.md` | ✓ | ✓ | ✓ |
| `pyproject.toml` | ✓ | — | — |
| `.gitignore`（LaTeX用パターン追記） | — | ✓ | — |
| `sections/` `figures/` `refs.bib` `.latexmkrc` | — | ✓（骨格作成） | — |
| `docs/` `figures/` `refs/` | — | — | ✓（骨格作成） |

## テンプレートに含まれるもの

```
.
├── AGENTS.md                     # AI CLI 共通指示書（3ツール共通）
├── CLAUDE.md                     # Claude Code 用（@AGENTS.md）
├── GEMINI.md                     # Gemini CLI 用（@AGENTS.md）
├── scripts/
│   └── init-project.py           # ★ 初期化スクリプト（OS自動判定・uv自動インストール対応）
├── .claude/
│   ├── settings.json             # Hooks・権限設定
│   ├── commands/
│   │   ├── test-run.md           # /project:test-run コマンド
│   │   └── check-conventions.md  # /project:check-conventions コマンド
│   ├── rules/
│   │   └── python-conventions.md # Python 規約詳細
│   └── skills/
│       └── ml-research/SKILL.md  # ML研究スキル（サンプル）
├── .gemini/commands/
├── .codex/
├── src/                          # ソースコード骨格（Python 向け）
├── tests/                        # テスト骨格
├── notebooks/                    # Jupyter Notebook 用
├── data/
│   ├── raw/                      # 元データ（git管理外）
│   └── processed/                # 加工済みデータ
├── configs/                      # 設定ファイル（YAML）
└── pyproject.toml                # uv プロジェクト設定
```

## セキュリティについて

- `.env` / `.env.*` はすべて `.gitignore` 済み
- `settings.local.json`（個人フック設定）は `.gitignore` 済み
- `data/raw/` は `.gitignore` 済み（元データをコミットしない）
- 大容量ファイル（`*.pt`, `*.pkl`, `*.mp4` 等）は `.gitignore` 済み
- `*.key` / `*.pem` / `credentials.json` は `.gitignore` 済み
- LaTeX の場合、コンパイル生成ファイルは `.gitignore` に自動追記

## ライセンス

MIT
