"""Setup check script / セットアップ確認スクリプト。

Diagnoses whether required development tools are installed.
Runs with Python standard library only — no uv or external packages needed.

Usage:
    python  scripts/check-setup.py            # Windows
    python3 scripts/check-setup.py            # macOS / Linux
    python3 scripts/check-setup.py --lang en  # Force English
    python3 scripts/check-setup.py --lang ja  # Force Japanese
"""

from __future__ import annotations

import locale
import platform
import shutil
import subprocess
import sys

OS = platform.system()  # "Windows" | "Darwin" | "Linux"

# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------


def _detect_lang() -> str:
    """Detect display language from --lang argument or system locale.

    Returns:
        "en" or "ja"
    """
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--lang" and i + 2 < len(sys.argv):
            val = sys.argv[i + 2]
            if val in ("en", "ja"):
                return val
        if arg.startswith("--lang="):
            val = arg.split("=", 1)[1]
            if val in ("en", "ja"):
                return val
    loc = locale.getdefaultlocale()[0] or ""
    return "ja" if loc.startswith("ja") else "en"


LANG = _detect_lang()

# ---------------------------------------------------------------------------
# Messages (EN / JA)
# ---------------------------------------------------------------------------

MSG: dict[str, dict[str, str]] = {
    "en": {
        "title": "Setup Check Script",
        "required": "[Required]",
        "recommended": "[Recommended]",
        "ai_cli": "[AI CLI (optional)]",
        "all_ok": "✓ All required tools are installed.",
        "next_step_label": "Next step:",
        "next_step_cmd": "    uv run python scripts/init-project.py",
        "missing_label": "✗ Missing required tools: {missing}",
        "fix_msg": "Install the tools shown above, restart your terminal, then run this script again:",
        "fix_win": "    python  scripts/check-setup.py",
        "fix_unix": "    python3 scripts/check-setup.py",
        # git
        "git_ok": "Git: {v}",
        "git_ng": "Git not found",
        "git_hint_win": (
            "Install:\n"
            "  Option A: winget install --id Git.Git -e --source winget\n"
            "  Option B: Download installer from https://git-scm.com/download/win"
        ),
        "git_hint_mac": "Install: xcode-select --install",
        "git_hint_linux": "Install: sudo apt install git  (Ubuntu/Debian)",
        # uv
        "uv_ok": "uv: {v}",
        "uv_ng": "uv not found",
        "uv_hint_win": (
            'Install:\n'
            '  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"\n'
            '  or double-click uv_setup\\install.bat'
        ),
        "uv_hint_unix": (
            "Install:\n"
            "  ./uv_setup/install.sh\n"
            "  or: curl -LsSf https://astral.sh/uv/install.sh | sh"
        ),
        # python
        "python_ok": "{v}  (recommended version)",
        "python_warn": "{v}  (works, but 3.10+ is recommended)",
        "python_upgrade": "Install latest Python via uv: uv python install 3.12",
        "python_ng": "{v}  (Python 3.8+ required)",
        # node
        "node_ok": "Node.js: {v}  (required for AI CLIs)",
        "node_warn_ver": "Node.js: {v}  (v18+ recommended)",
        "node_ng": "Node.js not found  (required for AI CLIs, optional)",
        "node_update_win": "Update: winget install OpenJS.NodeJS.LTS",
        "node_update_mac": "Update: brew install node",
        "node_update_linux": (
            "Update:\n"
            "  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -\n"
            "  sudo apt install -y nodejs"
        ),
        "node_hint_win": "Install: winget install OpenJS.NodeJS.LTS",
        "node_hint_mac": "Install: brew install node",
        "node_hint_linux": (
            "Install:\n"
            "  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -\n"
            "  sudo apt install -y nodejs"
        ),
        # vscode
        "vscode_ok": "VS Code: {v}  (recommended editor)",
        "vscode_ng": "VS Code not found  (recommended, optional)",
        "vscode_hint_win": "Install: winget install Microsoft.VisualStudioCode",
        "vscode_hint_mac": "Install: brew install --cask visual-studio-code",
        "vscode_hint_linux": "Install: sudo snap install code --classic",
        # ai cli
        "ai_cli_ok": "{name}: {v}  (AI CLI)",
        "ai_cli_ng": "{name} not found  (optional)",
        "ai_cli_hint": "Install: npm install -g {pkg}",
    },
    "ja": {
        "title": "セットアップ確認スクリプト",
        "required": "【必須】",
        "recommended": "【推奨】",
        "ai_cli": "【AI CLI（任意）】",
        "all_ok": "✓ 必須ツールはすべて揃っています。",
        "next_step_label": "次のステップ:",
        "next_step_cmd": "    uv run python scripts/init-project.py",
        "missing_label": "✗ 必須ツールが不足しています: {missing}",
        "fix_msg": (
            "上の「インストール方法」を実行してから、"
            "ターミナルを開き直してもう一度このスクリプトを実行してください:"
        ),
        "fix_win": "    python  scripts/check-setup.py   （Windows）",
        "fix_unix": "    python3 scripts/check-setup.py   （macOS / Linux）",
        # git
        "git_ok": "Git: {v}",
        "git_ng": "Git が見つかりません",
        "git_hint_win": (
            "インストール方法:\n"
            "  方法 A: winget install --id Git.Git -e --source winget\n"
            "  方法 B: https://git-scm.com/download/win からインストーラーをダウンロード"
        ),
        "git_hint_mac": "インストール方法: xcode-select --install",
        "git_hint_linux": "インストール方法: sudo apt install git  （Ubuntu/Debian）",
        # uv
        "uv_ok": "uv: {v}",
        "uv_ng": "uv が見つかりません",
        "uv_hint_win": (
            "インストール方法:\n"
            '  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"\n'
            "  または uv_setup\\install.bat をダブルクリック"
        ),
        "uv_hint_unix": (
            "インストール方法:\n"
            "  ./uv_setup/install.sh\n"
            "  または: curl -LsSf https://astral.sh/uv/install.sh | sh"
        ),
        # python
        "python_ok": "{v}  （推奨バージョン）",
        "python_warn": "{v}  （動作しますが 3.10+ を推奨します）",
        "python_upgrade": "uv で最新 Python を使う: uv python install 3.12",
        "python_ng": "{v}  （3.8 以上が必要です）",
        # node
        "node_ok": "Node.js: {v}  （AI CLI に必要）",
        "node_warn_ver": "Node.js: {v}  （v18 以上を推奨）",
        "node_ng": "Node.js が見つかりません  （AI CLI を使う場合に必要・任意）",
        "node_update_win": "更新方法: winget install OpenJS.NodeJS.LTS",
        "node_update_mac": "更新方法: brew install node",
        "node_update_linux": (
            "更新方法:\n"
            "  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -\n"
            "  sudo apt install -y nodejs"
        ),
        "node_hint_win": "インストール方法: winget install OpenJS.NodeJS.LTS",
        "node_hint_mac": "インストール方法: brew install node",
        "node_hint_linux": (
            "インストール方法:\n"
            "  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -\n"
            "  sudo apt install -y nodejs"
        ),
        # vscode
        "vscode_ok": "VS Code: {v}  （推奨エディタ）",
        "vscode_ng": "VS Code が見つかりません  （推奨・任意）",
        "vscode_hint_win": "インストール方法: winget install Microsoft.VisualStudioCode",
        "vscode_hint_mac": "インストール方法: brew install --cask visual-studio-code",
        "vscode_hint_linux": "インストール方法: sudo snap install code --classic",
        # ai cli
        "ai_cli_ok": "{name}: {v}  （AI CLI）",
        "ai_cli_ng": "{name} が見つかりません  （任意）",
        "ai_cli_hint": "インストール方法: npm install -g {pkg}",
    },
}

