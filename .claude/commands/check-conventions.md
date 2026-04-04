---
description: Check that changed files follow AGENTS.md conventions / 変更ファイルが AGENTS.md の Conventions に従っているかチェックする
---

## Convention Check / 規約チェック

### Changed files / 変更ファイルの確認
```
!`git diff --name-only HEAD 2>/dev/null || git status --short`
```

### Lint / リント実行
```
!`uv run ruff check src/ tests/ 2>&1`
```

### Type check / 型チェック実行
```
!`uv run mypy src/ 2>&1`
```

Review the results against the following criteria:
/ 上記の結果をもとに、以下の観点でチェックしてください：

1. **Type hints / 型ヒント**: Are argument and return types annotated?
2. **Docstrings / docstring**: Do public functions and classes have docstrings?
3. **Constants / 定数化**: Are magic numbers avoided?
4. **Path handling / パス操作**: Is `pathlib.Path` used instead of `os.path`?
5. **Error handling / エラーハンドリング**: Is bare `except Exception` avoided?
6. **Units / 単位明記**: Are numeric units noted in comments or variable names?

If issues are found, suggest corrections.
/ 問題があれば修正案を提示してください。
