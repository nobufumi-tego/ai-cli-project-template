"""プロジェクト初期化スクリプト。

対話形式でプロジェクト情報を収集し、AGENTS.md・CLAUDE.md・GEMINI.md・
README.md・pyproject.toml を自動生成する。
uv が未インストールの場合は OS を自動判定してインストールを支援する。

対応 OS: Windows 11 / macOS / Linux
対応プロジェクト種別: Python（ML・分析・API・CLI・ライブラリ）/ LaTeX / Word

Usage:
    python  scripts/init-project.py   # Windows
    python3 scripts/init-project.py   # macOS / Linux
"""

from __future__ import annotations

import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

# プロジェクトルートを基準にパスを解決する
ROOT = Path(__file__).parent.parent

# Python 最低バージョン（警告のみ。スクリプト自体は 3.8 以上で動作する）
MIN_PYTHON: tuple[int, int] = (3, 10)


# ---------------------------------------------------------------------------
# プリセット定義
# type: "python" | "latex" | "word" | "custom"
# ---------------------------------------------------------------------------

PYTHON_CONVENTIONS = """\
- 型ヒント必須（Python 3.10+）
- すべての関数・クラスにdocstringを書く（Google スタイル）
- 数値の単位はコメントまたは変数名で明記（例: `duration_sec`, `size_mb`）
- マジックナンバーはすべて定数化（各モジュール先頭または `configs/` に定義）
- エラーハンドリングを省略しない
- `os.path` ではなく `pathlib.Path` を使う
- 絶対パスをハードコードしない"""

PYTHON_DO_DONT = """\
DO:
- 変更前に `uv run pytest` を実行して既存テストが通ることを確認する
- 新しい機能を追加したらテストも同時に追加する
- data/raw/ のファイルは読み取りのみ。加工結果は data/processed/ へ

DON'T:
- 大容量ファイル（動画・モデルチェックポイント等）をgit管理しない（.gitignore 設定済み）
- GPU/CPU環境依存のハードコードをしない
- data/raw/ のファイルを直接編集しない"""

LATEX_CONVENTIONS = """\
- セクション別に .tex ファイルを分割し、main.tex で \\input{sections/...} する
- 図のパスは相対パスで記述する（例: \\includegraphics{figures/fig1.pdf}）
- 参考文献は refs.bib にまとめ、\\citep / \\citet コマンドで引用する
- 変更理由をコメントで残す（例: % [2024-01-15] reviewer の指摘で修正）
- 日本語論文は uplatex + dvipdfmx または LuaLaTeX を使う
- 英語論文の句読点は period（.）と comma（,）で統一する"""

LATEX_DO_DONT = """\
DO:
- 変更前に git commit して履歴を残す
- 図・表を追加したら必ずコンパイルして見た目を確認する
- 参考文献は追加の都度 refs.bib を整理する

DON'T:
- コンパイル生成ファイル（*.aux, *.log 等）をgit管理しない（.gitignore 設定済み）
- main.tex に全文を書かない（sections/ に分割する）
- バックアップなしに大幅な書き換えをしない"""

LATEX_GITIGNORE_EXTRA = """\

# LaTeX コンパイル生成ファイル
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

WORD_CONVENTIONS = """\
- ファイル名にバージョン番号または日付を含める（例: paper_v2.1_20240115.docx）
- 見出し・本文・図タイトル等はスタイルを統一して使う（直接書式を多用しない）
- 図はインライン図として挿入し、テキストボックスに入れない
- 参考文献は Zotero 等の文献管理ツールで管理する
- 変更履歴が必要な場合は「変更履歴の記録」機能を使う（手動の取り消し線は禁止）"""

WORD_DO_DONT = """\
DO:
- 定期的に git で管理して変更履歴を残す（バイナリ差分は見えないが存在を記録できる）
- 提出前にトラックチェンジをすべて承認してクリーンな状態にする
- フォントは本文・見出しとも埋め込み設定で保存する

