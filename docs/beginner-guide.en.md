# Beginner Setup Guide

A step-by-step guide for people who have never used the command line before.
Every command can be run by copy-pasting it and pressing Enter.

> **About script safety**
> The scripts in this guide **do not modify system files**.
> All writes go inside your home folder only.
> `sudo` (admin access) is required only on Linux / WSL2 when running `install.sh` (for the libgomp system library).
> In the worst case, you'll see an error message. Your PC will not be damaged.
> If you want to undo everything, see [docs/recovery.md](recovery.md).

> **About this guide**
> There are many steps and you may get stuck along the way.
> For your first time, **we strongly recommend having someone experienced nearby, or screen-sharing with them**.
> If you're going it alone, take your time and verify each step before moving on.

---

## What you'll learn along the way

You're not just installing software — you'll naturally pick up **command patterns that professional developers use every day**.

| Step | Command pattern you'll learn | What it means |
|---|---|---|
| Step 1 | `toolname --version` | "Is this tool installed?" — works for any tool |
| Step 2 | `git clone URL` / `cd folder` | Download a project and navigate into it |
| Step 3 | `./install.sh` / `uv --version` | Run a script and confirm it worked |
| Step 4 | `uv run python script.py` | Run a program in the managed environment |
| Step 5+ | VS Code / AI CLI startup | Daily development tool usage |

> **Commands have patterns.**
> `toolname verb target` is the most common structure. Once you learn a pattern, it applies to other tools too.

### Today's goal (learning path)

| Level | Goal | Tools |
|---|---|---|
| **Beginner (today)** | **Get comfortable with the terminal and complete setup** | **Git, uv, this guide** |
| Elementary | Initialize and run a project | uv, AGENTS.md |
| Intermediate | Write tests and follow code conventions | pytest, Ruff, mypy |
| Advanced | Collaborate with AI CLIs in a development cycle | Claude Code |

**Today's goal is completing "Beginner."** Take it one step at a time.

---

## Run the environment diagnostic first

After installing Git, run this command to check what's installed and what's missing:

```bash
python  scripts/check-setup.py --lang en   # Windows
python3 scripts/check-setup.py --lang en   # macOS / Linux
```

It automatically shows what's missing and how to install it.
**If you get an error, copy the output and search for it, or show it to someone experienced.**

---

## What is a terminal?

A terminal is a screen where you type commands to control your computer.
Instead of clicking icons with a mouse, you type commands to get things done.

**How to open a terminal**

| OS | How to open |
|---|---|
| Windows 11 | Right-click the Start button → "Windows PowerShell" or "Terminal" |
| macOS | `Command + Space` → type "Terminal" → press Enter |
| Linux | `Ctrl + Alt + T` |

> ⚠️ On Windows, you do NOT need "Run as administrator." Open it as a normal user.

---

## Step 1: Install Git

> **What you're learning in this step:**
> The `toolname --version` pattern. This is the universal way to check if any tool is installed.
> It works for `git`, `uv`, `python`, `node`, and almost everything else.

Git is a tool for tracking the history of file changes. It's also used to download projects.

First, check if it's already installed:

```bash
git --version
```

**Expected output:**
```
git version 2.xx.x
```

If you see this → **proceed to Step 2**.

If not, install it using the instructions below.

**Windows 11**

Option A: Install via command
```powershell
winget install --id Git.Git -e --source winget
```
> ⚠️ If `winget` is not found, use Option B.

Option B: Official installer
1. Open https://git-scm.com/download/win
2. Download and run the installer
3. Keep clicking "Next" to install with default settings

After installation, **close and reopen PowerShell**, then run `git --version` to confirm.

**macOS**
```bash
xcode-select --install
```
Click "Install" in the dialog that appears (takes a few minutes).

**Linux (Ubuntu / Debian)**
```bash
sudo apt update && sudo apt install git
```
When prompted for a password, enter your login password (it won't appear on screen — that's normal).

> 💡 **Reading the command: `sudo apt update && sudo apt install git`**
> `sudo` = run as administrator / `apt` = package manager / `&&` = run next command if first succeeds
> Translation: "Update the package list as admin, then install git."

---

## Step 2: Get the repository from GitHub

> **What you're learning in this step:**
> `git clone` (download) and `cd` (navigate into a folder).
> These two always go together as a pair.

**What is GitHub?** A service for managing and sharing code files on the internet.

