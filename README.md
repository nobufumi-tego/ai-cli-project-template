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

> **ターミナル（コマンドライン）とは？**
> キーボードで文字を入力してコンピュータを操作する画面です。
> マウスでアイコンをクリックするかわりに、コマンドを入力して作業します。
> このガイドの手順は、ターミナルにコマンドをコピー＆ペーストして Enter を押すだけで進められます。

---

### ターミナルの開き方

**Windows 11**
1. スタートボタンを右クリック
2. 「Windows PowerShell」または「ターミナル」をクリック

> ⚠️ 「管理者として実行」は不要です。通常ユーザーで開いてください。

**macOS**
1. Spotlight（`Command + Space`）を開く
2. 「ターミナル」と入力して Enter

**Linux**
- `Ctrl + Alt + T` を押す（Ubuntu 等）

---

### Step 1：Git をインストール

Git は「ファイルの変更履歴を管理するツール」です。プロジェクトのダウンロードにも使います。

まずターミナルで以下を入力して確認してください：

```bash
git --version
```

「git version 2.xx.x」のように表示されれば OK です → **Step 2 へ進んでください**。

何も表示されない・エラーが出る場合はインストールが必要です。

---

**Windows 11 の場合**

方法 A：コマンドでインストール（PowerShell に貼り付けて Enter）
```powershell
winget install --id Git.Git -e --source winget
```

> ⚠️ `winget` が見つからないと言われた場合は方法 B を使ってください。

方法 B：インストーラーを使う
1. https://git-scm.com/download/win を開く
2. 一番上のダウンロードリンクをクリック
3. ダウンロードされた `.exe` ファイルをダブルクリック
4. 「Next」を押し続けてデフォルト設定のままインストール

インストール後：**PowerShell を閉じて開き直し**、以下で確認
```powershell
git --version
```

---

**macOS の場合**

ターミナルで以下を実行：
```bash
xcode-select --install
```

ダイアログが出たら「インストール」をクリックして待つ（数分かかります）。

---

**Linux (Ubuntu / Debian) の場合**
```bash
sudo apt update && sudo apt install git
```

パスワードを聞かれたらログイン時のパスワードを入力してください（画面に表示されませんが入力されています）。

---

### Step 2：GitHub からリポジトリを取得する

> **GitHub とは？** プログラムのファイルをインターネット上で管理・共有するサービスです。
> このテンプレートも GitHub で公開されています。

**① GitHub アカウントを作る（持っていない場合）**

1. https://github.com を開く
2. 「Sign up」からアカウントを作成

**② このテンプレートをコピーする**

1. このリポジトリのページで「**Use this template**」ボタンをクリック
2. 「Create a new repository」を選択
3. リポジトリ名を入力して「Create repository」

**③ 自分のリポジトリをパソコンにダウンロードする**

作成されたリポジトリのページで「**Code**」→「**HTTPS**」の URL をコピーして、
ターミナルで以下を実行（URL は自分のものに変えてください）：

```bash
git clone https://github.com/<あなたのアカウント名>/<リポジトリ名>.git
```

ダウンロードが完了したら、そのフォルダに移動します：

```bash
cd <リポジトリ名>
```

> **`cd` とは？** 「Change Directory」の略で、フォルダを移動するコマンドです。
> `cd my-project` と入力すると `my-project` フォルダの中に入ります。

---

### Step 3：uv をインストール

uv は Python とパッケージを自動管理するツールです。
`uv_setup/` フォルダに OS 別の検証済みインストーラーが入っています。

**Windows 11 の場合**

エクスプローラーでクローンしたフォルダを開き、`uv_setup` フォルダの中の
`install.bat` を**ダブルクリック**してください。

> ⚠️ 「Windows によって PC が保護されました」というダイアログが出た場合：
> 「詳細情報」→「実行」をクリックしてください。

または PowerShell から：
```powershell
.\uv_setup\install.bat
```

**macOS / Linux の場合**

```bash
chmod +x uv_setup/install.sh
./uv_setup/install.sh
```

