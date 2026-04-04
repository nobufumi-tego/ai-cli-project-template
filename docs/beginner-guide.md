# はじめてのセットアップガイド

コマンドラインを触ったことがない方向けの、丁寧な手順書です。
コマンドはすべてコピー＆ペーストして Enter を押すだけで進められます。

> **このガイドについて**
> 手順の数が多く、途中でつまずく可能性があります。
> 初回は**詳しい人に隣にいてもらうか、画面共有しながら進めること**を強くお勧めします。
> 一人で進める場合は、焦らず1ステップずつ確認しながら進めてください。

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

Git は「ファイルの変更履歴を管理するツール」です。プロジェクトのダウンロードにも使います。

まず確認してください：

```bash
git --version
```

「git version 2.xx.x」と表示されれば OK → **Step 2 へ**。

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

---

## Step 2：GitHub からリポジトリを取得する

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

ダウンロードが完了したら移動します：

```bash
cd <リポジトリ名>
```

> **`cd` とは？** 「Change Directory」の略。フォルダを移動するコマンドです。

---

## Step 3：uv をインストール

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

インストール後、**ターミナルを閉じて開き直し**、確認：
```bash
uv --version
```

詳細は [uv_setup/README.md](../uv_setup/README.md) を参照してください。

---

## Step 4：プロジェクトを初期化

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

## このテンプレートで学べること

このテンプレートは「動くものを作る」だけでなく、
**現代のソフトウェア開発で実際に使われる習慣とツール**を体験しながら学ぶことを意図しています。

### 1. 仕様を先に書く習慣（AGENTS.md）

> コードを書く前に「何を作るか・どう作るか」を言葉にする。

プロのエンジニアが設計書・要件定義書を書くのと同じ考え方です。
AI CLI を使わなくても、AGENTS.md はチームメンバーや将来の自分へのドキュメントになります。

**身につくこと：** 設計思考 / ドキュメントを書く習慣 / 「なんとなく作る」から脱却

### 2. バージョン管理（Git）

> 「昨日の状態に戻したい」「どこを変えたか確認したい」がいつでもできる。

Git は「タイムマシン」と「共同作業ツール」の両方です。
失敗を恐れずに試せるのは、いつでも元に戻せるからです。

**身につくこと：** 変更履歴の管理 / バックアップの概念 / チーム開発の基礎

### 3. 環境の再現性（uv）

> 「自分のパソコンでは動くのに、他の人のパソコンでは動かない」を防ぐ。

`pyproject.toml` と `uv.lock` により、どのパソコンでも同じ環境を再現できます。

**身につくこと：** 依存関係の管理 / 再現可能な環境の重要性 / チームでの開発準備

### 4. コード品質の自動チェック（Ruff・mypy）

> 「動けばいい」から「読みやすく・壊れにくいコードを書く」へ。

ファイルを保存するたびに Ruff が自動で実行されます（Hook 設定済み）。

**身につくこと：** コーディング規約の意味 / 静的解析の使い方 / 保守しやすいコードの書き方

### 5. AI との協働（Claude Code 等）

> AI はツール。何を作りたいかを伝えられる人間が主導する。

AGENTS.md に規約・構成・注意事項を育てることで、AI の出力の質が上がります。

**身につくこと：** プロンプトエンジニアリングの基礎 / AI 出力のレビュー能力 / 人間と AI の役割分担

### 段階的な学習パス

| 段階 | 目標 | 使うもの |
|---|---|---|
| 入門 | ターミナルに慣れる・Git でコミットできる | Git・VS Code |
| 初級 | プロジェクトを初期化して動かせる | uv・AGENTS.md |
| 中級 | テストを書いて規約を守れる | pytest・Ruff・mypy |
| 上級 | AI CLI と協働して開発サイクルを回せる | Claude Code |

どこから始めても構いません。「まず動かしてみる」ことが最初の一歩です。

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

`scripts/check-setup.py` の出力内容をそのままコピーして、以下のいずれかを試してください：

- エラーメッセージをそのまま検索エンジンで検索する
- 詳しい人に画面を見せる・画面共有する
- GitHub の Issues に投稿する