**① Create a GitHub account (if you don't have one)**
1. Open https://github.com
2. Click "Sign up" to create an account

**② Copy this template**
1. On this repository's page, click the "**Use this template**" button
2. Select "Create a new repository"
3. Enter a repository name and click "Create repository"

**③ Download to your computer**

On the page for your new repository, click "**Code**" → "**HTTPS**" and copy the URL, then run:

```bash
git clone https://github.com/<your-account>/<repository-name>.git
```

**Expected output:**
```
Cloning into '<repository-name>'...
remote: Enumerating objects: ...
Receiving objects: 100% ...
```

Once the download completes, navigate into the folder:

```bash
cd <repository-name>
```

> 💡 **Reading the command: `cd <folder-name>`**
> `cd` stands for "Change Directory" — it moves you into a folder.
> **To check where you are right now:**
> ```bash
> pwd          # macOS / Linux: shows the current folder path
> cd           # Windows: shows the current folder path
> ```
> If you ever get lost in the terminal, use this command to check your location.

---

## Step 3: Install uv

> **What you're learning in this step:**
> How to run a script to install a tool, and the habit of confirming with `--version`.

uv is a tool that automatically manages Python and its packages.
The `uv_setup/` folder contains verified installers for each OS.

**Windows 11**

Open the `uv_setup` folder in File Explorer and **double-click `install.bat`**.

> ⚠️ If "Windows protected your PC" appears: click "More info" → "Run anyway"

Or run from PowerShell:
```powershell
.\uv_setup\install.bat
```

**macOS / Linux**
```bash
chmod +x uv_setup/install.sh
./uv_setup/install.sh
```

> 💡 **Reading the commands: `chmod +x` and `./`**
> `chmod +x filename` = "Give this file permission to be executed."
> `./filename` = "Run the file in the current folder."

After installation, **close and reopen your terminal**, then confirm:
```bash
uv --version
```

**Expected output:**
```
uv 0.x.x (...)
```

See [uv_setup/README.md](../uv_setup/README.md) for more details.

---

## Step 4: Initialize the project

> **What you're learning in this step:**
> The `uv run python scriptname` pattern.
> Prepending `uv run` means "run this Python script inside the environment uv manages."
> This is the standard way to run programs in this template.

Run this command from inside the cloned folder:

```bash
uv run python scripts/init-project.py
```

Answer the questions that appear — type a number or text and press Enter:

```
Select language / 言語を選択 [en/ja] [en]: en   ← type and press Enter

Select project type:
  1. Python ML / AI Research
  2. Data Analysis
  ...
Enter number [1]: 1            ← type and press Enter

Project name (English recommended) [my-project]: my-analysis   ← type and press Enter
```

When you see "Done!" the process is complete.

> 💡 **What just happened?**
> Files like `AGENTS.md`, `CLAUDE.md`, and `README.md` were automatically generated.
> Open the project in VS Code and look at `AGENTS.md` — it's the instruction file for AI CLIs,
> and you can customize it to match your project.

---

## Step 5: Install VS Code (recommended)

> This step is optional. You can use any editor you prefer.

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

### Recommended extensions

| Category | Extension | ID |
|---|---|---|
| AI | Claude Code | `anthropic.claude-code` |
| AI | Continue | `continue.continue` |
| Python | Python | `ms-python.python` |
| Python | Pylance | `ms-python.vscode-pylance` |
| Python | Ruff | `charliermarsh.ruff` |
| Python | Mypy Type Checker | `ms-python.mypy-type-checker` |
| Notebook | Jupyter | `ms-toolsai.jupyter` |
| Git | GitLens | `eamodio.gitlens` |
| Git | Git Graph | `mhutchie.git-graph` |
| Editing | Markdown All in One | `yzhang.markdown-all-in-one` |
| Editing | indent-rainbow | `oderwat.indent-rainbow` |
| LaTeX | LaTeX Workshop | `James-Yu.latex-workshop` |
| Remote | Remote - SSH | `ms-vscode-remote.remote-ssh` |

Install key extensions for Python development all at once:
```bash
code --install-extension anthropic.claude-code \
     ms-python.python ms-python.vscode-pylance \
     charliermarsh.ruff ms-toolsai.jupyter \
     eamodio.gitlens yzhang.markdown-all-in-one
```

---

## Step 6: Install AI CLIs (optional)

> This step is optional. You can develop manually without any AI CLIs.
> `AGENTS.md` also works as a specification document for human readers.

All AI CLIs require **Node.js**.

### Install Node.js

Check first:
```bash
node --version   # v18 or higher is OK
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
claude   # Opens browser to log in with your Anthropic account
```

### Gemini CLI

```bash
npm install -g @google/gemini-cli
gemini   # Opens browser to log in with your Google account
```

### Codex CLI

```bash
npm install -g @openai/codex
```

Set your OpenAI API key:

**Windows 11** (PowerShell)
```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
```

**macOS / Linux** (add to `~/.bashrc` or `~/.zshrc`)
```bash
export OPENAI_API_KEY="sk-..."
```

---

## Setup complete! What's next

By completing this guide, you've naturally learned to use these commands:

| Command | What you can now do |
|---|---|
| `toolname --version` | Check if any tool is installed |
| `git clone URL` | Download a repository |
| `cd folder` | Navigate folders in the terminal |
| `pwd` | Check your current location |
| `uv run python file.py` | Run programs in the uv environment |

**Next steps:**

1. Open `AGENTS.md` and rewrite it to describe your project
2. Open the project in VS Code with `code .`
3. Confirm tests pass with `uv run pytest`

> 💡 **What is `code .`?**
> This command opens the current folder in VS Code.
> `.` means "the current folder" — a pattern that works in many commands.

---

## Using Claude Code for development

### Launch

```bash
cd your-project
claude
```

`AGENTS.md` is auto-loaded so Claude Code understands your project's conventions from the start.

### Basic usage

```
# Request an implementation
Implement a DataLoader class in src/data/loader.py with type hints and docstrings.

# Fix a bug
uv run pytest returns this error: [paste error here]. Find and fix the cause.

# Explain code
Explain the train() method in src/models/trainer.py.
```

### Custom commands

```
/project:test-run          # Run tests → show summary
/project:check-conventions # Check conventions (type hints, docstrings, etc.)
```

---

## Common errors and solutions

### "winget is not recognized" (Windows)

winget may not be installed on Windows 10 or older Windows 11 systems.

**Solution:** Use the official installer (see "Option B" in each Step)

---

### "Windows protected your PC" (Windows)

This appears when you double-click `install.bat` or an `.exe` file.

**Solution:**
1. Click "More info"
2. Click "Run anyway"

This is Windows warning you about files downloaded from the internet.
The files in this repository are safe, but if you're unsure, check with someone experienced.

---

### "Command not found" after installation

The most common cause is not **reopening the terminal** after installation.

**Solution:** Close the terminal, open it again, then run the same command.

---

### Error when running `uv run python scripts/check-setup.py`

**Solution:**
1. Run `uv --version` to check if uv is installed
2. If not shown, redo Step 3 (install uv)
3. If shown, check that your terminal is inside the repository folder:
   ```bash
   pwd          # macOS / Linux
   cd           # Windows (shows the current path)
   ```

---

### Password doesn't appear when typing (macOS / Linux)

When running `sudo`, your password won't show on screen as you type.
**This is normal behavior.** It's being entered — you just can't see it.
Type your password and press Enter.

---

### If nothing else works

**Ask an AI first (recommended)**

Claude, Gemini, and ChatGPT are excellent at diagnosing setup errors.
Copy the prompt template below, fill in your error details, and paste it into any of these:

| AI | Free service |
|---|---|
| Claude | https://claude.ai |
| Gemini | https://gemini.google.com |
| ChatGPT | https://chatgpt.com |

**Copy-paste prompt template:**

```
I'm getting an error while setting up a development environment. Please help me fix it.

[OS]
(e.g., Windows 11 / macOS Sequoia / Ubuntu 22.04)

[Command I ran]
(e.g., uv run python scripts/init-project.py)

[Error message]
(paste the exact error here)

[Environment diagnostic output]
(run the command below and paste the full output here)
python  scripts/check-setup.py --lang en   # Windows
python3 scripts/check-setup.py --lang en   # macOS / Linux
```

> **Tip:** Including both the error message and the `check-setup.py` output helps the AI identify the root cause quickly. The more you paste, the better the answer.

---

If that still doesn't resolve it:

- Show your screen to someone experienced (in person or via screen share)
- Post in [GitHub Discussions](https://github.com/nobufumi-tego/ai-cli-project-template/discussions) (always include the `check-setup.py` output)
