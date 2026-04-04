---
description: 変更ファイルが AGENTS.md の Conventions に従っているかチェックする
---

## 規約チェック

### 変更ファイルの確認
!`git diff --name-only HEAD 2>/dev/null || git status --short`

### リント実行
!`uv run ruff check src/ tests/ 2>&1`

### 型チェック実行
!`uv run mypy src/ 2>&1`

上記の結果をもとに、以下の観点でチェックしてください：

1. **型ヒント**: 引数・戻り値の型ヒントが付いているか
2. **docstring**: public な関数・クラスに docstring があるか
3. **定数化**: マジックナンバーが直接書かれていないか
4. **パス操作**: `os.path` ではなく `pathlib.Path` を使っているか
5. **エラーハンドリング**: 素の `except Exception` が使われていないか
6. **単位明記**: 数値の単位がコメントまたは変数名で明記されているか

問題があれば修正案を提示してください。
