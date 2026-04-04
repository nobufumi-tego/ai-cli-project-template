"""Project initialization script / プロジェクト初期化スクリプト。

Interactively collects project information and generates AGENTS.md, CLAUDE.md,
GEMINI.md, README.md, and pyproject.toml.
Supports English and Japanese. Helps install uv if not found.

対話形式でプロジェクト情報を収集し、AGENTS.md・CLAUDE.md・GEMINI.md・
README.md・pyproject.toml を自動生成する。
英語・日本語に対応。uv が未インストールの場合はインストールを支援する。

Supported OS / 対応 OS: Windows 11 / macOS / Linux
Project types / 対応種別: Python (ML, Analysis, API, CLI, Library) / LaTeX / Word / Custom

Usage:
    python  scripts/init-project.py          # Windows
    python3 scripts/init-project.py          # macOS / Linux
    python3 scripts/init-project.py --lang en  # Force English
    python3 scripts/init-project.py --lang ja  # Force Japanese
"""

from __future__ import annotations

import locale
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
MIN_PYTHON: tuple[int, int] = (3, 10)

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


# ---------------------------------------------------------------------------
# UI Messages (EN / JA)
# ---------------------------------------------------------------------------

MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "lang_prompt": "Select language / 言語を選択",
        "title": "AI CLI Project Initialization",
        "subtitle": "Answer the questions to generate AGENTS.md, README.md, and more.",
        "interrupt_hint": "(Press Ctrl+C to cancel at any time)",
        "python_warn": "  ! Python {ver} detected. Python {min}+ is recommended.",
        "python_ok": "  ✓ Python {ver}",
        "uv_section": "── uv check ──",
        "uv_ok": "  ✓ uv: {ver}",
        "uv_ng": "  uv not found.",
        "uv_desc": "  uv is a fast Python package manager used by this template.",
        "uv_install_header": "  ─── How to install uv ───",
        "uv_install_footer": "  ────────────────────────",
        "uv_win_label": "  Run in PowerShell:",
        "uv_unix_label": "  Run in terminal:",
        "uv_homebrew": "  Or (Homebrew):",
        "no_curl": "  ! curl not found. Please install uv manually.",
        "uv_install_prompt": "  Try auto-install now?",
        "uv_manual": "  Run the command above manually, then re-run this script.",
        "uv_installing": "  Installing...",
        "uv_cmd_not_found": "  ✗ Command not found: {e}",
        "uv_install_failed": "  ✗ Installation failed. Please install manually.",
        "uv_install_ok": "  ✓ Installation complete.",
        "uv_restart": "  ! Please restart your terminal to update PATH.",
        "uv_restart_win": (
            '    Or run in PowerShell: '
            '$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","User")'
        ),
        "uv_restart_unix": (
            "    Or run: source ~/.bashrc"
            "  (or ~/.zshrc, ~/.config/fish/config.fish, etc.)"
        ),
        "preset_title": "Select project type:",
        "preset_selected": '→ Selected: "{label}"\n',
        "preset_invalid": "  Please enter a number from 1 to {n}.",
        "prompt_number": "Enter number",
        "prompt_name": "Project name (English recommended)",
        "default_name": "my-project",
        "prompt_desc": "Project description (1-2 lines)",
        "default_desc": "Project description.",
        "label_commands": "commands",
        "label_arch": "folder structure",
        "label_conv": "conventions",
        "label_watch": "watch out for",
        "default_check": "Use this default?",
        "multiline_end": "(Press Enter on an empty line to finish)",
        "input_label": "Enter {label}",
        "interrupted": "\n\nCancelled.",
        "conv_select": "Select convention type:",
        "conv_options": [
            "1. Python (type hints, docstrings, etc.)",
            "2. LaTeX (section split, BibTeX, etc.)",
            "3. Word (file naming, style, etc.)",
            "4. Manual input",
        ],
        "dodont_label": "Do / Don't",
        "confirm_header": "The following files will be generated:",
        "confirm_name": "  Project name  : {v}",
        "confirm_type": "  Type          : {v}",
        "confirm_desc": "  Description   : {v}",
        "confirm_files": "  Files         : AGENTS.md / CLAUDE.md / GEMINI.md / README.md",
        "confirm_pyproject": "                  pyproject.toml",
        "proceed": "Proceed?",
        "aborted": "Aborted.",
        "done": "Done!",
        "next_python": (
            "Next steps:\n"
            "  1. uv sync                 # Install dependencies\n"
            "  2. uv run pytest tests/    # Confirm tests pass\n"
            "  3. Develop AGENTS.md       # Add project-specific details"
        ),
        "next_latex": (
            "Next steps:\n"
            "  1. Check your TeX environment   # See README.md setup section\n"
            "  2. Edit sections/*.tex\n"
            "  3. latexmk -pdf main.tex       # Compile to PDF"
        ),
        "next_word": (
            "Next steps:\n"
            "  1. Create .docx files in docs/\n"
            "  2. Set up Zotero or another reference manager\n"
            "  3. Add writing guidelines to README.md"
        ),
        "written": "  ✓ {f}",
        "latex_gitignore": "  ✓ .gitignore (LaTeX patterns added)",
        "latex_skeleton": "  ✓ LaTeX skeleton created (sections/ figures/ refs.bib .latexmkrc)",
        "word_skeleton": "  ✓ Word skeleton created (docs/ figures/ refs/)",
    },
    "ja": {
        "lang_prompt": "Select language / 言語を選択",
        "title": "AI CLI プロジェクト初期化スクリプト",
        "subtitle": "質問に答えると AGENTS.md・README.md 等が自動生成されます。",
        "interrupt_hint": "（Ctrl+C でいつでも中断できます）",
        "python_warn": "  ! Python {ver} を使用中です。Python {min}+ を推奨します。",
        "python_ok": "  ✓ Python {ver}",
        "uv_section": "─── uv チェック ───",
        "uv_ok": "  ✓ uv: {ver}",
        "uv_ng": "  ! uv が見つかりません。",
        "uv_desc": "  uv は高速な Python パッケージマネージャーです（このテンプレートで使用）。",
        "uv_install_header": "  ─── uv インストール方法 ───",
        "uv_install_footer": "  ─────────────────────────",
        "uv_win_label": "  PowerShell（管理者）で実行：",
        "uv_unix_label": "  ターミナルで実行：",
        "uv_homebrew": "  または（Homebrew）：",
        "no_curl": "  ! curl が見つかりません。手動でインストールしてください。",
        "uv_install_prompt": "  今すぐ自動インストールを試みますか？",
        "uv_manual": "  上記コマンドを手動で実行してから、スクリプトを再度実行してください。",
        "uv_installing": "  インストール中...",
        "uv_cmd_not_found": "  ✗ コマンドが見つかりません: {e}",
        "uv_install_failed": "  ✗ インストールに失敗しました。手動でインストールしてください。",
        "uv_install_ok": "  ✓ インストールが完了しました。",
        "uv_restart": "  ! PATH を更新するためターミナルを再起動してください。",
        "uv_restart_win": (
            '    または PowerShell で実行：'
            ' $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","User")'
        ),
        "uv_restart_unix": (
            "    または: source ~/.bashrc"
            "  （~/.zshrc / ~/.config/fish/config.fish 等）"
        ),
        "preset_title": "プロジェクト種別を選択してください：",
        "preset_selected": '→ 「{label}」を選択しました。\n',
        "preset_invalid": "  1〜{n} の番号を入力してください。",
        "prompt_number": "番号を入力",
        "prompt_name": "プロジェクト名（英語推奨）",
        "default_name": "my-project",
        "prompt_desc": "プロジェクトの説明（1〜2行）",
        "default_desc": "プロジェクトの説明。",
        "label_commands": "コマンド",
        "label_arch": "フォルダ構成",
        "label_conv": "規約",
        "label_watch": "注意事項",
        "default_check": "このまま使いますか？",
        "multiline_end": "（空行で入力終了）",
        "input_label": "{label}を入力",
        "interrupted": "\n\n中断しました。",
        "conv_select": "規約の種別を選択してください：",
        "conv_options": [
            "1. Python（型ヒント・docstring 等）",
            "2. LaTeX（セクション分割・BibTeX 等）",
            "3. Word（ファイル命名・スタイル統一 等）",
            "4. 手動入力",
        ],
        "dodont_label": "Do / Don't",
        "confirm_header": "以下の内容でファイルを生成します：",
        "confirm_name": "  プロジェクト名  : {v}",
        "confirm_type": "  種別            : {v}",
        "confirm_desc": "  説明            : {v}",
        "confirm_files": "  生成ファイル    : AGENTS.md / CLAUDE.md / GEMINI.md / README.md",
        "confirm_pyproject": "                    pyproject.toml",
        "proceed": "続けますか？",
        "aborted": "中断しました。",
        "done": "完了しました！",
        "next_python": (
            "次のステップ：\n"
            "  1. uv sync                 # 依存パッケージをインストール\n"
            "  2. uv run pytest tests/    # テスト実行で動作確認\n"
            "  3. AGENTS.md を育てる      # プロジェクト固有の情報を追記していく"
        ),
        "next_latex": (
            "次のステップ：\n"
            "  1. TeX 環境を確認する      # README.md のセットアップ手順を参照\n"
            "  2. sections/*.tex を編集する\n"
            "  3. latexmk -pdf main.tex  # PDF をコンパイル"
        ),
        "next_word": (
            "次のステップ：\n"
            "  1. docs/ フォルダに .docx ファイルを作成する\n"
            "  2. Zotero 等の参考文献管理ツールを設定する\n"
            "  3. README.md に執筆ガイドラインを追記する"
        ),
        "written": "  ✓ {f}",
        "latex_gitignore": "  ✓ .gitignore（LaTeX パターンを追記）",
        "latex_skeleton": "  ✓ LaTeX 骨格ファイルを作成（sections/ figures/ refs.bib .latexmkrc）",
        "word_skeleton": "  ✓ Word 骨格ディレクトリを作成（docs/ figures/ refs/）",
    },
}

