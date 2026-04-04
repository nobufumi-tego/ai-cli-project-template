# はじめてのセットアップガイド

コマンドラインを触ったことがない方向けの、丁寧な手順書です。
コマンドはすべてコピー＆ペーストして Enter を押すだけで進められます。

> **スクリプトの安全性について**
> このガイドで実行するスクリプトは、**システムファイルを変更しません**。
> 書き込み先はホームフォルダ内のみで、`sudo`（管理者権限）も不要です。
> 最悪の場合でもエラーメッセージが表示されるだけで、PC が壊れることはありません。
> やり直したいときは [docs/recovery.md](recovery.md) を参照してください。

> **このガイドについて**
> 手順の数が多く、途中でつまずく可能性があります。
> 初回は**詳しい人に隣にいてもらうか、画面共有しながら進めること**を強くお勧めします。
> 一人で進める場合は、焦らず1ステップずつ確認しながら進めてください。

---

## このセットアップで身につくこと

手順をこなすだけでなく、**プロのエンジニアが毎日使う習慣とコマンドの型**を自然に体験します。

| ステップ | 身につくコマンドの型 | 意味 |
|---|---|---|
| Step 1 | `ツール名 --version` | 「このツールは入っている？」の確認方法 |
| Step 2 | `git clone URL` / `cd フォルダ名` | ファイルのダウンロードと移動 |
| Step 3 | `./install.sh` / `uv --version` | スクリプトの実行と確認 |
| Step 4 | `uv run python スクリプト名` | 環境を指定してプログラムを動かす |
| Step 5以降 | VS Code / AI CLI の起動 | 開発ツールの日常的な使い方 |

> **コマンドには「型」がある**
> `ツール名 動詞 対象` という構造が多く、覚えたパターンは他のツールにも転用できます。
> Step ごとに「いま何を学んでいるか」を意識して進めると、後で応用できる知識になります。

### 今日のゴール（段階的な学習パス）

| 段階 | 目標 | 使うもの |
|---|---|---|
| **入門（今日）** | **ターミナルに慣れる・セットアップを完了できる** | **Git・uv・このガイド** |
| 初級 | プロジェクトを初期化して動かせる | uv・AGENTS.md |
| 中級 | テストを書いて規約を守れる | pytest・Ruff・mypy |
| 上級 | AI CLI と協働して開発サイクルを回せる | Claude Code |

**今日は「入門」の完了が目標**です。焦らず進めてください。

---

## まず環境診断を実行してください

Git のインストール後、以下のコマンドで「何が揃っていて何が足りないか」を確認できます。

```bash
python  scripts/check-setup.py   # Windows
python3 scripts/check-setup.py   # macOS / Linux
```

何が足りないかと、インストール方法が自動で表示されます。
**エラーが出たときは、このコマンドの出力内容をそのままコピーして検索するか、詳しい人に見せてください。**

---

## ターミナルとは？

キーボードで文字を入力してコンピュータを操作する画面です。
マウスでアイコンをクリックするかわりに、コマンドを入力して作業します。

**ターミナルの開き方**

| OS | 開き方 |
|---|---|
| Windows 11 | スタートボタンを右クリック →「Windows PowerShell」または「ターミナル」 |
| macOS | `Command + Space` → 「ターミナル」と入力して Enter |
| Linux | `Ctrl + Alt + T` |

> ⚠️ Windows では「管理者として実行」は不要です。通常ユーザーで開いてください。

---

## Step 1：Git をインストール

> **このステップで学ぶこと：**
> `ツール名 --version` というコマンドの型。これは「このツールが入っているか確認する」万能パターンです。
> `git`・`uv`・`python`・`node` など、あらゆるツールで同じように使えます。

Git は「ファイルの変更履歴を管理するツール」です。プロジェクトのダウンロードにも使います。

まず確認してください：

```bash
git --version
```

**期待される出力：**
```
git version 2.xx.x
```

この形式で表示されれば OK → **Step 2 へ**。

表示されない場合は以下を実行してください。

**Windows 11**

方法 A：コマンドでインストール
```powershell
winget install --id Git.Git -e --source winget
```
> ⚠️ `winget` が見つからない場合は方法 B を使ってください。

