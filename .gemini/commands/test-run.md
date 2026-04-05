---
description: Run tests and summarize results / テストを実行して結果をサマリーする
---

## Run Tests / テスト実行

```
!`uv run pytest tests/ -v --tb=short 2>&1`
```

Based on the output, provide a summary covering:
/ 実行結果をもとに以下をサマリーしてください：

1. **Total / 合計**: Count of PASSED / FAILED / ERROR
2. **Failures / 失敗・エラー** (if any): List each test name and cause
3. **All passed / すべて通過**: Report "All tests passed"
4. **Suggestions / 改善提案**: If failures exist, briefly suggest a fix approach
