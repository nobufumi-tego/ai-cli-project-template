"""プロジェクト初期化スクリプト。

対話形式でプロジェクト情報を収集し、AGENTS.md・CLAUDE.md・GEMINI.md・
README.md・pyproject.toml を自動生成する。

Usage:
    python scripts/init-project.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# プロジェクトルートを基準にパスを解決する
ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# プリセット定義
# ---------------------------------------------------------------------------

PRESETS: dict[str, dict[str, str]] = {
    "1": {
        "label": "Python ML / AI 研究",
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
        "watch_out_for": """\
- GPU/CPU環境で乱数シードを固定しても数値結果が微妙に異なる場合がある
- データセットのファイルパスは絶対パスではなく pathlib.Path で相対記述する
- モデルチェックポイントファイル（*.pt, *.pkl）は data/ 以下に置くこと""",
    },
    "2": {
        "label": "データ分析",
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
        "watch_out_for": """\
- データセットのファイルパスは絶対パスではなく pathlib.Path で相対記述する
- Notebook の実行順序に依存したコードを書かない（モジュールに切り出す）
- 可視化ライブラリのバージョンで出力が変わる場合がある""",
    },
    "3": {
        "label": "Web API (FastAPI)",
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
        "watch_out_for": """\
- 環境変数・秘密情報は .env に書き .gitignore 済みであることを確認する
- 依存性注入（Depends）を積極的に使い、テスト可能な設計にする
- 非同期処理（async/await）の混在に注意する""",
    },
    "4": {
        "label": "CLIツール",
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
        "watch_out_for": """\
- 終了コードを適切に設定する（正常: 0、エラー: 非0）
- stdin / stdout / stderr の使い分けを明確にする
- パスは pathlib.Path で扱い、OSの違いを吸収する""",
    },
    "5": {
        "label": "Pythonライブラリ",
        "commands": """\
uv run pytest tests/ -v                # テスト実行
uv run ruff check src/ tests/          # リント
uv run mypy src/                       # 型チェック
uv build                               # パッケージビルド""",
        "architecture": """\
- src/<package>/ - ライブラリ本体
- tests/         - テストコード
- docs/          - ドキュメント（Sphinx等）""",
        "watch_out_for": """\
- Python バージョン互換性の範囲を pyproject.toml で明示する
- 外部依存は必要最小限にする
- パブリック API（__all__）を明示的に定義する""",
    },
    "6": {
        "label": "カスタム（全項目を手動入力）",
        "commands": "",
        "architecture": "",
        "watch_out_for": "",
    },
}


# ---------------------------------------------------------------------------
# ヘルパー関数
# ---------------------------------------------------------------------------


def prompt(message: str, default: str = "") -> str:
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


def prompt_multiline(message: str) -> str:
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


def select_preset() -> dict[str, str]:
    """プロジェクト種別を選択させる。

    Returns:
        選択されたプリセット辞書
    """
    print("\n" + "=" * 50)
    print("プロジェクト種別を選択してください：")
    print("=" * 50)
    for key, preset in PRESETS.items():
        print(f"  {key}. {preset['label']}")
    print("=" * 50)

    while True:
        choice = prompt("番号を入力", default="1")
        if choice in PRESETS:
            selected = PRESETS[choice]
            print(f"\n→ 「{selected['label']}」を選択しました。\n")
            return selected
        print(f"  1〜{len(PRESETS)} の番号を入力してください。")


# ---------------------------------------------------------------------------
# ファイル生成関数
# ---------------------------------------------------------------------------


def generate_agents_md(
    name: str,
    description: str,
    commands: str,
    architecture: str,
    watch_out_for: str,
) -> str:
    """AGENTS.md の内容を生成する。

    Args:
        name: プロジェクト名
        description: プロジェクト説明
        commands: コマンド一覧（複数行）
        architecture: フォルダ構成（複数行）
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
- 型ヒント必須（Python 3.10+）
- すべての関数・クラスにdocstringを書く（Google スタイル）
- 数値の単位はコメントまたは変数名で明記（例: `duration_sec`, `size_mb`）
- マジックナンバーはすべて定数化（各モジュール先頭または `configs/` に定義）
- エラーハンドリングを省略しない
- `os.path` ではなく `pathlib.Path` を使う
- 絶対パスをハードコードしない

## Do / Don't
DO:
- 変更前に `uv run pytest` を実行して既存テストが通ることを確認する
- 新しい機能を追加したらテストも同時に追加する
- data/raw/ のファイルは読み取りのみ。加工結果は data/processed/ へ

DON'T:
- 大容量ファイル（動画・モデルチェックポイント等）をgit管理しない（.gitignore 設定済み）
- GPU/CPU環境依存のハードコードをしない
- data/raw/ のファイルを直接編集しない

## Watch out for
{watch_out_for}
"""