方法 B：公式インストーラー
1. https://git-scm.com/download/win を開く
2. インストーラーをダウンロードして実行
3. 「Next」を押し続けてデフォルト設定のままインストール

インストール後は **PowerShell を閉じて開き直し**、`git --version` で確認。

**macOS**
```bash
xcode-select --install
```
ダイアログが出たら「インストール」をクリック（数分かかります）。

**Linux (Ubuntu / Debian)**
```bash
sudo apt update && sudo apt install git
```
パスワードを聞かれたらログインパスワードを入力（画面に表示されませんが入力されています）。

> 💡 **コマンドの読み方：`sudo apt update && sudo apt install git`**
> `sudo` = 管理者権限で実行 / `apt` = パッケージ管理ツール / `&&` = 前が成功したら次を実行
> 「管理者権限でパッケージ情報を更新し、続けて git をインストール」という意味です。

---

## Step 2：GitHub からリポジトリを取得する

> **このステップで学ぶこと：**
> `git clone`（ダウンロード）と `cd`（フォルダ移動）。
> この2つはセットで使う基本操作です。

**GitHub とは？** プログラムのファイルをインターネット上で管理・共有するサービスです。

**① GitHub アカウントを作る（持っていない場合）**
1. https://github.com を開く
2. 「Sign up」からアカウントを作成

**② このテンプレートをコピーする**
1. このリポジトリのページで「**Use this template**」ボタンをクリック
2. 「Create a new repository」を選択
3. リポジトリ名を入力して「Create repository」

**③ パソコンにダウンロードする**

作成されたリポジトリのページで「**Code**」→「**HTTPS**」の URL をコピーして実行：

```bash
git clone https://github.com/<あなたのアカウント名>/<リポジトリ名>.git
```

**期待される出力：**
```
Cloning into '<リポジトリ名>'...
remote: Enumerating objects: ...
Receiving objects: 100% ...
```

ダウンロードが完了したら移動します：

```bash
cd <リポジトリ名>
```

> 💡 **コマンドの読み方：`cd <リポジトリ名>`**
> `cd` = "Change Directory"（ディレクトリを変える）の略。フォルダを移動するコマンドです。
> **現在どこにいるかを確認するには：**
> ```bash
> pwd          # macOS / Linux：現在のフォルダのパスが表示される
> cd           # Windows：現在のフォルダのパスが表示される
> ```
> ターミナルで迷子になったときはこのコマンドで現在地を確認できます。

---

## Step 3：uv をインストール

> **このステップで学ぶこと：**
> スクリプトを実行してツールをインストールする方法と、`--version` で確認する習慣。

uv は Python とパッケージを自動管理するツールです。
`uv_setup/` フォルダに OS 別の検証済みインストーラーが入っています。

**Windows 11**

エクスプローラーで `uv_setup` フォルダを開き、`install.bat` を**ダブルクリック**。

> ⚠️ 「Windows によって PC が保護されました」と出た場合：「詳細情報」→「実行」

または PowerShell から：
```powershell
.\uv_setup\install.bat
```

**macOS / Linux**
```bash
chmod +x uv_setup/install.sh
./uv_setup/install.sh
```

> 💡 **コマンドの読み方：`chmod +x` と `./`**
> `chmod +x ファイル名` = 「このファイルを実行できるようにする」許可設定。
> `./ファイル名` = 「現在のフォルダにあるこのファイルを実行する」という意味です。

インストール後、**ターミナルを閉じて開き直し**、確認：
```bash
uv --version
```

**期待される出力：**
```
uv 0.x.x (...)
```

詳細は [uv_setup/README.md](../uv_setup/README.md) を参照してください。

---

## Step 4：プロジェクトを初期化

> **このステップで学ぶこと：**
> `uv run python スクリプト名` というパターン。
> `uv run` を前に付けることで「uv が管理する環境の Python で実行する」という意味になります。
> これがこのテンプレートの基本的なプログラム実行方法です。

クローンしたフォルダ内で実行：

```bash
uv run python scripts/init-project.py
```

質問が表示されるので、番号や文字を入力して Enter を押してください：

