# ai-cli-project-template

Claude Code / Gemini CLI / Codex CLI に対応した Python・LaTeX・Word プロジェクトの汎用雛形。
`scripts/init-project.py` を実行するだけで、用途に合わせた AI 指示ファイルとプロジェクト構成が自動生成されます。

**対応 OS**: Windows 11 / macOS / Linux

## 前提条件

**Python は不要です。** uv が Python を自動管理します。必要なのは **git** と **uv** だけです。

### uv のインストール

→ **[uv_setup/README.md](uv_setup/README.md)** を参照してください。

| OS | 検証状況 |
|---|---|
| Windows 11 | ✅ 検証済み |
| Linux | ✅ 検証済み |
| macOS | 未検証 |

インストール後、以下で確認：
```bash
uv --version
git --version
```

---

## クイックスタート

### Step 1：リポジトリをクローン

git だけあれば OK です。

```bash
git clone https://github.com/<your-name>/<your-repo>.git
cd <your-repo>
```

---

### Step 2：uv をインストール

clone 直後は `uv` コマンドが使えないため、**先にインストールが必要**です。
`uv_setup/` に OS 別の検証済みスクリプトがあります（curl / PowerShell のみ必要）。

**Linux**
```bash
chmod +x uv_setup/install.sh
./uv_setup/install.sh
```

**Windows 11**（ダブルクリックまたは PowerShell から）
```bat
uv_setup\install.bat
```

> 詳細は **[uv_setup/README.md](uv_setup/README.md)** を参照してください。
> ※ `uv_setup/install.*` は uv + Python + ML 基本パッケージを一括セットアップします。
> uv だけ入れたい場合は `uv --version` で確認後、不要なパッケージは後から追加してください。

インストール後、**ターミナルを再起動**して確認：
```bash
uv --version   # バージョンが表示されれば OK
```

---

### Step 3：プロジェクトを初期化

```bash
uv run python scripts/init-project.py
```

対話形式で以下を設定します：
- プロジェクト種別の選択（8種類）
- プロジェクト名・説明の入力
- AGENTS.md・README.md 等を自動生成

## uv について

uv は Python のインストールからパッケージ管理まで一括で担うツールです。
**システムに Python がなくても、uv さえあれば動作します。**

```
uv run python scripts/init-project.py
↑ Python がなければ uv が自動でダウンロード・実行する
```

| OS | uv インストールコマンド |
|---|---|
| Windows 11 | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| macOS / Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

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
├── uv_setup/                     # ★ uv + Python 環境インストーラー（検証済み）
│   ├── install.sh                #   macOS / Linux
│   ├── install.ps1               #   Windows 11 (PowerShell)
│   ├── install.bat               #   Windows 11 (ダブルクリック)
│   └── README.md                 #   インストール手順
├── scripts/
│   └── init-project.py           # ★ 初期化スクリプト（プロジェクト種別設定）
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
