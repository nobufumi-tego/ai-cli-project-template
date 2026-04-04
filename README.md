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

### Step 1：Git をインストール

Git はどの OS にも標準搭載されていません。まず確認してください：

```bash
git --version   # バージョンが表示されれば OK → Step 2 へ
```

インストールされていない場合は、OS に応じて以下を実行してください。

**Windows 11**

方法 A：winget（PowerShell または コマンドプロンプトで実行）
```powershell
winget install --id Git.Git -e --source winget
```

方法 B：公式インストーラー
1. https://git-scm.com/download/win を開く
2. インストーラーをダウンロードして実行（オプションはすべてデフォルトで OK）

インストール後は **PowerShell を再起動**して `git --version` で確認。

---

**macOS**

```bash
xcode-select --install   # Xcode Command Line Tools（git を含む）
```

または Homebrew 経由：
```bash
brew install git
```

---

**Linux (Ubuntu / Debian)**
```bash
sudo apt update && sudo apt install git
```

**Linux (Fedora / RHEL)**
```bash
sudo dnf install git
```

---

### Step 2：リポジトリをクローン

```bash
git clone https://github.com/<your-name>/<your-repo>.git
cd <your-repo>
```

---

### Step 3：uv をインストール

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

### Step 4：プロジェクトを初期化

```bash
uv run python scripts/init-project.py
```

対話形式で以下を設定します：
- プロジェクト種別の選択（8種類）
- プロジェクト名・説明の入力
- AGENTS.md・README.md 等を自動生成

---

### Step 5：VS Code をインストール（推奨）

> **このステップは省略できます。**
> お好みのエディタを使って構いません。
> ただし VS Code は Claude Code・Gemini CLI との統合機能があり、このテンプレートとの相性が良いため推奨します。

**Windows 11**
```powershell
winget install Microsoft.VisualStudioCode
```
インストール後は **PowerShell を再起動**してください。

**macOS**
```bash
brew install --cask visual-studio-code
```

**Linux (Ubuntu / Debian)**
```bash
sudo snap install code --classic
```

**Linux（snap が使えない場合）**
```bash
# Microsoft の apt リポジトリ経由
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update && sudo apt install code
```

インストール確認：
```bash
code --version
```

#### 推奨拡張機能

VS Code 起動後、以下の拡張機能をインストールすると快適に使えます。
`code --install-extension <ID>` でコマンドラインからインストールできます。

**AI・コーディング支援**

| 拡張機能 | ID | 用途 |
|---|---|---|
| Claude Code | `anthropic.claude-code` | Claude によるコード補完・AI 操作 |
| GitHub Copilot | `github.copilot` | GitHub AI コード補完（有料） |
| Continue | `continue.continue` | オープンソース AI コーディング支援 |

**Python 開発**

| 拡張機能 | ID | 用途 |
|---|---|---|
| Python | `ms-python.python` | Python 実行・デバッグ・テスト |
| Pylance | `ms-python.vscode-pylance` | 型チェック・高速補完 |
| Ruff | `charliermarsh.ruff` | 高速リンター（このテンプレートで使用） |
| Mypy Type Checker | `ms-python.mypy-type-checker` | 厳密な型チェック |
| Python Debugger | `ms-python.debugpy` | ブレークポイントデバッグ |

**データ・Notebook**

| 拡張機能 | ID | 用途 |
|---|---|---|
| Jupyter | `ms-toolsai.jupyter` | Notebook の編集・実行 |
| Rainbow CSV | `mechatroner.rainbow-csv` | CSV ファイルを色分け表示 |

**Git 管理**

| 拡張機能 | ID | 用途 |
|---|---|---|
| GitLens | `eamodio.gitlens` | Git 履歴・差分・blame の可視化 |
| Git Graph | `mhutchie.git-graph` | ブランチのグラフ表示 |

**ファイル・編集補助**

| 拡張機能 | ID | 用途 |
|---|---|---|
| YAML | `redhat.vscode-yaml` | YAML 補完・検証（configs/ 向け） |
| Markdown All in One | `yzhang.markdown-all-in-one` | AGENTS.md 等の Markdown 編集 |
| indent-rainbow | `oderwat.indent-rainbow` | インデントを色分け表示 |
| Better Comments | `aaron-bond.better-comments` | コメントを色分けして可読性向上 |

**LaTeX 論文執筆**（プリセット 6 を選んだ場合）

| 拡張機能 | ID | 用途 |
|---|---|---|
| LaTeX Workshop | `James-Yu.latex-workshop` | LaTeX 編集・PDF プレビュー・自動ビルド |
| LTeX | `valentjn.vscode-ltex` | 英語・日本語の文法・スペルチェック |

**リモート開発**（サーバー上で開発する場合）

| 拡張機能 | ID | 用途 |
|---|---|---|
| Remote - SSH | `ms-vscode-remote.remote-ssh` | SSH 接続先で VS Code を使う |
| WSL | `ms-vscode-remote.remote-wsl` | Windows の WSL 上で VS Code を使う |

一括インストール例（Python 開発向け）：
```bash
code --install-extension anthropic.claude-code \
     ms-python.python \
     ms-python.vscode-pylance \
     charliermarsh.ruff \
     ms-toolsai.jupyter \
     eamodio.gitlens \
     yzhang.markdown-all-in-one
```

---

### Step 6：AI CLI をインストール（任意）


> **このステップは省略できます。**
> AI CLI がなくてもプロジェクトは通常通り使えます。
> `AGENTS.md` はプロジェクト仕様書・規約書として人間が読む文書としても機能します。
> AI CLI を使う場合にのみ、以下をインストールしてください。

Claude Code・Gemini CLI・Codex CLI はすべて **Node.js** が必要です。
使いたいツールだけインストールすれば OK です。

#### Node.js のインストール

まず確認：
```bash
node --version   # v18 以上であれば OK → CLI インストールへ
```

インストールされていない場合：

**Windows 11**
```powershell
winget install OpenJS.NodeJS.LTS
```
インストール後は **PowerShell を再起動**してください。

**macOS**
```bash
brew install node
```
Homebrew 未導入の場合は https://brew.sh を参照してください。

**Linux (Ubuntu / Debian)**
```bash
# NodeSource 経由（apt の標準版は古いため非推奨）
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

**Linux (Fedora / RHEL)**
```bash
sudo dnf install nodejs
```

インストール確認：
```bash
node --version
npm --version
```

---

#### Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

初回認証（Anthropic アカウントが必要）：
```bash
claude   # ブラウザが開き、ログイン画面が表示される
```

---

#### Gemini CLI

```bash
npm install -g @google/gemini-cli
```

初回認証（Google アカウントが必要）：
```bash
gemini   # ブラウザが開き、ログイン画面が表示される
```

---

#### Codex CLI

```bash
npm install -g @openai/codex
```

OpenAI API キーを環境変数に設定：

**Windows 11**（PowerShell）
```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
```

**macOS / Linux**（`~/.bashrc` または `~/.zshrc` に追記）
```bash
export OPENAI_API_KEY="sk-..."
```

---

#### インストール確認

```bash
claude --version
gemini --version
codex --version
```

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