DON'T:
- 最終稿以外の多数の .docx を git 管理しない（バイナリ差分が見えない）
- 図の位置をスペースや改行で調整しない（図の配置設定を使う）
- コメント・変更履歴を残したまま提出しない"""

PRESETS: dict[str, dict[str, str]] = {
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
        "conventions": PYTHON_CONVENTIONS,
        "do_dont": PYTHON_DO_DONT,
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
        "conventions": PYTHON_CONVENTIONS,
        "do_dont": PYTHON_DO_DONT,
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
        "conventions": PYTHON_CONVENTIONS,
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
        "conventions": PYTHON_CONVENTIONS,
        "do_dont": PYTHON_DO_DONT,
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
        "conventions": PYTHON_CONVENTIONS,
        "do_dont": PYTHON_DO_DONT,
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
        "conventions": LATEX_CONVENTIONS,
        "do_dont": LATEX_DO_DONT,
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
- refs/              - 参考文献（.bib または Zotero エクスポート）
- data/              - 参照データ・統計結果""",
        "conventions": WORD_CONVENTIONS,
        "do_dont": WORD_DO_DONT,
        "watch_out_for": """\
- .docx はバイナリファイルのため git diff で内容が見えない（コミット粒度を粗くする）
- 異なるバージョンの Word で開くとレイアウトが崩れる場合がある
- 図の解像度は印刷時 300 dpi 以上、画面表示用は 96 dpi で保存する""",
    },
    "8": {
        "label": "カスタム（全項目を手動入力）",
        "type": "custom",
        "commands": "",
        "architecture": "",
        "conventions": "",
        "do_dont": "",
        "watch_out_for": "",
    },
}


# ---------------------------------------------------------------------------
# Python バージョンチェック
# ---------------------------------------------------------------------------


def check_python_version() -> None:
    """Python バージョンを確認し、推奨未満の場合は警告する。"""
    current = sys.version_info[:2]
    if current < MIN_PYTHON:
        print(
            f"  ! Python {current[0]}.{current[1]} を使用中です。"
            f" Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ を推奨します。"
        )
    else:
        print(f"  ✓ Python {current[0]}.{current[1]}")


# ---------------------------------------------------------------------------
# uv チェック・インストール
# ---------------------------------------------------------------------------


def _get_uv_install_command() -> list[str]:
    """OS に応じた uv インストールコマンドを返す。

    Returns:
        subprocess.run に渡すコマンドリスト
    """
    os_name = platform.system()
    if os_name == "Windows":
        return [
            "powershell",
            "-ExecutionPolicy",
            "ByPass",
            "-c",
            "irm https://astral.sh/uv/install.ps1 | iex",
        ]
    # macOS / Linux
    return ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]