# ---------------------------------------------------------------------------
# Preset content — English
# ---------------------------------------------------------------------------

_PY_CONV_EN = """\
- Type hints required (Python 3.10+)
- Write docstrings for all functions and classes (Google style)
- Include units in comments or variable names (e.g., `duration_sec`, `size_mb`)
- Convert all magic numbers to named constants (at module top or in `configs/`)
- Do not omit error handling
- Use `pathlib.Path` instead of `os.path`
- Do not hardcode absolute paths"""

_PY_DODONT_EN = """\
DO:
- Run `uv run pytest` before making changes to confirm existing tests pass
- Add tests whenever you add a new feature
- data/raw/ files are read-only; put processed results in data/processed/

DON'T:
- Do not git-track large files (videos, model checkpoints, etc.) — .gitignore is configured
- Do not hardcode GPU/CPU environment differences
- Do not directly edit files in data/raw/"""

_LATEX_CONV_EN = """\
- Split sections into separate .tex files; load with \\input{sections/...} in main.tex
- Use relative paths for figures (e.g., \\includegraphics{figures/fig1.pdf})
- Collect all references in refs.bib; cite with \\citep / \\citet
- Leave comments explaining changes (e.g., % [2024-01-15] Fixed per reviewer)
- For Japanese papers use uplatex + dvipdfmx or LuaLaTeX
- Standardize English punctuation: period (.) and comma (,)"""

_LATEX_DODONT_EN = """\
DO:
- git commit before making changes to preserve history
- Compile and visually verify after adding figures or tables
- Tidy refs.bib as you add each reference

DON'T:
- Do not git-track compiled files (*.aux, *.log, etc.) — .gitignore is configured
- Do not write the entire paper in main.tex (split into sections/)
- Do not make large rewrites without a backup commit"""

_WORD_CONV_EN = """\
- Include version number or date in filenames (e.g., paper_v2.1_20240115.docx)
- Apply consistent heading, body, and caption styles (avoid direct formatting)
- Insert figures as inline images, not inside text boxes
- Manage references with Zotero or similar tools
- Use Track Changes when a revision trail is required (no manual strikethrough)"""

_WORD_DODONT_EN = """\
DO:
- Use git regularly to record history (binary diff is invisible, but commits are tracked)
- Accept all tracked changes before submission for a clean final document
- Save with embedded fonts for both body and headings

DON'T:
- Do not git-track multiple draft .docx files (binary diffs are not readable)
- Do not position figures with spaces or blank lines (use figure positioning settings)
- Do not submit with comments or tracked changes remaining"""