インストールが終わったら、**ターミナルを閉じて開き直し**、以下で確認：

```bash
uv --version
```

バージョン番号が表示されれば OK です。

> 詳細は **[uv_setup/README.md](uv_setup/README.md)** を参照してください。

---

### Step 4：プロジェクトを初期化

ターミナルでクローンしたフォルダにいることを確認して（`cd <リポジトリ名>` で移動）、
以下を実行：

```bash
uv run python scripts/init-project.py
```

質問が表示されるので、番号や文字を入力して Enter を押してください。

```
プロジェクト種別を選択してください：
  1. Python ML / AI 研究
  2. データ分析
  ...
番号を入力 [1]: 1          ← 入力して Enter

プロジェクト名（英語推奨） [my-project]: my-analysis    ← 入力して Enter
```

最後に「完了しました！」と表示されれば成功です。

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

## Claude Code でのプログラム開発例

### 起動

プロジェクトフォルダで以下を実行するだけです。

```bash
cd your-project
claude
```

Claude が `AGENTS.md` を自動で読み込み、プロジェクトの規約・構成を理解した状態で始まります。

---

### 基本的な使い方

**新機能の実装を依頼する**
```
src/data/loader.py に CSV を読み込む DataLoader クラスを実装してください。
AGENTS.md の規約に従い、型ヒントと docstring を付けてください。
```

**バグを修正させる**
```
uv run pytest を実行すると tests/test_loader.py でエラーが出ます。
[エラーメッセージをここに貼り付け]
原因を調べて修正してください。
```

**コードの説明を聞く**
```
src/models/trainer.py の train() メソッドの処理を説明してください。
```

**リファクタリングを依頼する**
```
src/utils/helper.py の関数が長くなってきました。
役割ごとにモジュールを分割してください。
```

---

### カスタムコマンド

このテンプレートには2つのカスタムコマンドが含まれています。

**テストを実行してサマリーを表示する**
```
/project:test-run
```

実行例：
```
✓ PASSED  tests/test_loader.py::test_load_csv
✓ PASSED  tests/test_loader.py::test_load_empty
✗ FAILED  tests/test_trainer.py::test_fit — AssertionError: expected 0.9, got 0.7
→ 修正方針：学習率が高すぎる可能性。LEARNING_RATE を 1e-3 → 1e-4 に下げて再試行。
```

**コードが規約に準拠しているかチェックする**
```
/project:check-conventions
```

実行例：
```
✓ 型ヒント: すべての関数に付いています
✗ docstring: src/models/trainer.py の fit() に docstring がありません
✗ 定数化: src/data/loader.py 12行目 — 32 をマジックナンバーで使用しています
→ 修正案を提示します...
```

---

### 実践的なワークフロー例

**① 朝の作業開始**
```
昨日の続きです。src/evaluation/ の実装を進めましょう。
まず現状を把握したいので、src/ の構成を説明してください。
```

**② 実装 → テスト → 修正のサイクル**
```
# 1. 実装
EarlyStopping クラスを src/models/callbacks.py に実装してください。

# 2. テスト確認
/project:test-run

# 3. 規約チェック
/project:check-conventions

# 4. 問題があれば修正
test_callbacks.py の失敗しているテストを修正してください。
```

**③ コミット前のレビュー**
```
今日の変更をコミットする前に、差分をレビューしてください。
問題があれば指摘してください。
```

**④ AGENTS.md を育てる**
```
今日の作業でわかったことを AGENTS.md の Watch out for に追記してください。
「DataLoader はファイルが存在しない場合 FileNotFoundError を raise する設計にする」
```

---

### VS Code との併用

VS Code で Claude Code 拡張機能を使う場合、エディタ上でファイルを開きながらチャットできます。

1. VS Code でプロジェクトフォルダを開く
2. サイドバーの Claude アイコンをクリック
3. 開いているファイルの内容を参照しながら指示できる

```
# ファイルを開いた状態で
このファイルの TODO コメントを実装してください。
```

## ライセンス

MIT
