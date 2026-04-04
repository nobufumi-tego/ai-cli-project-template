# インストールを元に戻す手順 / Recovery Guide

このガイドでインストールしたツールを安全に削除する方法です。
How to safely remove the tools installed by this guide.

> **重要 / Important**
> このテンプレートのスクリプトは**ユーザー領域のみ**に書き込みます。
> システムファイル（Windows・macOS・Linux のコアファイル）は変更しません。
> / The scripts in this template write **only to user space**.
> They do not modify system files.

---

## 1. クローンしたリポジトリを削除する

セットアップで何か問題が起きた場合、まずこれだけで十分なことが多いです。

```bash
# macOS / Linux
rm -rf <リポジトリ名>

# Windows（PowerShell）
Remove-Item -Recurse -Force <リポジトリ名>
```

またはエクスプローラーでフォルダを右クリック → 削除。

---

## 2. uv をアンインストールする

uv は `~/.local/bin/` 以下（macOS/Linux）または `%USERPROFILE%\.local\bin\`（Windows）に
インストールされています。システムには干渉しません。

**macOS / Linux**
```bash
# uv 自身のアンインストールコマンド（uv 0.5+ で利用可能）
uv self uninstall

# 上記が動かない場合：手動削除
rm -f ~/.local/bin/uv ~/.local/bin/uvx

# ~/.bashrc または ~/.zshrc から以下の行を削除する
# . "$HOME/.local/bin/env"
```

**Windows（PowerShell）**
```powershell
# uv 自身のアンインストールコマンド
uv self uninstall

# 上記が動かない場合：手動削除
Remove-Item "$env:USERPROFILE\.local\bin\uv.exe" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.local\bin\uvx.exe" -Force -ErrorAction SilentlyContinue
```

---

## 3. Node.js をアンインストールする（AI CLI を入れた場合）

**Windows**
```powershell
winget uninstall OpenJS.NodeJS.LTS
```

**macOS（Homebrew でインストールした場合）**
```bash
brew uninstall node
```

**Linux (Ubuntu / Debian)**
```bash
sudo apt remove nodejs
```

---

## 4. AI CLI をアンインストールする

```bash
npm uninstall -g @anthropic-ai/claude-code   # Claude Code
npm uninstall -g @google/gemini-cli          # Gemini CLI
npm uninstall -g @openai/codex               # Codex CLI
```

---

## 5. Git をアンインストールする（通常は不要）

Git はほかの開発作業でも広く使われるため、通常は残しておいて問題ありません。

**Windows**
```powershell
winget uninstall Git.Git
```

**macOS（xcode-select でインストールした場合）**
```bash
sudo rm -rf /Library/Developer/CommandLineTools
```

**Linux (Ubuntu / Debian)**
```bash
sudo apt remove git
```

---

## 6. PATH の設定を元に戻す（必要な場合）

uv のインストールは `~/.bashrc` や `~/.zshrc` に1行追加します。
エディタで開いて削除してください。

```bash
# 追加された行の例（この行を削除する）
. "$HOME/.local/bin/env"
```

変更後にターミナルを再起動するか、以下を実行：
```bash
source ~/.bashrc   # または ~/.zshrc
```

---

## うまくいかない場合

`scripts/check-setup.py` の出力をコピーして
[GitHub Issues](https://github.com/nobufumi-tego/ai-cli-project-template/issues/new/choose)
または
[GitHub Discussions](https://github.com/nobufumi-tego/ai-cli-project-template/discussions)
に投稿してください。

---

# Recovery Guide (English)

## What the scripts actually touch

| Tool | Install location | System files modified? |
|---|---|---|
| uv | `~/.local/bin/uv` (macOS/Linux) / `%USERPROFILE%\.local\bin\uv.exe` (Windows) | No |
| Node.js | System package manager | No |
| Git | System package manager | No |
| AI CLIs | npm global packages (`~/.npm/` or system npm prefix) | No |
| Python (via uv) | `~/.uv/python/` | No |
| Project files | Cloned folder only | No |

**Nothing this template installs can prevent your OS from booting or break system applications.**
The worst case is a confused terminal environment, which is fully recoverable by following the steps above.

## Quick recovery for "terminal looks broken"

The most common issue is commands not found after installation. Fix:

1. **Close and reopen your terminal** — this reloads PATH
2. Run `python3 scripts/check-setup.py --lang en` to see what's missing
3. If still broken, delete the cloned folder and start over from Step 1

## Full uninstall (start fresh)

```bash
# 1. Remove the project
rm -rf <repository-name>

# 2. Uninstall uv
uv self uninstall   # or delete ~/.local/bin/uv manually

# 3. Remove PATH entry from ~/.bashrc or ~/.zshrc
#    Delete the line: . "$HOME/.local/bin/env"

# 4. Restart terminal
```

That's all. Your system will be exactly as it was before.