PRESETS_EN: dict[str, dict[str, str]] = {
    "1": {
        "label": "Python ML / AI Research",
        "type": "python",
        "commands": """\
uv run python src/main.py              # Run main process
uv run pytest tests/ -v                # Run tests
uv run ruff check src/ tests/          # Lint
uv run mypy src/                       # Type check
jupyter lab notebooks/                 # Launch Notebook""",
        "architecture": """\
- src/data/       - Data loading and preprocessing modules
- src/models/     - Model definitions and training logic
- src/evaluation/ - Evaluation and metrics
- src/utils/      - Shared utilities
- data/raw/       - Source data (read-only, not git-tracked)
- data/processed/ - Processed data
- notebooks/      - Jupyter Notebooks for experiments
- tests/          - Test code
- configs/        - Configuration files (YAML)""",
        "conventions": _PY_CONV_EN,
        "do_dont": _PY_DODONT_EN,
        "watch_out_for": """\
- Even with a fixed random seed, numerical results may vary slightly between GPU and CPU
- Use pathlib.Path for dataset paths; avoid absolute paths
- Place model checkpoints (*.pt, *.pkl) under data/""",
    },
    "2": {
        "label": "Data Analysis",
        "type": "python",
        "commands": """\
uv run python src/main.py              # Run main process
uv run pytest tests/ -v                # Run tests
uv run ruff check src/ tests/          # Lint
jupyter lab notebooks/                 # Launch Notebook""",
        "architecture": """\
- src/           - Analysis scripts
- src/utils/     - Shared utilities
- data/raw/      - Source data (read-only, not git-tracked)
- data/processed/- Processed data
- notebooks/     - Jupyter Notebooks for analysis
- tests/         - Test code
- outputs/       - Figures and report outputs""",
        "conventions": _PY_CONV_EN,
        "do_dont": _PY_DODONT_EN,
        "watch_out_for": """\
- Use pathlib.Path for dataset paths; avoid absolute paths
- Do not write notebook code that depends on execution order (refactor into modules)
- Visualization library versions may affect output""",
    },
    "3": {
        "label": "Web API (FastAPI)",
        "type": "python",
        "commands": """\
uv run uvicorn src.main:app --reload   # Start dev server
uv run pytest tests/ -v                # Run tests
uv run ruff check src/ tests/          # Lint
uv run mypy src/                       # Type check""",
        "architecture": """\
- src/            - Application code
- src/routers/    - API routers
- src/models/     - Pydantic models and schemas
- src/services/   - Business logic
- src/utils/      - Shared utilities
- tests/          - Test code""",
        "conventions": _PY_CONV_EN,
        "do_dont": """\
DO:
- Store env vars and secrets in .env (confirm it is .gitignored)
- Use dependency injection (Depends) for testable code
- Run `uv run pytest` before making changes to confirm tests pass

DON'T:
- Never hardcode API keys or passwords in source code
- Do not mix async/await with synchronous code
- Do not run tests connected to a production database""",
        "watch_out_for": """\
- Never commit the .env file to git
- Be careful about mixing async/await and synchronous code
- Watch for circular dependencies in dependency injection""",
    },
    "4": {
        "label": "CLI Tool",
        "type": "python",
        "commands": """\
uv run python src/main.py --help       # Show help
uv run pytest tests/ -v                # Run tests
uv run ruff check src/ tests/          # Lint
uv run mypy src/                       # Type check""",
        "architecture": """\
- src/           - CLI code (click / typer etc.)
- src/commands/  - Subcommand definitions
- src/utils/     - Shared utilities
- tests/         - Test code""",
        "conventions": _PY_CONV_EN,
        "do_dont": _PY_DODONT_EN,
        "watch_out_for": """\
- Set appropriate exit codes (success: 0, error: non-zero)
- Clearly separate stdin / stdout / stderr usage
- Use pathlib.Path to abstract OS path differences""",
    },
    "5": {
        "label": "Python Library",
        "type": "python",
        "commands": """\
uv run pytest tests/ -v                # Run tests
uv run ruff check src/ tests/          # Lint
uv run mypy src/                       # Type check
uv build                               # Build package""",
        "architecture": """\
- src/<package>/ - Library source
- tests/         - Test code
- docs/          - Documentation (Sphinx etc.)""",
        "conventions": _PY_CONV_EN,
        "do_dont": _PY_DODONT_EN,
        "watch_out_for": """\
- Explicitly specify the supported Python version range in pyproject.toml
- Keep external dependencies to a minimum
- Explicitly define the public API (__all__)""",
    },
    "6": {
        "label": "LaTeX Paper",
        "type": "latex",
        "commands": """\
latexmk -pdf main.tex              # Compile to PDF
latexmk -c                         # Clean intermediate files
latexmk -pvc main.tex              # Auto-compile (watch mode)
# For Japanese papers:
latexmk -pdfdvi main.tex           # Compile with uplatex + dvipdfmx""",
        "architecture": """\
- main.tex        - Main paper file (loads sections with \\input)
- sections/       - Per-section .tex files
  - introduction.tex
  - method.tex
  - results.tex
  - discussion.tex
  - conclusion.tex
- figures/        - Figures and graphs (PDF / PNG recommended)
- tables/         - Tables (.tex format)
- refs.bib        - References (BibTeX format)
- styles/         - Style and class files
- .latexmkrc      - latexmk configuration""",
        "conventions": _LATEX_CONV_EN,
        "do_dont": _LATEX_DODONT_EN,
        "watch_out_for": """\
- Japanese fonts are environment-dependent; install required fonts via tlmgr for TeX Live
- Avoid spaces and non-ASCII characters in figure filenames
- Use FirstauthorYYYYkeyword format for BibTeX cite keys for consistency
- Include .latexmkrc in the repository to standardize the build environment""",
    },
    "7": {
        "label": "Word Paper (.docx)",
        "type": "word",
        "commands": """\
# Edit files directly in Word / LibreOffice
# Using pandoc (optional):
pandoc main.docx -o main.pdf       # Convert to PDF
pandoc main.md -o main.docx        # Convert Markdown to Word
# Reference management with Zotero:
# → Use Zotero desktop app + Word plugin""",
        "architecture": """\
- docs/              - Word documents (.docx)
  - paper_v1.0.docx  - Draft versions
  - paper_final.docx - Final version
- figures/           - Figures and graphs (source files)
- tables/            - Tables (Excel / CSV format)
- refs/              - References (.bib or Zotero export)""",
        "conventions": _WORD_CONV_EN,
        "do_dont": _WORD_DODONT_EN,
        "watch_out_for": """\
- Never commit API keys or credentials to git
- Binary .docx files cannot show meaningful diffs in git
- Use consistent filename conventions throughout the project""",
    },
    "8": {
        "label": "Custom",
        "type": "custom",
        "commands": "",
        "architecture": "",
        "conventions": "",
        "do_dont": "",
        "watch_out_for": "",
    },
}