```
プロジェクト種別を選択してください：
  1. Python ML / AI 研究
  2. データ分析
  ...
番号を入力 [1]: 1            ← 入力して Enter

プロジェクト名 [my-project]: my-analysis   ← 入力して Enter
```

「完了しました！」と表示されれば成功です。

> 💡 **いま何が起きたか**
> `AGENTS.md`・`CLAUDE.md`・`README.md` などのファイルが自動生成されました。
> 生成されたファイルを VS Code で開いて中を見てみましょう。
> AI CLI への指示書（`AGENTS.md`）がどんな内容になっているか確認するのがおすすめです。

---

## Step 5：VS Code をインストール（推奨）

> 省略可能です。お好みのエディタを使っても構いません。

**Windows 11**
```powershell
winget install Microsoft.VisualStudioCode
```

**macOS**
```bash
brew install --cask visual-studio-code
```

**Linux (Ubuntu)**
```bash
sudo snap install code --classic
```

### 推奨拡張機能

| カテゴリ | 拡張機能 | ID |
|---|---|---|
| AI支援 | Claude Code | `anthropic.claude-code` |
| AI支援 | Continue | `continue.continue` |
| Python | Python | `ms-python.python` |
| Python | Pylance | `ms-python.vscode-pylance` |
| Python | Ruff | `charliermarsh.ruff` |
| Python | Mypy Type Checker | `ms-python.mypy-type-checker` |
| Notebook | Jupyter | `ms-toolsai.jupyter` |
| Git | GitLens | `eamodio.gitlens` |
| Git | Git Graph | `mhutchie.git-graph` |
| 編集補助 | Markdown All in One | `yzhang.markdown-all-in-one` |
| 編集補助 | indent-rainbow | `oderwat.indent-rainbow` |
| LaTeX | LaTeX Workshop | `James-Yu.latex-workshop` |
| リモート | Remote - SSH | `ms-vscode-remote.remote-ssh` |

Python 開発向け一括インストール：
```bash
code --install-extension anthropic.claude-code \
     ms-python.python ms-python.vscode-pylance \
     charliermarsh.ruff ms-toolsai.jupyter \
     eamodio.gitlens yzhang.markdown-all-in-one
```

---

## Step 6：AI CLI をインストール（任意）

> 省略可能です。AI CLI がなくても手動でプロジェクトを開発できます。
> `AGENTS.md` は人間が読む仕様書としても機能します。

すべての AI CLI に **Node.js** が必要です。

### Node.js のインストール

確認：
```bash
node --version   # v18 以上であれば OK
```

**Windows 11**
```powershell
winget install OpenJS.NodeJS.LTS
```

**macOS**
```bash
brew install node
```

**Linux (Ubuntu)**
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

### Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude   # ブラウザが開き、Anthropic アカウントでログイン
```

### Gemini CLI

```bash
npm install -g @google/gemini-cli
gemini   # ブラウザが開き、Google アカウントでログイン
```

### Codex CLI

```bash
npm install -g @openai/codex
```

OpenAI API キーを設定：

**Windows 11**（PowerShell）
```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
```

**macOS / Linux**（`~/.bashrc` または `~/.zshrc` に追記）
```bash
export OPENAI_API_KEY="sk-..."
```

---

## セットアップ完了！次のステップ

ここまで来たあなたは、以下のコマンドを自然に使えるようになっています：

| コマンド | 使えるようになったこと |
|---|---|
| `ツール名 --version` | ツールのインストール確認 |
| `git clone URL` | リポジトリのダウンロード |
| `cd フォルダ名` | ターミナルでのフォルダ移動 |
| `pwd` | 現在地の確認 |
| `uv run python ファイル名` | uv 環境でのプログラム実行 |

**次にやること：**

1. `AGENTS.md` を開いて、自分のプロジェクトの説明に書き換える
2. VS Code でプロジェクトフォルダを開く（`code .` で開けます）
3. `uv run pytest` でテストが通ることを確認する

> 💡 **`code .` とは？**
> 「現在のフォルダを VS Code で開く」コマンドです。
> `.` は「現在のフォルダ」を意味します。これも多くのコマンドで共通して使えるパターンです。

---

## Claude Code での開発例

### 起動

```bash
cd your-project
claude
```

`AGENTS.md` を自動読み込みして、プロジェクトの規約・構成を理解した状態で始まります。

### 基本的な使い方

```
# 新機能の実装
src/data/loader.py に CSV を読み込む DataLoader クラスを実装してください。
型ヒントと docstring を付けてください。

