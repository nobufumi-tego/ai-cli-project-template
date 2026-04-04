# AGENTS.md 生成サンプル

`scripts/init-project.py` を実行すると、選択したプロジェクト種別に応じて
`AGENTS.md` が自動生成されます。このファイルはその完成形サンプルです。

---

## サンプル：Python ML / AI 研究（プリセット 1）

実行時の対話例：

```
プロジェクト種別を選択してください：
  1. Python ML / AI 研究
  ...
番号を入力 [1]: 1

プロジェクト名 [my-project]: tug-analysis
プロジェクトの概要を入力してください: MediaPipe 姿勢推定を用いた TUG 歩行解析システム
```

生成される `AGENTS.md`：

---

```markdown
# tug-analysis

MediaPipe 姿勢推定を用いた TUG 歩行解析システム

## Commands
uv run python src/main.py              # メイン処理実行
uv run pytest tests/ -v                # テスト実行
uv run ruff check src/ tests/          # リント
uv run mypy src/                       # 型チェック
jupyter lab notebooks/                 # Notebook起動

## Architecture
- src/data/       - データ読み込み・前処理モジュール
- src/models/     - モデル定義・学習ロジック
- src/evaluation/ - 評価・メトリクス算出
- src/utils/      - 共通ユーティリティ
- data/raw/       - 元データ（読み取り専用・git管理外）
- data/processed/ - 加工済みデータ
- notebooks/      - 実験・分析用Jupyter Notebook
- tests/          - テストコード
- configs/        - 設定ファイル（YAML）

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
- GPU/CPU環境で乱数シードを固定しても数値結果が微妙に異なる場合がある
- データセットのファイルパスは絶対パスではなく pathlib.Path で相対記述する
- モデルチェックポイントファイル（*.pt, *.pkl）は data/ 以下に置くこと
```

---

## サンプル：LaTeX 論文執筆（プリセット 6）

```
番号を入力 [1]: 6

プロジェクト名 [my-project]: my-thesis
プロジェクトの概要を入力してください: 深層学習を用いた歩行解析に関する修士論文
```

生成される `AGENTS.md`：

---

```markdown
# my-thesis

深層学習を用いた歩行解析に関する修士論文

## Commands
latexmk -pdf main.tex              # PDF コンパイル
latexmk -c                         # 中間ファイルをクリーン
latexmk -pvc main.tex              # 自動コンパイル（監視モード）
# 日本語論文の場合:
latexmk -pdfdvi main.tex           # uplatex + dvipdfmx でコンパイル

## Architecture
- main.tex        - メイン論文ファイル（\input でセクションを読み込む）
- sections/       - セクション別 .tex ファイル
  - introduction.tex
  - method.tex
  - results.tex
  - discussion.tex
  - conclusion.tex
- figures/        - 図・グラフ（PDF / PNG 推奨）
- refs.bib        - 参考文献（BibTeX 形式）
- .latexmkrc      - latexmk 設定ファイル

## Conventions
- セクション別に .tex ファイルを分割し、main.tex で \input{sections/...} する
- 図のパスは相対パスで記述する（例: \includegraphics{figures/fig1.pdf}）
- 参考文献は refs.bib にまとめ、\citep / \citet コマンドで引用する
- 変更理由をコメントで残す（例: % [2024-01-15] reviewer の指摘で修正）

## Do / Don't
DO:
- 変更前に git commit して履歴を残す
- 図・表を追加したら必ずコンパイルして見た目を確認する

DON'T:
- コンパイル生成ファイル（*.aux, *.log 等）をgit管理しない（.gitignore 設定済み）
- main.tex に全文を書かない（sections/ に分割する）

## Watch out for
- 日本語フォントは環境依存。TeX Live の場合 tlmgr で必要フォントをインストールする
- 図のファイル名にスペースや日本語を使わない
- BibTeX の cite key は FirstauthorYYYYkeyword 形式で統一すると管理しやすい
```

---

## 生成後にやること

生成された `AGENTS.md` は**育てていくもの**です。

```
# Claude Code 内でこう依頼する
今日の作業でわかったことを AGENTS.md の Watch out for に追記してください。
「DataLoader はファイルが存在しない場合 FileNotFoundError を raise する設計にする」
```

| タイミング | 追記場所 |
|---|---|
| 同じ説明を2回以上した | Conventions |
| AI が間違いを繰り返した | Don't |
| 新コマンドが増えた | Commands |
| ハマったポイントがあった | Watch out for |