m = MSG[LANG]

# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

# Disable colors on Windows Command Prompt (may not support ANSI codes)
if OS == "Windows":
    GREEN = YELLOW = RED = RESET = ""


def ok(msg: str) -> None:
    """Print a success message."""
    print(f"  {GREEN}✓{RESET}  {msg}")


def warn(msg: str) -> None:
    """Print a warning message."""
    print(f"  {YELLOW}!{RESET}  {msg}")


def ng(msg: str) -> None:
    """Print an error message."""
    print(f"  {RED}✗{RESET}  {msg}")


def hint(msg: str) -> None:
    """Print install instructions."""
    for line in msg.strip().splitlines():
        print(f"       {line}")
    print()


# ---------------------------------------------------------------------------
# Tool checks
# ---------------------------------------------------------------------------


def get_version(cmd: list[str]) -> str | None:
    """Run a command and return the first line of output.

    Args:
        cmd: Command list to execute.

    Returns:
        First line of stdout+stderr, or None on failure.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        output = (result.stdout + result.stderr).strip()
        return output.splitlines()[0] if output else None
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None


def check_git() -> bool:
    """Check whether Git is installed.

    Returns:
        True if installed.
    """
    version = get_version(["git", "--version"])
    if version:
        ok(m["git_ok"].format(v=version))
        return True
    ng(m["git_ng"])
    if OS == "Windows":
        hint(m["git_hint_win"])
    elif OS == "Darwin":
        hint(m["git_hint_mac"])
    else:
        hint(m["git_hint_linux"])
    return False


def check_uv() -> bool:
    """Check whether uv is installed.

    Returns:
        True if installed.
    """
    version = get_version(["uv", "--version"])
    if version:
        ok(m["uv_ok"].format(v=version))
        return True
    ng(m["uv_ng"])
    if OS == "Windows":
        hint(m["uv_hint_win"])
    else:
        hint(m["uv_hint_unix"])
    return False


def check_python() -> bool:
    """Check whether Python version meets the minimum requirement.

    Returns:
        True if Python 3.8+.
    """
    major, minor = sys.version_info[:2]
    v = f"Python {major}.{minor}.{sys.version_info[2]}"
    if (major, minor) >= (3, 10):
        ok(m["python_ok"].format(v=v))
        return True
    elif (major, minor) >= (3, 8):
        warn(m["python_warn"].format(v=v))
        hint(m["python_upgrade"])
        return True
    else:
        ng(m["python_ng"].format(v=v))
        hint(m["python_upgrade"])
        return False


def check_node() -> bool:
    """Check whether Node.js is installed (optional, for AI CLIs).

    Returns:
        True if installed.
    """
    version = get_version(["node", "--version"])
    if version:
        num = version.lstrip("v").split(".")[0]
        if num.isdigit() and int(num) >= 18:
            ok(m["node_ok"].format(v=version))
        else:
            warn(m["node_warn_ver"].format(v=version))
            if OS == "Windows":
                hint(m["node_update_win"])
            elif OS == "Darwin":
                hint(m["node_update_mac"])
            else:
                hint(m["node_update_linux"])
        return True
    warn(m["node_ng"])
    if OS == "Windows":
        hint(m["node_hint_win"])
    elif OS == "Darwin":
        hint(m["node_hint_mac"])
    else:
        hint(m["node_hint_linux"])
    return False


def check_vscode() -> bool:
    """Check whether VS Code is installed (optional).

    Returns:
        True if installed.
    """
    version = get_version(["code", "--version"])
    if version:
        ok(m["vscode_ok"].format(v=version.splitlines()[0]))
        return True
    warn(m["vscode_ng"])
    if OS == "Windows":
        hint(m["vscode_hint_win"])
    elif OS == "Darwin":
        hint(m["vscode_hint_mac"])
    else:
        hint(m["vscode_hint_linux"])
    return False


def check_ai_cli(name: str, cmd: str, pkg: str) -> bool:
    """Check whether an AI CLI tool is installed (optional).

    Args:
        name: Tool display name.
        cmd: Executable name to check.
        pkg: npm package name for install hint.

    Returns:
        True if installed.
    """
    if shutil.which(cmd):
        version = get_version([cmd, "--version"])
        ok(m["ai_cli_ok"].format(name=name, v=version or "?"))
        return True
    warn(m["ai_cli_ng"].format(name=name))
    hint(m["ai_cli_hint"].format(pkg=pkg))
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the environment diagnostic and print results."""
    print()
    print("=" * 54)
    print(f"  {m['title']}")
    print(f"  OS: {OS} / Python {sys.version.split()[0]}")
    print("=" * 54)

    results: dict[str, bool] = {}

    print(f"\n{m['required']}")
    results["git"] = check_git()
    results["uv"] = check_uv()
    results["python"] = check_python()

    print(f"\n{m['recommended']}")
    results["vscode"] = check_vscode()

    print(f"\n{m['ai_cli']}")
    results["node"] = check_node()
    if results["node"]:
        results["claude"] = check_ai_cli(
            "Claude Code", "claude", "@anthropic-ai/claude-code"
        )
        results["gemini"] = check_ai_cli(
            "Gemini CLI", "gemini", "@google/gemini-cli"
        )
        results["codex"] = check_ai_cli(
            "Codex CLI", "codex", "@openai/codex"
        )

    print()
    print("=" * 54)
    required_ok = results["git"] and results["uv"] and results["python"]

    if required_ok:
        print(f"  {GREEN}{m['all_ok']}{RESET}")
        print()
        print(f"  {m['next_step_label']}")
        print(m["next_step_cmd"])
    else:
        missing = [k for k in ("git", "uv", "python") if not results.get(k)]
        print(f"  {RED}{m['missing_label'].format(missing=', '.join(missing))}{RESET}")
        print()
        print(f"  {m['fix_msg']}")
        print(m["fix_win"] if OS == "Windows" else m["fix_unix"])

    print("=" * 54)
    print()

    sys.exit(0 if required_ok else 1)


if __name__ == "__main__":
    main()