# バグ修正
uv run pytest でエラーが出ます。[エラーメッセージ] 原因を調べて修正してください。

# コードの説明
src/models/trainer.py の train() メソッドを説明してください。
```

### カスタムコマンド

```
/project:test-run          # テスト実行 → サマリー表示
/project:check-conventions # 規約チェック（型ヒント・docstring 等）
```

### 典型的な開発サイクル

```
実装依頼 → /project:test-run → /project:check-conventions → 修正 → git commit
```

### AGENTS.md を育てる

```
今日の作業でわかったことを AGENTS.md の Watch out for に追記してください。
「DataLoader はファイルが存在しない場合 FileNotFoundError を raise する設計にする」
```

---

## よくあるエラーと対処法

### 「winget が見つかりません」（Windows）

Windows 10 以前、または古い Windows 11 では winget が入っていないことがあります。

**対処法：** 公式インストーラーを使う（各 Step の「方法 B」を参照）

---

### 「Windows によって PC が保護されました」（Windows）

`install.bat` や `.exe` をダブルクリックしたときに表示されます。

**対処法：**
1. 「詳細情報」をクリック
2. 「実行」をクリック

これはインターネットからダウンロードしたファイルへの Windows の警告です。
このリポジトリのファイルは安全ですが、不安な場合は詳しい人に確認してください。

---

### コマンドを入力しても「見つかりません」と表示される

インストール後にターミナルを**開き直していない**ことが原因の大半です。

**対処法：** ターミナルを閉じて、もう一度開いてから同じコマンドを実行する

---

### `uv run python scripts/check-setup.py` でエラーが出る

**対処法：**
1. `uv --version` を実行して uv がインストールされているか確認する
2. 表示されない場合は Step 3（uv のインストール）をやり直す
3. 表示される場合は、ターミナルがリポジトリのフォルダにいるか確認する
   ```bash
   # 現在の場所を確認
   pwd          # macOS / Linux
   cd           # Windows（現在のパスが表示される）
   ```

---

### パスワードを入力しても反応しない（macOS / Linux）

`sudo` コマンド実行時、パスワードを入力しても画面に何も表示されません。
これは**正常な動作**です。見えていないだけで入力されています。
そのまま入力して Enter を押してください。

---

### それでも解決しない場合

**まず生成 AI に聞く（推奨）**

Claude・Gemini・ChatGPT はこういったエラーの解決が得意です。以下のプロンプトをコピーして、エラー情報を埋めて貼り付けるだけで手順を教えてくれます。

| AI | 無料で使えるサービス |
|---|---|
| Claude | https://claude.ai |
| Gemini | https://gemini.google.com |
| ChatGPT | https://chatgpt.com |

**貼り付け用プロンプト（コピーして使ってください）：**

```
開発環境のセットアップ中にエラーが発生しました。解決方法を教えてください。

【OS】
（例：Windows 11 / macOS Sequoia / Ubuntu 22.04）

【実行したコマンド】
（例：uv run python scripts/init-project.py）

【エラーメッセージ】
（ここにエラーをそのまま貼り付け）

【環境診断スクリプトの出力】
（以下のコマンドを実行して出力をここに貼り付け）
python  scripts/check-setup.py   # Windows
python3 scripts/check-setup.py   # macOS / Linux
```

> **ポイント：** エラーメッセージと `check-setup.py` の出力を両方貼ると、AI が原因を特定しやすくなります。「英語でもいいので解決手順を日本語で教えて」と添えると親切な回答が返ってきます。

---

それでも解決しない場合は：

- 詳しい人に画面を見せる・画面共有する
- [GitHub Discussions](https://github.com/nobufumi-tego/ai-cli-project-template/discussions) に投稿する（`check-setup.py` の出力を必ず添付）
