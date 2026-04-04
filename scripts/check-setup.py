"""セットアップ確認スクリプト。

開発環境に必要なツールが揃っているか自動診断します。
Python のみで動作します（uv・外部パッケージ不要）。

Usage:
    python  scripts/check-setup.py   # Windows
    python3 scripts/check-setup.py   # macOS / Linux
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys

OS = platform.system()  # "Windows" | "Darwin" | "Linux"

# ---------------------------------------------------------------------------
# 表示ヘルパー
# ---------------------------------------------------------------------------

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

# Windows のコマンドプロンプトはカラーコード非対応の場合があるため無効化
if OS == "Windows":
    GREEN = YELLOW = RED = RESET = ""


def ok(msg: str) -> None:
    """成功メッセージを表示する。"""
    print(f"  {GREEN}✓{RESET}  {msg}")


def warn(msg: str) -> None:
    """警告メッセージを表示する。"""
    print(f"  {YELLOW}!{RESET}  {msg}")


def ng(msg: str) -> None:
    """エラーメッセージを表示する。"""
    print(f"  {RED}✗{RESET}  {msg}")


def hint(msg: str) -> None:
    """インストール方法のヒントを表示する。"""
    for line in msg.strip().splitlines():
        print(f"       {line}")
    print()


# ---------------------------------------------------------------------------
# ツールチェック
# ---------------------------------------------------------------------------


def get_version(cmd: list[str]) -> str | None:
    """コマンドを実行してバージョン文字列を返す。失敗時は None。

    Args:
        cmd: 実行するコマンドリスト

    Returns:
        バージョン文字列、または None
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
    """Git のインストールを確認する。

    Returns:
        インストール済みの場合 True
    """
    version = get_version(["git", "--version"])
    if version:
        ok(f"Git: {version}")
        return True

    ng("Git が見つかりません")
    if OS == "Windows":
        hint("""\
インストール方法:
  方法 A: winget install --id Git.Git -e --source winget
  方法 B: https://git-scm.com/download/win からインストーラーをダウンロード""")
    elif OS == "Darwin":
        hint("インストール方法: xcode-select --install")
    else:
        hint("インストール方法: sudo apt install git  （Ubuntu/Debian）")
    return False


def check_uv() -> bool:
    """uv のインストールを確認する。

    Returns:
        インストール済みの場合 True
    """
    version = get_version(["uv", "--version"])
    if version:
        ok(f"uv: {version}")
        return True

    ng("uv が見つかりません")
    if OS == "Windows":
        hint(
            'インストール方法:\n'
            '  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"\n'
            '  または uv_setup\\install.bat をダブルクリック'
        )
    else:
        hint(
            "インストール方法:\n"
            "  ./uv_setup/install.sh\n"
            "  または: curl -LsSf https://astral.sh/uv/install.sh | sh"
        )
    return False


def check_python() -> bool:
    """Python のバージョンを確認する。

    Returns:
        3.8 以上であれば True
    """
    major, minor = sys.version_info[:2]
    version_str = f"Python {major}.{minor}.{sys.version_info[2]}"

    if (major, minor) >= (3, 10):
        ok(f"{version_str}  （推奨バージョン）")
        return True
    elif (major, minor) >= (3, 8):
        warn(f"{version_str}  （動作しますが 3.10+ を推奨します）")
        hint("uv で最新 Python を使う: uv python install 3.12")
        return True
    else:
        ng(f"{version_str}  （3.8 以上が必要です）")
        hint("uv で最新 Python を使う: uv python install 3.12")
        return False


def check_node() -> bool:
    """Node.js のインストールを確認する（任意）。

    Returns:
        インストール済みの場合 True
    """
    version = get_version(["node", "--version"])
    if version:
        # v18 以上かチェック
        num = version.lstrip("v").split(".")[0]
        if num.isdigit() and int(num) >= 18:
            ok(f"Node.js: {version}  （AI CLI に必要）")
        else:
            warn(f"Node.js: {version}  （v18 以上を推奨）")
            if OS == "Windows":
                hint("更新方法: winget install OpenJS.NodeJS.LTS")
            elif OS == "Darwin":
                hint("更新方法: brew install node")
            else:
                hint(
                    "更新方法:\n"
                    "  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -\n"
                    "  sudo apt install -y nodejs"
                )
        return True

    warn("Node.js が見つかりません  （AI CLI を使う場合に必要・任意）")
    if OS == "Windows":
        hint("インストール方法: winget install OpenJS.NodeJS.LTS")
    elif OS == "Darwin":
        hint("インストール方法: brew install node")
    else:
        hint(
            "インストール方法:\n"
            "  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -\n"
            "  sudo apt install -y nodejs"
        )
    return False


def check_vscode() -> bool:
    """VS Code のインストールを確認する（任意）。

    Returns:
        インストール済みの場合 True
    """
    version = get_version(["code", "--version"])
    if version:
        ok(f"VS Code: {version.splitlines()[0]}  （推奨エディタ）")
        return True

    warn("VS Code が見つかりません  （推奨・任意）")
    if OS == "Windows":
        hint("インストール方法: winget install Microsoft.VisualStudioCode")
    elif OS == "Darwin":
        hint("インストール方法: brew install --cask visual-studio-code")
    else:
        hint("インストール方法: sudo snap install code --classic")
    return False


def check_ai_cli(name: str, cmd: str, pkg: str) -> bool:
    """AI CLI のインストールを確認する（任意）。

    Args:
        name: ツール名
        cmd: 確認コマンド
        pkg: npm パッケージ名

    Returns:
        インストール済みの場合 True
    """
    if shutil.which(cmd):
        version = get_version([cmd, "--version"])
        ok(f"{name}: {version or '（バージョン取得失敗）'}  （AI CLI）")
        return True

    warn(f"{name} が見つかりません  （任意）")
    hint(f"インストール方法: npm install -g {pkg}")
    return False


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------


def main() -> None:
    """環境診断を実行して結果を表示する。"""
    print()
    print("=" * 54)
    print("  セットアップ確認スクリプト")
    print(f"  OS: {OS} / Python {sys.version.split()[0]}")
    print("=" * 54)

    results: dict[str, bool] = {}

    # ── 必須ツール ──────────────────────────────────────
    print("\n【必須】")
    results["git"] = check_git()
    results["uv"] = check_uv()
    results["python"] = check_python()

    # ── 推奨ツール ──────────────────────────────────────
    print("\n【推奨】")
    results["vscode"] = check_vscode()

    # ── AI CLI（任意） ───────────────────────────────────
    print("\n【AI CLI（任意）】")
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

    # ── サマリー ────────────────────────────────────────
    print()
    print("=" * 54)
    required_ok = results["git"] and results["uv"] and results["python"]

    if required_ok:
        print(f"  {GREEN}✓ 必須ツールはすべて揃っています。{RESET}")
        print()
        print("  次のステップ:")
        print("    uv run python scripts/init-project.py")
    else:
        missing = [k for k in ("git", "uv", "python") if not results.get(k)]
        print(f"  {RED}✗ 必須ツールが不足しています: {', '.join(missing)}{RESET}")
        print()
        print("  上の「インストール方法」を実行してから、")
        print("  ターミナルを開き直してもう一度このスクリプトを実行してください:")
        print("    python  scripts/check-setup.py   （Windows）")
        print("    python3 scripts/check-setup.py   （macOS / Linux）")

    print("=" * 54)
    print()

    sys.exit(0 if required_ok else 1)


if __name__ == "__main__":
    main()