# ---------------------------------------------------------------------------
# Preset content — Japanese
# ---------------------------------------------------------------------------

_PY_CONV_JA = """\
- 型ヒント必須（Python 3.10+）
- すべての関数・クラスにdocstringを書く（Google スタイル）
- 数値の単位はコメントまたは変数名で明記（例: `duration_sec`, `size_mb`）
- マジックナンバーはすべて定数化（各モジュール先頭または `configs/` に定義）
- エラーハンドリングを省略しない
- `os.path` ではなく `pathlib.Path` を使う
- 絶対パスをハードコードしない"""

_PY_DODONT_JA = """\
DO:
- 変更前に `uv run pytest` を実行して既存テストが通ることを確認する
- 新しい機能を追加したらテストも同時に追加する
- data/raw/ のファイルは読み取りのみ。加工結果は data/processed/ へ

DON'T:
- 大容量ファイル（動画・モデルチェックポイント等）をgit管理しない（.gitignore 設定済み）
- GPU/CPU環境依存のハードコードをしない
- data/raw/ のファイルを直接編集しない"""

_LATEX_CONV_JA = """\
- セクション別に .tex ファイルを分割し、main.tex で \\input{sections/...} する
- 図のパスは相対パスで記述する（例: \\includegraphics{figures/fig1.pdf}）
- 参考文献は refs.bib にまとめ、\\citep / \\citet コマンドで引用する
- 変更理由をコメントで残す（例: % [2024-01-15] reviewer の指摘で修正）
- 日本語論文は uplatex + dvipdfmx または LuaLaTeX を使う
- 英語論文の句読点は period（.）と comma（,）で統一する"""

_LATEX_DODONT_JA = """\
DO:
- 変更前に git commit して履歴を残す
- 図・表を追加したら必ずコンパイルして見た目を確認する
- 参考文献は追加の都度 refs.bib を整理する

DON'T:
- コンパイル生成ファイル（*.aux, *.log 等）をgit管理しない（.gitignore 設定済み）
- main.tex に全文を書かない（sections/ に分割する）
- バックアップなしに大幅な書き換えをしない"""

_WORD_CONV_JA = """\
- ファイル名にバージョン番号または日付を含める（例: paper_v2.1_20240115.docx）
- 見出し・本文・図タイトル等はスタイルを統一して使う（直接書式を多用しない）
- 図はインライン図として挿入し、テキストボックスに入れない
- 参考文献は Zotero 等の文献管理ツールで管理する
- 変更履歴が必要な場合は「変更履歴の記録」機能を使う（手動の取り消し線は禁止）"""

_WORD_DODONT_JA = """\
DO:
- 定期的に git で管理して変更履歴を残す（バイナリ差分は見えないが存在を記録できる）
- 提出前にトラックチェンジをすべて承認してクリーンな状態にする
- フォントは本文・見出しとも埋め込み設定で保存する

DON'T:
- 最終稿以外の多数の .docx を git 管理しない（バイナリ差分が見えない）
- 図の位置をスペースや改行で調整しない（図の配置設定を使う）
- コメント・変更履歴を残したまま提出しない"""

