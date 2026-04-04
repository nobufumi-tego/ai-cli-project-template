# ai-cli-project-template

🇬🇧 [English README](README.en.md)

Claude Code / Gemini CLI / Codex CLI に対応した Python・LaTeX・Word プロジェクトの汎用雛形。
`scripts/init-project.py` を対話形式で実行するだけで、用途別の AGENTS.md・CLAUDE.md・GEMINI.md 等を自動生成します。

**対応 OS**: Windows 11 / macOS / Linux

---

### 対象読者

| 対象 | 案内先 |
|---|---|
| ターミナルの基本操作（`cd`・コマンドの実行）ができる方 | このページをそのまま読み進めてください |
| コマンドラインを触ったことがない方 | [はじめてのセットアップガイド (JA)](docs/beginner-guide.md) / [(EN)](docs/beginner-guide.en.md) |

> **完全なコマンド初心者の方へ：**
> セットアップには複数ツールのインストールが必要です。
> 初回は対面サポートや動画ガイドの併用を推奨します。
> まず [`scripts/check-setup.py`](#環境診断スクリプト) を実行すると、何が足りないかを自動で確認できます。

---

## 対応 AI CLI

| AI CLI | 提供元 | 対応ファイル | 用途 |
|---|---|---|---|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) | Anthropic | `CLAUDE.md` `.claude/` | コード生成・リファクタリング・テスト |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google | `GEMINI.md` `.gemini/` | コード生成・ドキュメント作成 |
| [Codex CLI](https://github.com/openai/codex) | OpenAI | `AGENTS.md` `.codex/` | コード生成・自動化 |

3ツールは **`AGENTS.md` を共通の指示書**として使います。
`CLAUDE.md` と `GEMINI.md` は `@AGENTS.md` の1行だけで、内容は `AGENTS.md` に集約されます。

```
AGENTS.md を更新するだけで 3ツールすべてに反映される
```

---

## クイックスタート

```bash
# 1. Git・uv をインストール（uv_setup/ 参照）
./uv_setup/install.sh        # macOS / Linux
.\uv_setup\install.bat       # Windows 11

# 2. クローン
git clone https://github.com/<your-name>/<your-repo>.git
cd <your-repo>

# 3. 環境確認（何が足りないか自動診断）
python  scripts/check-setup.py   # Windows
python3 scripts/check-setup.py   # macOS / Linux

# 4. 初期化（対話形式）
uv run python scripts/init-project.py
```

## 環境診断スクリプト

`scripts/check-setup.py` は Git・uv・Python・VS Code・AI CLI の有無を一括確認し、
不足しているもののインストール方法を表示します。
**Python のみで動作します（uv・外部パッケージ不要）。**

```
======================================================
  セットアップ確認スクリプト
======================================================
【必須】
  ✓  Git: git version 2.39.5
  ✓  uv: uv 0.11.2
  ✓  Python 3.12.13
【推奨】
  ✓  VS Code: 1.114.0
【AI CLI（任意）】
  ✓  Node.js: v24.0.0
  ✓  Claude Code: 2.1.92
  ✗  Gemini CLI が見つかりません（任意）
       インストール方法: npm install -g @google/gemini-cli
  ...
======================================================
  ✓ 必須ツールはすべて揃っています。
  次のステップ: uv run python scripts/init-project.py
======================================================
```

---

## 対応プロジェクト種別

| No. | 種別 | 必要ツール |
|---|---|---|
| 1 | Python ML / AI 研究 | uv |
| 2 | データ分析 | uv |
| 3 | Web API (FastAPI) | uv |
| 4 | CLIツール | uv |
| 5 | Pythonライブラリ | uv |
| 6 | LaTeX 論文執筆 | TeX Live / MiKTeX |
| 7 | Word 論文執筆 | Word / LibreOffice |
| 8 | カスタム | 任意 |

生成後の `AGENTS.md` の完成形は [docs/example-agents.md](docs/example-agents.md) で確認できます。

---

## 生成されるファイル

| ファイル | Python | LaTeX | Word |
|---|---|---|---|
| `AGENTS.md` | ✓ | ✓ | ✓ |
| `CLAUDE.md` | ✓ | ✓ | ✓ |
| `GEMINI.md` | ✓ | ✓ | ✓ |
| `README.md` | ✓ | ✓ | ✓ |
| `pyproject.toml` | ✓ | — | — |
| `.gitignore`（LaTeX 用追記） | — | ✓ | — |
| `sections/` `figures/` `refs.bib` `.latexmkrc` | — | ✓ | — |
| `docs/` `figures/` `refs/` | — | — | ✓ |

---

## リポジトリ構成

```
.
├── AGENTS.md                     # AI CLI 共通指示書
├── CLAUDE.md / GEMINI.md         # 各 CLI 用（@AGENTS.md を読み込み）
├── uv_setup/                     # uv + Python 環境インストーラー（検証済み）
│   ├── install.sh / install.bat  #   OS 別インストーラー
│   └── README.md
├── scripts/
│   └── init-project.py           # プロジェクト初期化スクリプト
├── .claude/
│   ├── settings.json             # Hooks・権限設定
│   ├── commands/
│   │   ├── test-run.md           # /project:test-run
│   │   └── check-conventions.md  # /project:check-conventions
│   ├── rules/python-conventions.md
│   └── skills/ml-research/SKILL.md
├── .gemini/commands/
├── .codex/
│   └── config.toml               # Codex CLI 設定（モデル・サンドボックス・MCP）
├── src/ tests/ notebooks/ data/ configs/
├── docs/
│   ├── beginner-guide.md         # 初心者向けセットアップガイド
│   └── example-agents.md         # AGENTS.md 生成サンプル
└── pyproject.toml
```

---

## AI CLI のインストール（任意）

AI CLI がなくても手動でプロジェクトを開発できます。使いたいものだけ導入してください。

```bash
# Node.js が必要（winget install OpenJS.NodeJS.LTS など）
npm install -g @anthropic-ai/claude-code   # Claude Code
npm install -g @google/gemini-cli          # Gemini CLI
npm install -g @openai/codex               # Codex CLI
```

初回認証：`claude`（Anthropic）、`gemini`（Google）、Codex は `OPENAI_API_KEY` 環境変数。

---

## Claude Code での開発

```bash
cd your-project && claude
```

```
# 実装依頼例
src/data/loader.py に DataLoader クラスを実装してください。

# カスタムコマンド
/project:test-run           # テスト実行 → サマリー
/project:check-conventions  # 規約チェック
```

---

## セキュリティ

`.env` / `*.key` / `*.pem` / `credentials.json` / `data/raw/` / `settings.local.json` /
大容量ファイル（`*.pt` `*.pkl` `*.mp4`）はすべて `.gitignore` 済み。

---

## ライセンス

MIT