def _show_uv_install_instructions() -> None:
    """OS に応じた uv の手動インストール手順を表示する。"""
    os_name = platform.system()
    print("  ─── uv インストール方法 ───")
    if os_name == "Windows":
        print("  PowerShell（管理者）で実行：")
        print(
            '    powershell -ExecutionPolicy ByPass -c'
            ' "irm https://astral.sh/uv/install.ps1 | iex"'
        )
    elif os_name == "Darwin":
        print("  ターミナルで実行：")
        print("    curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("  または（Homebrew）：")
        print("    brew install uv")
    else:
        print("  ターミナルで実行：")
        print("    curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("  ─────────────────────────")


def _install_uv() -> bool:
    """OS に応じて uv を自動インストールする。

    Returns:
        インストールに成功した場合 True、失敗した場合 False
    """
    os_name = platform.system()

    if os_name != "Windows" and not shutil.which("curl"):
        print("  ! curl が見つかりません。手動でインストールしてください。")
        _show_uv_install_instructions()
        return False

    print("  インストール中...")
    cmd = _get_uv_install_command()
    try:
        result = subprocess.run(cmd, check=False)
    except FileNotFoundError as exc:
        print(f"  ✗ コマンドが見つかりません: {exc}")
        return False

    if result.returncode != 0:
        print("  ✗ インストールに失敗しました。手動でインストールしてください。")
        _show_uv_install_instructions()
        return False

    print("  ✓ インストールが完了しました。")
    print()
    print("  ! PATH を更新するためターミナルを再起動してください。")
    if os_name == "Windows":
        print(
            '    または PowerShell で実行：'
            ' $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","User")'
        )
    else:
        print("    または: source ~/.bashrc  （~/.zshrc / ~/.config/fish/config.fish 等）")
    return True


def check_and_setup_uv() -> bool:
    """uv のインストール状況を確認し、必要に応じてインストールを支援する。

    Returns:
        uv が利用可能な場合 True、そうでない場合 False
    """
    if shutil.which("uv"):
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=False
        )
        print(f"  ✓ uv: {result.stdout.strip()}")
        return True

    print()
    print("  ! uv が見つかりません。")
    print("  uv は高速な Python パッケージマネージャーです（このテンプレートで使用）。")
    print()
    _show_uv_install_instructions()
    print()

    choice = _prompt("  今すぐ自動インストールを試みますか？", default="y").lower()
    if choice not in ("y", "yes", ""):
        print("  上記コマンドを手動で実行してから、スクリプトを再度実行してください。")
        return False

    return _install_uv()


# ---------------------------------------------------------------------------
# 入力ヘルパー
# ---------------------------------------------------------------------------


def _prompt(message: str, default: str = "") -> str:
    """ユーザーに入力を促す。

    Args:
        message: 表示するメッセージ
        default: 空白入力時のデフォルト値

    Returns:
        ユーザーの入力値（空白の場合はデフォルト値）
    """
    hint = f" [{default}]" if default else ""
    try:
        value = input(f"{message}{hint}: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n中断しました。")
        sys.exit(0)
    return value if value else default


def _prompt_multiline(message: str) -> str:
    """複数行の入力を受け付ける。空行で終了。

    Args:
        message: 表示するメッセージ

    Returns:
        入力された複数行テキスト
    """
    print(f"{message}（空行で入力終了）:")
    lines: list[str] = []
    try:
        while True:
            line = input("  ")
            if line == "":
                break
            lines.append(line)
    except (KeyboardInterrupt, EOFError):
        print("\n\n中断しました。")
        sys.exit(0)
    return "\n".join(lines)


def _ask_use_default(label: str, default_text: str) -> str:
    """デフォルト値を表示して使うかどうか確認する。

    Args:
        label: 項目ラベル（例: "コマンド"）
        default_text: デフォルトのテキスト

    Returns:
        最終的に使用するテキスト
    """
    print(f"\nデフォルトの{label}:")
    print(default_text)
    use_default = _prompt("このまま使いますか？", default="y").lower()
    if use_default == "n":
        return _prompt_multiline(f"{label}を入力")
    return default_text


def select_preset() -> dict[str, str]:
    """プロジェクト種別を選択させる。

    Returns:
        選択されたプリセット辞書
    """
    print("\n" + "=" * 54)
    print("  プロジェクト種別を選択してください：")
    print("=" * 54)
    for key, preset in PRESETS.items():
        print(f"  {key}. {preset['label']}")
    print("=" * 54)

    while True:
        choice = _prompt("番号を入力", default="1")
        if choice in PRESETS:
            selected = PRESETS[choice]
            print(f"\n→ 「{selected['label']}」を選択しました。\n")
            return selected
        print(f"  1〜{len(PRESETS)} の番号を入力してください。")


# ---------------------------------------------------------------------------
# ファイル生成
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
    """AGENTS.md の内容を生成する。

    Args:
        name: プロジェクト名
        description: プロジェクト説明
        commands: コマンド一覧（複数行）
        architecture: フォルダ構成（複数行）
        conventions: 規約一覧（複数行）
        do_dont: Do / Don't（複数行）
        watch_out_for: 注意事項（複数行）

    Returns:
        AGENTS.md のテキスト
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


def generate_readme_python(name: str, description: str) -> str:
    """Python プロジェクト用 README.md を生成する。

    Args:
        name: プロジェクト名
        description: プロジェクト説明

    Returns:
        README.md のテキスト
    """
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


def generate_readme_latex(name: str, description: str) -> str:
    """LaTeX プロジェクト用 README.md を生成する。

    Args:
        name: プロジェクト名
        description: プロジェクト説明

    Returns:
        README.md のテキスト
    """
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
# Homebrew でインストール
brew install --cask mactex-no-gui
```

### Linux (Ubuntu / Debian)
```bash
sudo apt install texlive-full latexmk
```

## コンパイル

```bash
# PDF コンパイル
latexmk -pdf main.tex

# 中間ファイルをクリーン
latexmk -c
```

## ディレクトリ構成

詳細は `AGENTS.md` を参照してください。
"""


def generate_readme_word(name: str, description: str) -> str:
    """Word プロジェクト用 README.md を生成する。

    Args:
        name: プロジェクト名
        description: プロジェクト説明

    Returns:
        README.md のテキスト
    """
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
# Word → PDF
pandoc docs/paper_final.docx -o docs/paper_final.pdf

# Markdown → Word
pandoc draft.md -o docs/paper_draft.docx --reference-doc=styles/template.docx
```

## ディレクトリ構成

詳細は `AGENTS.md` を参照してください。
"""


def update_pyproject(name: str, description: str) -> None:
    """pyproject.toml のプロジェクト名と説明を更新する。

    Args:
        name: プロジェクト名（スラッグに正規化）
        description: プロジェクト説明
    """
    path = ROOT / "pyproject.toml"
    if not path.exists():
        return

    slug = name.lower().replace(" ", "-").replace("_", "-")
    content = path.read_text(encoding="utf-8")
    content = re.sub(r'^name\s*=\s*".+"', f'name = "{slug}"', content, flags=re.MULTILINE)
    content = re.sub(
        r'^description\s*=\s*".+"',
        f'description = "{description}"',
        content,
        flags=re.MULTILINE,
    )
    path.write_text(content, encoding="utf-8")


def append_gitignore(extra: str) -> None:
    """既存の .gitignore にパターンを追記する。

    Args:
        extra: 追記するパターン文字列
    """
    path = ROOT / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if extra.strip() not in existing:
        path.write_text(existing + extra, encoding="utf-8")


def create_latex_skeleton() -> None:
    """LaTeX プロジェクトの基本ディレクトリと骨格ファイルを作成する。"""
    dirs = [
        ROOT / "sections",
        ROOT / "figures",
        ROOT / "tables",
        ROOT / "styles",
    ]
    for d in dirs:
        d.mkdir(exist_ok=True)
        (d / ".gitkeep").touch()

    # main.tex 骨格
    main_tex = ROOT / "main.tex"
    if not main_tex.exists():
        main_tex.write_text(
            r"""\documentclass[12pt]{article}
% \documentclass[12pt]{jlreq}  % 日本語論文の場合

\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage[backend=biber, style=authoryear]{biblatex}

\addbibresource{refs.bib}

\title{論文タイトル}
\author{著者名}
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

    # セクション骨格
    for sec in ["introduction", "method", "results", "discussion", "conclusion"]:
        tex_file = ROOT / "sections" / f"{sec}.tex"
        if not tex_file.exists():
            tex_file.write_text(
                f"\\section{{{sec.capitalize()}}}\n\n% TODO: ここに本文を書く\n",
                encoding="utf-8",
            )

    # refs.bib
    refs_bib = ROOT / "refs.bib"
    if not refs_bib.exists():
        refs_bib.write_text(
            "% 参考文献を BibTeX 形式で記述する\n"
            "% 例:\n"
            "% @article{Smith2024example,\n"
            "%   author  = {Smith, John},\n"
            "%   title   = {Example Title},\n"
            "%   journal = {Journal Name},\n"
            "%   year    = {2024},\n"
            "% }\n",
            encoding="utf-8",
        )

    # .latexmkrc
    latexmkrc = ROOT / ".latexmkrc"
    if not latexmkrc.exists():
        latexmkrc.write_text(
            "# latexmk 設定ファイル\n"
            "# PDF 直接生成（pdflatex）\n"
            "$pdf_mode = 1;\n"
            "\n"
            "# 日本語論文（uplatex + dvipdfmx）の場合は上をコメントアウトして下を使う:\n"
            "# $latex = 'uplatex %O %S';\n"
            "# $bibtex = 'upbibtex %O %B';\n"
            "# $dvipdf = 'dvipdfmx %O -o %D %S';\n"
            "# $pdf_mode = 3;\n",
            encoding="utf-8",
        )


def create_word_skeleton() -> None:
    """Word プロジェクトの基本ディレクトリを作成する。"""
    dirs = [
        ROOT / "docs",
        ROOT / "figures",
        ROOT / "tables",
        ROOT / "refs",
        ROOT / "data",
    ]
    for d in dirs:
        d.mkdir(exist_ok=True)
        (d / ".gitkeep").touch()


# ---------------------------------------------------------------------------
# 次のステップ表示
# ---------------------------------------------------------------------------

_NEXT_STEPS_PYTHON = """\
次のステップ：
  1. uv sync                 # 依存パッケージをインストール
  2. uv run pytest tests/    # テスト実行で動作確認
  3. AGENTS.md を育てる      # プロジェクト固有の情報を追記していく"""

_NEXT_STEPS_LATEX = """\
次のステップ：
  1. TeX 環境を確認する      # README.md のセットアップ手順を参照
  2. sections/*.tex を編集する
  3. latexmk -pdf main.tex  # PDF をコンパイル"""

_NEXT_STEPS_WORD = """\
次のステップ：
  1. docs/ フォルダに .docx ファイルを作成する
  2. Zotero 等の参考文献管理ツールを設定する
  3. README.md に執筆ガイドラインを追記する"""


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------


def main() -> None:
    """対話形式でプロジェクト情報を収集し、各ファイルを生成する。"""
    print("\n" + "=" * 54)
    print("  AI CLI プロジェクト初期化スクリプト")
    print("=" * 54)
    print("質問に答えると AGENTS.md・README.md 等が自動生成されます。")
    print("（Ctrl+C でいつでも中断できます）")
    print()

    # --- Python バージョン確認 ---
    check_python_version()

    # --- プロジェクト種別を選択 ---
    preset = select_preset()
    preset_type = preset["type"]  # "python" | "latex" | "word" | "custom"

    # --- Python プロジェクトのみ uv チェック ---
    if preset_type in ("python", "custom"):
        print()
        print("─── uv チェック ───")
        check_and_setup_uv()

    # --- 基本情報 ---
    print()
    name = _prompt("プロジェクト名（英語推奨）", default="my-project")
    description = _prompt("プロジェクトの説明（1〜2行）", default="プロジェクトの説明。")

    # --- コマンド ---
    commands = (
        _ask_use_default("コマンド", preset["commands"])
        if preset["commands"]
        else _prompt_multiline(
            "コマンドを入力（例: uv run python src/main.py  # メイン実行）"
        )
    )

    # --- フォルダ構成 ---
    architecture = (
        _ask_use_default("フォルダ構成", preset["architecture"])
        if preset["architecture"]
        else _prompt_multiline("フォルダ構成を入力（例: - src/ - ソースコード）")
    )

    # --- 規約 ---
    if preset_type == "custom":
        print("\n規約の種別を選択してください：")
        print("  1. Python（型ヒント・docstring 等）")
        print("  2. LaTeX（セクション分割・BibTeX 等）")
        print("  3. Word（ファイル命名・スタイル統一 等）")
        print("  4. 手動入力")
        conv_choice = _prompt("番号を入力", default="1")
        conv_map = {
            "1": PYTHON_CONVENTIONS,
            "2": LATEX_CONVENTIONS,
            "3": WORD_CONVENTIONS,
        }
        conventions = (
            conv_map.get(conv_choice)
            or _prompt_multiline("規約を入力")
        )
        do_dont = _prompt_multiline("Do / Don't を入力")
    else:
        conventions = preset["conventions"]
        do_dont = preset["do_dont"]

    # --- 注意事項 ---
    watch_out_for = (
        _ask_use_default("注意事項", preset["watch_out_for"])
        if preset["watch_out_for"]
        else _prompt_multiline("注意事項を入力（ハマりポイント・落とし穴など）")
    )

    # --- 確認 ---
    print("\n" + "=" * 54)
    print("以下の内容でファイルを生成します：")
    print("=" * 54)
    print(f"  プロジェクト名  : {name}")
    print(f"  種別            : {preset['label']}")
    print(f"  説明            : {description}")
    print(f"  生成ファイル    : AGENTS.md / CLAUDE.md / GEMINI.md / README.md")
    if preset_type in ("python", "custom"):
        print(f"                    pyproject.toml")
    print("=" * 54)

    confirm = _prompt("\n続けますか？", default="y").lower()
    if confirm not in ("y", "yes", ""):
        print("中断しました。")
        sys.exit(0)

    print()

    # --- AGENTS.md ---
    agents_content = generate_agents_md(
        name, description, commands, architecture, conventions, do_dont, watch_out_for
    )
    (ROOT / "AGENTS.md").write_text(agents_content, encoding="utf-8")
    print("  ✓ AGENTS.md")

    # --- CLAUDE.md / GEMINI.md ---
    (ROOT / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    print("  ✓ CLAUDE.md")
    (ROOT / "GEMINI.md").write_text("@AGENTS.md\n", encoding="utf-8")
    print("  ✓ GEMINI.md")

    # --- README.md ---
    if preset_type == "latex":
        readme_content = generate_readme_latex(name, description)
    elif preset_type == "word":
        readme_content = generate_readme_word(name, description)
    else:
        readme_content = generate_readme_python(name, description)
    (ROOT / "README.md").write_text(readme_content, encoding="utf-8")
    print("  ✓ README.md")

    # --- pyproject.toml（Python のみ） ---
    if preset_type in ("python", "custom"):
        update_pyproject(name, description)
        print("  ✓ pyproject.toml")

    # --- LaTeX 固有処理 ---
    if preset_type == "latex":
        append_gitignore(LATEX_GITIGNORE_EXTRA)
        print("  ✓ .gitignore（LaTeX パターンを追記）")
        create_latex_skeleton()
        print("  ✓ LaTeX 骨格ファイルを作成（sections/ figures/ refs.bib .latexmkrc）")

    # --- Word 固有処理 ---
    if preset_type == "word":
        create_word_skeleton()
        print("  ✓ Word 骨格ディレクトリを作成（docs/ figures/ refs/）")

    # --- 完了メッセージ ---
    print()
    print("=" * 54)
    print("  完了しました！")
    print("=" * 54)
    if preset_type == "latex":
        print(_NEXT_STEPS_LATEX)
    elif preset_type == "word":
        print(_NEXT_STEPS_WORD)
    else:
        print(_NEXT_STEPS_PYTHON)
    print("=" * 54)
    print()


if __name__ == "__main__":
    main()