PRESETS_JA: dict[str, dict[str, str]] = {
    "1": {
        "label": "Python ML / AI 研究",
        "type": "python",
        "commands": """\
uv run python src/main.py              # メイン処理実行
uv run pytest tests/ -v                # テスト実行
uv run ruff check src/ tests/          # リント
uv run mypy src/                       # 型チェック
jupyter lab notebooks/                 # Notebook起動""",
        "architecture": """\
- src/data/       - データ読み込み・前処理モジュール
- src/models/     - モデル定義・学習ロジック
- src/evaluation/ - 評価・メトリクス算出
- src/utils/      - 共通ユーティリティ
- data/raw/       - 元データ（読み取り専用・git管理外）
- data/processed/ - 加工済みデータ
- notebooks/      - 実験・分析用Jupyter Notebook
- tests/          - テストコード
- configs/        - 設定ファイル（YAML）""",
        "conventions": _PY_CONV_JA,
        "do_dont": _PY_DODONT_JA,
        "watch_out_for": """\
- GPU/CPU環境で乱数シードを固定しても数値結果が微妙に異なる場合がある
- データセットのファイルパスは絶対パスではなく pathlib.Path で相対記述する
- モデルチェックポイントファイル（*.pt, *.pkl）は data/ 以下に置くこと""",
    },
    "2": {
        "label": "データ分析",
        "type": "python",
        "commands": """\
uv run python src/main.py              # メイン処理実行
uv run pytest tests/ -v                # テスト実行
uv run ruff check src/ tests/          # リント
jupyter lab notebooks/                 # Notebook起動""",
        "architecture": """\
- src/           - 分析スクリプト
- src/utils/     - 共通ユーティリティ
- data/raw/      - 元データ（読み取り専用・git管理外）
- data/processed/- 加工済みデータ
- notebooks/     - 分析用Jupyter Notebook
- tests/         - テストコード
- outputs/       - 図表・レポート出力先""",
        "conventions": _PY_CONV_JA,
        "do_dont": _PY_DODONT_JA,
        "watch_out_for": """\
- データセットのファイルパスは絶対パスではなく pathlib.Path で相対記述する
- Notebook の実行順序に依存したコードを書かない（モジュールに切り出す）
- 可視化ライブラリのバージョンで出力が変わる場合がある""",
    },
    "3": {
        "label": "Web API (FastAPI)",
        "type": "python",
        "commands": """\
uv run uvicorn src.main:app --reload   # 開発サーバー起動
uv run pytest tests/ -v                # テスト実行
uv run ruff check src/ tests/          # リント
uv run mypy src/                       # 型チェック""",
        "architecture": """\
- src/            - アプリケーションコード
- src/routers/    - APIルーター
- src/models/     - Pydanticモデル・スキーマ
- src/services/   - ビジネスロジック
- src/utils/      - 共通ユーティリティ
- tests/          - テストコード""",
        "conventions": _PY_CONV_JA,
        "do_dont": """\
DO:
- 環境変数・秘密情報は .env に書き .gitignore 済みであることを確認する
- 依存性注入（Depends）を積極的に使い、テスト可能な設計にする
- 変更前に `uv run pytest` を実行して既存テストが通ることを確認する

DON'T:
- APIキー・パスワード等の秘密情報をコードにハードコードしない
- 非同期処理（async/await）と同期処理を混在させない
- 本番DBに直接つないだままテストを実行しない""",
        "watch_out_for": """\
- .env ファイルを絶対に git にコミットしない
- 非同期処理（async/await）の混在に注意する
- 依存性注入の循環参照に注意する""",
    },
    "4": {
        "label": "CLIツール",
        "type": "python",
        "commands": """\
uv run python src/main.py --help       # ヘルプ表示
uv run pytest tests/ -v                # テスト実行
uv run ruff check src/ tests/          # リント
uv run mypy src/                       # 型チェック""",
        "architecture": """\
- src/           - CLIコード（click / typer 等）
- src/commands/  - サブコマンド定義
- src/utils/     - 共通ユーティリティ
- tests/         - テストコード""",
        "conventions": _PY_CONV_JA,
        "do_dont": _PY_DODONT_JA,
        "watch_out_for": """\
- 終了コードを適切に設定する（正常: 0、エラー: 非0）
- stdin / stdout / stderr の使い分けを明確にする
- パスは pathlib.Path で扱い、OSの違いを吸収する""",
    },
    "5": {
        "label": "Pythonライブラリ",
        "type": "python",
        "commands": """\
uv run pytest tests/ -v                # テスト実行
uv run ruff check src/ tests/          # リント
uv run mypy src/                       # 型チェック
uv build                               # パッケージビルド""",
        "architecture": """\
- src/<package>/ - ライブラリ本体
- tests/         - テストコード
- docs/          - ドキュメント（Sphinx等）""",
        "conventions": _PY_CONV_JA,
        "do_dont": _PY_DODONT_JA,
        "watch_out_for": """\
- Python バージョン互換性の範囲を pyproject.toml で明示する
- 外部依存は必要最小限にする
- パブリック API（__all__）を明示的に定義する""",
    },
    "6": {
        "label": "LaTeX 論文執筆",
        "type": "latex",
        "commands": """\
latexmk -pdf main.tex              # PDF コンパイル
latexmk -c                         # 中間ファイルをクリーン
latexmk -pvc main.tex              # 自動コンパイル（監視モード）
# 日本語論文の場合:
latexmk -pdfdvi main.tex           # uplatex + dvipdfmx でコンパイル""",
        "architecture": """\
- main.tex        - メイン論文ファイル（\\input でセクションを読み込む）
- sections/       - セクション別 .tex ファイル
  - introduction.tex
  - method.tex
  - results.tex
  - discussion.tex
  - conclusion.tex
- figures/        - 図・グラフ（PDF / PNG 推奨）
- tables/         - 表（.tex 形式）
- refs.bib        - 参考文献（BibTeX 形式）
- styles/         - スタイルファイル・クラスファイル
- .latexmkrc      - latexmk 設定ファイル""",
        "conventions": _LATEX_CONV_JA,
        "do_dont": _LATEX_DODONT_JA,
        "watch_out_for": """\
- 日本語フォントは環境依存。TeX Live の場合 tlmgr で必要フォントをインストールする
- 図のファイル名にスペースや日本語を使わない
- BibTeX の cite key は FirstauthorYYYYkeyword 形式で統一すると管理しやすい
- latexmk の設定（.latexmkrc）はリポジトリに含めて環境を統一する""",
    },
    "7": {
        "label": "Word 論文執筆 (.docx)",
        "type": "word",
        "commands": """\
# Word / LibreOffice でファイルを直接編集する
# pandoc を使う場合（オプション）:
pandoc main.docx -o main.pdf       # PDF 変換
pandoc main.md -o main.docx        # Markdown から Word に変換
# 参考文献管理（Zotero を使う場合）:
# → Zotero デスクトップアプリ + Word プラグインを使用""",
        "architecture": """\
- docs/              - Word 文書（.docx）
  - paper_v1.0.docx  - 各バージョンのドラフト
  - paper_final.docx - 最終稿
- figures/           - 図・グラフ（元ファイル保管）
- tables/            - 表（Excel / CSV 形式）
- refs/              - 参考文献（.bib または Zotero エクスポート）""",
        "conventions": _WORD_CONV_JA,
        "do_dont": _WORD_DODONT_JA,
        "watch_out_for": """\
- APIキー・認証情報を絶対に git にコミットしない
- バイナリの .docx ファイルは git で差分が見えない
- プロジェクト全体でファイル命名規則を統一する""",
    },
    "8": {
        "label": "カスタム",
        "type": "custom",
        "commands": "",
        "architecture": "",
        "conventions": "",
        "do_dont": "",
        "watch_out_for": "",
    },
}

ALL_PRESETS: dict[str, dict[str, dict[str, str]]] = {
    "en": PRESETS_EN,
    "ja": PRESETS_JA,
}

# LaTeX .gitignore additions (language-independent)
LATEX_GITIGNORE_EXTRA = """\

# LaTeX compiled output
*.aux
*.log
*.out
*.toc
*.lof
*.lot
*.bbl
*.blg
*.synctex.gz
*.fls
*.fdb_latexmk
*.nav
*.snm
*.vrb
*.xdv
"""

# ---------------------------------------------------------------------------
# Python version check
# ---------------------------------------------------------------------------


def check_python_version(m: dict[str, str]) -> None:
    """Warn if the current Python version is below the recommended minimum.

    Args:
        m: Message dict for the selected language.
    """
    cur = sys.version_info[:2]
    ver = f"{cur[0]}.{cur[1]}.{sys.version_info[2]}"
    if cur < MIN_PYTHON:
        min_str = f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
        print(m["python_warn"].format(ver=ver, min=min_str))
    else:
        print(m["python_ok"].format(ver=ver))


# ---------------------------------------------------------------------------
# uv check and install
# ---------------------------------------------------------------------------


def _get_uv_install_cmd() -> list[str]:
    """Return the OS-appropriate uv install command.

    Returns:
        Command list for subprocess.run.
    """
    if OS == "Windows":
        return [
            "powershell",
            "-ExecutionPolicy", "ByPass",
            "-c", "irm https://astral.sh/uv/install.ps1 | iex",
        ]
    return ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]