def generate_readme(name: str, description: str) -> str:
    """README.md のプロジェクト固有部分を生成する。

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

```
.
├── AGENTS.md        # AI CLI 共通指示書
├── src/             # ソースコード
├── tests/           # テストコード
├── data/
│   ├── raw/         # 元データ（読み取り専用・git管理外）
│   └── processed/   # 加工済みデータ
└── notebooks/       # Jupyter Notebook
```
"""


def update_pyproject(name: str, description: str) -> None:
    """pyproject.toml のプロジェクト名と説明を更新する。

    Args:
        name: プロジェクト名（ハイフン区切りに正規化）
        description: プロジェクト説明
    """
    path = ROOT / "pyproject.toml"
    if not path.exists():
        return

    slug = name.lower().replace(" ", "-").replace("_", "-")
    content = path.read_text(encoding="utf-8")

    import re

    content = re.sub(r'^name\s*=\s*".+"', f'name = "{slug}"', content, flags=re.MULTILINE)
    content = re.sub(
        r'^description\s*=\s*".+"',
        f'description = "{description}"',
        content,
        flags=re.MULTILINE,
    )
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------


def main() -> None:
    """対話形式でプロジェクト情報を収集し、各ファイルを生成する。"""
    print("\n" + "=" * 50)
    print("  AI CLI プロジェクト初期化スクリプト")
    print("=" * 50)
    print("質問に答えると AGENTS.md・README.md 等が自動生成されます。")
    print("（Ctrl+C でいつでも中断できます）\n")

    # --- プロジェクト種別を選択 ---
    preset = select_preset()

    # --- 基本情報 ---
    name = prompt("プロジェクト名（英語推奨）", default="my-project")
    description = prompt("プロジェクトの説明（1〜2行）", default="Python プロジェクト。")

    # --- コマンド ---
    if preset["commands"]:
        print(f"\nデフォルトのコマンド（変更する場合は 'n'、そのまま使う場合はEnter）:")
        print(preset["commands"])
        use_default = prompt("このまま使いますか？", default="y").lower()
        commands = preset["commands"] if use_default != "n" else prompt_multiline("コマンドを入力")
    else:
        commands = prompt_multiline("コマンドを入力（例: uv run python src/main.py  # メイン実行）")

    # --- フォルダ構成 ---
    if preset["architecture"]:
        print(f"\nデフォルトのフォルダ構成:")
        print(preset["architecture"])
        use_default = prompt("このまま使いますか？", default="y").lower()
        architecture = (
            preset["architecture"] if use_default != "n" else prompt_multiline("フォルダ構成を入力")
        )
    else:
        architecture = prompt_multiline("フォルダ構成を入力（例: - src/ - ソースコード）")

    # --- 注意事項 ---
    if preset["watch_out_for"]:
        print(f"\nデフォルトの注意事項:")
        print(preset["watch_out_for"])
        use_default = prompt("このまま使いますか？", default="y").lower()
        watch_out_for = (
            preset["watch_out_for"]
            if use_default != "n"
            else prompt_multiline("注意事項を入力")
        )
    else:
        watch_out_for = prompt_multiline("注意事項を入力（ハマりポイント・落とし穴など）")

    # --- 確認 ---
    print("\n" + "=" * 50)
    print("以下の内容でファイルを生成します：")
    print("=" * 50)
    print(f"  プロジェクト名  : {name}")
    print(f"  説明            : {description}")
    print(f"  生成ファイル    : AGENTS.md / CLAUDE.md / GEMINI.md / README.md / pyproject.toml")
    print("=" * 50)

    confirm = prompt("\n続けますか？", default="y").lower()
    if confirm not in ("y", "yes", ""):
        print("中断しました。")
        sys.exit(0)

    # --- ファイル生成 ---
    agents_content = generate_agents_md(name, description, commands, architecture, watch_out_for)
    (ROOT / "AGENTS.md").write_text(agents_content, encoding="utf-8")
    print("  ✓ AGENTS.md を生成しました")

    (ROOT / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    print("  ✓ CLAUDE.md を生成しました")

    (ROOT / "GEMINI.md").write_text("@AGENTS.md\n", encoding="utf-8")
    print("  ✓ GEMINI.md を生成しました")

    readme_content = generate_readme(name, description)
    (ROOT / "README.md").write_text(readme_content, encoding="utf-8")
    print("  ✓ README.md を生成しました")

    update_pyproject(name, description)
    print("  ✓ pyproject.toml を更新しました")

    print("\n" + "=" * 50)
    print("  完了しました！")
    print("=" * 50)
    print("次のステップ：")
    print("  1. uv sync              # 依存パッケージをインストール")
    print("  2. uv run pytest tests/ # テスト実行で動作確認")
    print("  3. AGENTS.md を育てる   # プロジェクト固有の情報を追記していく")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
