# Pythonコード規約

AGENTS.md の Conventions セクションを詳細化したルール集。

## 型ヒント
- すべての関数・メソッドに引数と戻り値の型ヒントを付ける
- `from __future__ import annotations` を各ファイル先頭に記述する
- `Optional[X]` ではなく `X | None` を使う（Python 3.10+）
- `List`, `Dict`, `Tuple` ではなく `list`, `dict`, `tuple` を使う

## Docstring
- すべての public 関数・クラス・モジュールに docstring を書く
- 形式: Google スタイル
  ```python
  def func(x: float) -> float:
      """1行で要約する。

      Args:
          x: 入力値（単位: 秒）

      Returns:
          処理結果（単位: ミリ秒）

      Raises:
          ValueError: x が負の値の場合
      """
  ```

## 定数化
- ファイル先頭に大文字スネークケースで定義する
- 例: `MAX_EPOCHS = 100`、`LEARNING_RATE = 1e-3`

## パス操作
- `os.path` ではなく `pathlib.Path` を使う
- 絶対パスをハードコードしない

## エラーハンドリング
- 具体的な例外クラスを使う（`Exception` の素の `except` は禁止）
- エラーメッセージに何が起きたかを明記する