def _show_uv_instructions(m: dict[str, str]) -> None:
    """Print OS-specific uv install instructions.

    Args:
        m: Message dict for the selected language.
    """
    print(m["uv_install_header"])
    if OS == "Windows":
        print(m["uv_win_label"])
        print(
            '    powershell -ExecutionPolicy ByPass -c'
            ' "irm https://astral.sh/uv/install.ps1 | iex"'
        )
    elif OS == "Darwin":
        print(m["uv_unix_label"])
        print("    curl -LsSf https://astral.sh/uv/install.sh | sh")
        print(m["uv_homebrew"])
        print("    brew install uv")
    else:
        print(m["uv_unix_label"])
        print("    curl -LsSf https://astral.sh/uv/install.sh | sh")
    print(m["uv_install_footer"])


def _install_uv(m: dict[str, str]) -> bool:
    """Attempt to auto-install uv.

    Args:
        m: Message dict for the selected language.

    Returns:
        True if installation succeeded.
    """
    if OS != "Windows" and not shutil.which("curl"):
        print(m["no_curl"])
        _show_uv_instructions(m)
        return False

    print(m["uv_installing"])
    cmd = _get_uv_install_cmd()
    try:
        result = subprocess.run(cmd, check=False)
    except FileNotFoundError as exc:
        print(m["uv_cmd_not_found"].format(e=exc))
        return False

    if result.returncode != 0:
        print(m["uv_install_failed"])
        _show_uv_instructions(m)
        return False

    print(m["uv_install_ok"])
    print()
    print(m["uv_restart"])
    if OS == "Windows":
        print(m["uv_restart_win"])
    else:
        print(m["uv_restart_unix"])
    return True


def check_and_setup_uv(m: dict[str, str]) -> bool:
    """Check whether uv is available; offer to install if not.

    Args:
        m: Message dict for the selected language.

    Returns:
        True if uv is available after the check.
    """
    if shutil.which("uv"):
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=False
        )
        print(m["uv_ok"].format(ver=result.stdout.strip()))
        return True

    print()
    print(m["uv_ng"])
    print(m["uv_desc"])
    print()
    _show_uv_instructions(m)
    print()

    choice = _prompt(m["uv_install_prompt"], default="y", m=m).lower()
    if choice not in ("y", "yes", ""):
        print(m["uv_manual"])
        return False

    return _install_uv(m)


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------


def _prompt(message: str, default: str = "", m: dict[str, str] | None = None) -> str:
    """Prompt for user input with an optional default.

    Args:
        message: Prompt text to display.
        default: Value to use if the user presses Enter without input.
        m: Message dict (used for interrupt message only).

    Returns:
        User input, or the default value if empty.
    """
    hint = f" [{default}]" if default else ""
    try:
        value = input(f"{message}{hint}: ").strip()
    except (KeyboardInterrupt, EOFError):
        interrupted_msg = (m or {}).get("interrupted", "\n\nCancelled.")
        print(interrupted_msg)
        sys.exit(0)
    return value if value else default


def _prompt_multiline(label: str, m: dict[str, str]) -> str:
    """Prompt for multi-line input, terminated by an empty line.

    Args:
        label: Description of the input field.
        m: Message dict for the selected language.

    Returns:
        Multi-line string entered by the user.
    """
    print(f"{m['input_label'].format(label=label)} {m['multiline_end']}:")
    lines: list[str] = []
    try:
        while True:
            line = input("  ")
            if line == "":
                break
            lines.append(line)
    except (KeyboardInterrupt, EOFError):
        print(m["interrupted"])
        sys.exit(0)
    return "\n".join(lines)


def _ask_use_default(label: str, default_text: str, m: dict[str, str]) -> str:
    """Show a default value and ask whether to use it or enter a custom one.

    Args:
        label: Field label for display.
        default_text: Default content to show.
        m: Message dict for the selected language.

    Returns:
        The selected or manually entered text.
    """
    print(f"\n{label}:")
    print(default_text)
    use_default = _prompt(m["default_check"], default="y", m=m).lower()
    if use_default == "n":
        return _prompt_multiline(label, m)
    return default_text


def select_preset(
    presets: dict[str, dict[str, str]], m: dict[str, str]
) -> dict[str, str]:
    """Present the project type menu and return the chosen preset.

    Args:
        presets: Preset dict for the selected language.
        m: Message dict for the selected language.

    Returns:
        The selected preset dict.
    """
    print("\n" + "=" * 54)
    print(f"  {m['preset_title']}")
    print("=" * 54)
    for key, preset in presets.items():
        print(f"  {key}. {preset['label']}")
    print("=" * 54)

    while True:
        choice = _prompt(m["prompt_number"], default="1", m=m)
        if choice in presets:
            selected = presets[choice]
            print(f"\n{m['preset_selected'].format(label=selected['label'])}")
            return selected
        print(m["preset_invalid"].format(n=len(presets)))


# ---------------------------------------------------------------------------
# File generation
# ---------------------------------------------------------------------------


def generate_agents_md(
    name: str,
    description: str,
    commands: str,
    architecture: str,
    conventions: str,
    do_dont: str,
    watch_out_for: str,
) -> str:
    """Generate the content of AGENTS.md.

    Args:
        name: Project name.
        description: Project description.
        commands: Commands section content.
        architecture: Architecture section content.
        conventions: Conventions section content.
        do_dont: Do/Don't section content.
        watch_out_for: Watch out for section content.

    Returns:
        AGENTS.md content as a string.
    """
    return f"""\
# {name}

{description}

## Commands
{commands}

## Architecture
{architecture}

## Conventions
{conventions}

## Do / Don't
{do_dont}

## Watch out for
{watch_out_for}
"""


def _readme_python_en(name: str, description: str) -> str:
    return f"""\
# {name}

{description}

## Setup

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest tests/ -v
```

## Key Commands

| Command | Description |
|---|---|
| `uv run pytest tests/ -v` | Run tests |
| `uv run ruff check src/ tests/` | Lint |
| `uv run mypy src/` | Type check |
| `/project:test-run` | Run tests & summarize (Claude Code) |
| `/project:check-conventions` | Check conventions (Claude Code) |

## Directory Structure

See `AGENTS.md` for details.
"""


def _readme_python_ja(name: str, description: str) -> str:
    return f"""\
# {name}

{description}

## セットアップ

```bash
# 依存パッケージのインストール
uv sync

# テスト実行
uv run pytest tests/ -v
```

## 主なコマンド

| コマンド | 内容 |
|---|---|
| `uv run pytest tests/ -v` | テスト実行 |
| `uv run ruff check src/ tests/` | リント |
| `uv run mypy src/` | 型チェック |
| `/project:test-run` | Claude Code でテスト実行＆サマリー |
| `/project:check-conventions` | Claude Code で規約チェック |

## ディレクトリ構成

詳細は `AGENTS.md` を参照してください。
"""


def _readme_latex_en(name: str, description: str) -> str:
    return f"""\
# {name}

{description}

## Requirements

- TeX Live 2022+ or MiKTeX (Windows)
- latexmk (included with TeX Live)
- (Optional) Zotero + BetterBibTeX plugin for reference management

## Setup

### Windows (MiKTeX)
```powershell
# Download MiKTeX installer from https://miktex.org/download
```

### macOS
```bash
brew install --cask mactex-no-gui
```

### Linux (Ubuntu / Debian)
```bash
sudo apt install texlive-full latexmk
```

## Compile

```bash
latexmk -pdf main.tex   # Compile to PDF
latexmk -c              # Clean intermediate files
```

## Directory Structure

See `AGENTS.md` for details.
"""


def _readme_latex_ja(name: str, description: str) -> str:
    return f"""\
# {name}

{description}

## 必要なツール

- TeX Live 2022+ または MiKTeX（Windows）
- latexmk（TeX Live に含まれる）
- （オプション）Zotero + BetterBibTeX プラグイン（参考文献管理）

## セットアップ

### Windows (MiKTeX)
```powershell
# MiKTeX インストーラーを公式サイトからダウンロード
# https://miktex.org/download
```

### macOS
```bash
brew install --cask mactex-no-gui
```

### Linux (Ubuntu / Debian)
```bash
sudo apt install texlive-full latexmk
```

## コンパイル

```bash
latexmk -pdf main.tex   # PDF コンパイル
latexmk -c              # 中間ファイルをクリーン
```

## ディレクトリ構成

詳細は `AGENTS.md` を参照してください。
"""


def _readme_word_en(name: str, description: str) -> str:
    return f"""\
# {name}

{description}

## Requirements

- Microsoft Word or LibreOffice Writer
- (Recommended) Zotero + Word plugin for reference management
- (Optional) pandoc for format conversion

## Install pandoc (optional)

### Windows
```powershell
winget install JohnMacFarlane.Pandoc
```

### macOS
```bash
brew install pandoc
```

### Linux
```bash
sudo apt install pandoc
```

## File Conversion (with pandoc)

```bash
pandoc docs/paper_final.docx -o docs/paper_final.pdf
pandoc draft.md -o docs/paper_draft.docx --reference-doc=styles/template.docx
```

## Directory Structure

See `AGENTS.md` for details.
"""


def _readme_word_ja(name: str, description: str) -> str:
    return f"""\
# {name}

{description}

## 必要なツール

- Microsoft Word または LibreOffice Writer
- （推奨）Zotero + Word プラグイン（参考文献管理）
- （オプション）pandoc（形式変換）

## pandoc のインストール（オプション）

### Windows
```powershell
winget install JohnMacFarlane.Pandoc
```

### macOS
```bash
brew install pandoc
```

### Linux
```bash
sudo apt install pandoc
```

## ファイル変換（pandoc を使う場合）

```bash
pandoc docs/paper_final.docx -o docs/paper_final.pdf
pandoc draft.md -o docs/paper_draft.docx --reference-doc=styles/template.docx
```

## ディレクトリ構成

詳細は `AGENTS.md` を参照してください。
"""


def generate_readme(
    preset_type: str, name: str, description: str, lang: str
) -> str:
    """Generate README.md content for the given project type and language.

    Args:
        preset_type: "python" | "latex" | "word" | "custom"
        name: Project name.
        description: Project description.
        lang: "en" or "ja"

    Returns:
        README.md content as a string.
    """
    if preset_type == "latex":
        return _readme_latex_en(name, description) if lang == "en" else _readme_latex_ja(name, description)
    if preset_type == "word":
        return _readme_word_en(name, description) if lang == "en" else _readme_word_ja(name, description)
    return _readme_python_en(name, description) if lang == "en" else _readme_python_ja(name, description)


def update_pyproject(name: str, description: str) -> None:
    """Update the project name and description in pyproject.toml.

    Args:
        name: Project name (will be slugified).
        description: Project description.
    """
    path = ROOT / "pyproject.toml"
    if not path.exists():
        return
    slug = name.lower().replace(" ", "-").replace("_", "-")
    content = path.read_text(encoding="utf-8")
    content = re.sub(
        r'^name\s*=\s*".+"', f'name = "{slug}"', content, flags=re.MULTILINE
    )
    content = re.sub(
        r'^description\s*=\s*".+"',
        f'description = "{description}"',
        content,
        flags=re.MULTILINE,
    )
    path.write_text(content, encoding="utf-8")


def append_gitignore(extra: str) -> None:
    """Append patterns to the existing .gitignore.

    Args:
        extra: Patterns to append.
    """
    path = ROOT / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if extra.strip() not in existing:
        path.write_text(existing + extra, encoding="utf-8")


def create_latex_skeleton() -> None:
    """Create the LaTeX project directory structure and skeleton files."""
    for d in [ROOT / "sections", ROOT / "figures", ROOT / "tables", ROOT / "styles"]:
        d.mkdir(exist_ok=True)
        (d / ".gitkeep").touch()

    main_tex = ROOT / "main.tex"
    if not main_tex.exists():
        main_tex.write_text(
            r"""\documentclass[12pt]{article}
% \documentclass[12pt]{jlreq}  % For Japanese papers

\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage[backend=biber, style=authoryear]{biblatex}

\addbibresource{refs.bib}

\title{Paper Title}
\author{Author Name}
\date{\today}

\begin{document}

\maketitle

\input{sections/introduction}
\input{sections/method}
\input{sections/results}
\input{sections/discussion}
\input{sections/conclusion}

\printbibliography

\end{document}
""",
            encoding="utf-8",
        )

    for sec in ["introduction", "method", "results", "discussion", "conclusion"]:
        tex_file = ROOT / "sections" / f"{sec}.tex"
        if not tex_file.exists():
            tex_file.write_text(
                f"\\section{{{sec.capitalize()}}}\n\n% TODO: Write content here\n",
                encoding="utf-8",
            )

    refs_bib = ROOT / "refs.bib"
    if not refs_bib.exists():
        refs_bib.write_text(
            "% Add references in BibTeX format\n"
            "% Example:\n"
            "% @article{Smith2024example,\n"
            "%   author  = {Smith, John},\n"
            "%   title   = {Example Title},\n"
            "%   journal = {Journal Name},\n"
            "%   year    = {2024},\n"
            "% }\n",
            encoding="utf-8",
        )

    latexmkrc = ROOT / ".latexmkrc"
    if not latexmkrc.exists():
        latexmkrc.write_text(
            "# latexmk configuration\n"
            "# Direct PDF generation (pdflatex)\n"
            "$pdf_mode = 1;\n"
            "\n"
            "# For Japanese papers (uplatex + dvipdfmx), comment out above and use:\n"
            "# $latex = 'uplatex %O %S';\n"
            "# $bibtex = 'upbibtex %O %B';\n"
            "# $dvipdf = 'dvipdfmx %O -o %D %S';\n"
            "# $pdf_mode = 3;\n",
            encoding="utf-8",
        )


def create_word_skeleton() -> None:
    """Create the Word project directory structure."""
    for d in [
        ROOT / "docs",
        ROOT / "figures",
        ROOT / "tables",
        ROOT / "refs",
        ROOT / "data",
    ]:
        d.mkdir(exist_ok=True)
        (d / ".gitkeep").touch()


# ---------------------------------------------------------------------------
# Language selection
# ---------------------------------------------------------------------------


def select_language() -> str:
    """Prompt the user to select a language, or auto-detect from locale.

    Returns:
        "en" or "ja"
    """
    detected = _detect_lang()
    prompt = "Select language / 言語を選択 [en/ja]"
    try:
        raw = input(f"{prompt} [{detected}]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled. / 中断しました。")
        sys.exit(0)
    if raw in ("en", "ja"):
        return raw
    return detected


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Interactively collect project information and generate configuration files."""
    # --- Language selection (first, before anything else) ---
    lang = _detect_lang()
    # Only show the prompt if --lang was NOT explicitly given
    if not any(
        a.startswith("--lang") for a in sys.argv[1:]
    ):
        lang = select_language()

    m = MESSAGES[lang]
    presets = ALL_PRESETS[lang]

    print("\n" + "=" * 54)
    print(f"  {m['title']}")
    print("=" * 54)
    print(m["subtitle"])
    print(m["interrupt_hint"])
    print()

    # --- Python version check ---
    check_python_version(m)

    # --- Project type selection ---
    preset = select_preset(presets, m)
    preset_type = preset["type"]

    # --- uv check (Python projects only) ---
    if preset_type in ("python", "custom"):
        print()
        print(m["uv_section"])
        check_and_setup_uv(m)

    # --- Basic info ---
    print()
    name = _prompt(m["prompt_name"], default=m["default_name"], m=m)
    description = _prompt(m["prompt_desc"], default=m["default_desc"], m=m)

    # --- Commands ---
    commands = (
        _ask_use_default(m["label_commands"], preset["commands"], m)
        if preset["commands"]
        else _prompt_multiline(m["label_commands"], m)
    )

    # --- Architecture ---
    architecture = (
        _ask_use_default(m["label_arch"], preset["architecture"], m)
        if preset["architecture"]
        else _prompt_multiline(m["label_arch"], m)
    )

    # --- Conventions (custom preset: choose type) ---
    if preset_type == "custom":
        print(f"\n{m['conv_select']}")
        for opt in m["conv_options"]:
            print(f"  {opt}")
        conv_choice = _prompt(m["prompt_number"], default="1", m=m)
        conv_map: dict[str, str] = {
            "1": _PY_CONV_EN if lang == "en" else _PY_CONV_JA,
            "2": _LATEX_CONV_EN if lang == "en" else _LATEX_CONV_JA,
            "3": _WORD_CONV_EN if lang == "en" else _WORD_CONV_JA,
        }
        conventions = conv_map.get(conv_choice) or _prompt_multiline(m["label_conv"], m)
        do_dont = _prompt_multiline(m["dodont_label"], m)
    else:
        conventions = preset["conventions"]
        do_dont = preset["do_dont"]

    # --- Watch out for ---
    watch_out_for = (
        _ask_use_default(m["label_watch"], preset["watch_out_for"], m)
        if preset["watch_out_for"]
        else _prompt_multiline(m["label_watch"], m)
    )

    # --- Confirmation ---
    print("\n" + "=" * 54)
    print(m["confirm_header"])
    print("=" * 54)
    print(m["confirm_name"].format(v=name))
    print(m["confirm_type"].format(v=preset["label"]))
    print(m["confirm_desc"].format(v=description))
    print(m["confirm_files"])
    if preset_type in ("python", "custom"):
        print(m["confirm_pyproject"])
    print("=" * 54)

    confirm = _prompt(f"\n{m['proceed']}", default="y", m=m).lower()
    if confirm not in ("y", "yes", ""):
        print(m["aborted"])
        sys.exit(0)

    print()

    # --- Write AGENTS.md ---
    agents_content = generate_agents_md(
        name, description, commands, architecture, conventions, do_dont, watch_out_for
    )
    (ROOT / "AGENTS.md").write_text(agents_content, encoding="utf-8")
    print(m["written"].format(f="AGENTS.md"))

    # --- Write CLAUDE.md / GEMINI.md ---
    (ROOT / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    print(m["written"].format(f="CLAUDE.md"))
    (ROOT / "GEMINI.md").write_text("@AGENTS.md\n", encoding="utf-8")
    print(m["written"].format(f="GEMINI.md"))

    # --- Write README.md ---
    readme_content = generate_readme(preset_type, name, description, lang)
    (ROOT / "README.md").write_text(readme_content, encoding="utf-8")
    print(m["written"].format(f="README.md"))

    # --- Update pyproject.toml (Python only) ---
    if preset_type in ("python", "custom"):
        update_pyproject(name, description)
        print(m["written"].format(f="pyproject.toml"))

    # --- LaTeX-specific ---
    if preset_type == "latex":
        append_gitignore(LATEX_GITIGNORE_EXTRA)
        print(m["latex_gitignore"])
        create_latex_skeleton()
        print(m["latex_skeleton"])

    # --- Word-specific ---
    if preset_type == "word":
        create_word_skeleton()
        print(m["word_skeleton"])

    # --- Done ---
    print()
    print("=" * 54)
    print(f"  {m['done']}")
    print("=" * 54)
    if preset_type == "latex":
        print(m["next_latex"])
    elif preset_type == "word":
        print(m["next_word"])
    else:
        print(m["next_python"])
    print("=" * 54)
    print()


if __name__ == "__main__":
    main()
