# サポート / Support

## まず試すこと / Try this first

### Step 1：環境診断を実行してコピーする / Run the diagnostic and copy the output

```bash
python  scripts/check-setup.py   # Windows
python3 scripts/check-setup.py --lang en   # macOS / Linux (English)
```

出力内容をそのままコピーしておくと、次のステップが格段に速くなります。
/ Copy the full output — it speeds up everything that follows.

---

### Step 2：生成 AI に聞く / Ask an AI chatbot

Claude・Gemini・ChatGPT はセットアップエラーの解決が得意です。
以下のプロンプトに情報を埋めて貼り付けてください。

| AI | URL |
|---|---|
| Claude | https://claude.ai |
| Gemini | https://gemini.google.com |
| ChatGPT | https://chatgpt.com |

**プロンプトテンプレート / Prompt template:**

```
開発環境のセットアップ中にエラーが発生しました。解決方法を教えてください。
I'm getting an error during development environment setup. Please help me fix it.

[OS] Windows 11 / macOS / Linux

[実行したコマンド / Command I ran]
（ここに貼り付け / paste here）

[エラーメッセージ / Error message]
（ここに貼り付け / paste here）

[check-setup.py の出力 / check-setup.py output]
（ここに貼り付け / paste here）
```

---

---

## 質問・相談 / Questions & Discussion

**GitHub Discussions**（推奨 / recommended）
→ https://github.com/nobufumi-tego/ai-cli-project-template/discussions

- セットアップの質問 / Setup questions
- 使い方の相談 / Usage questions
- 改善アイデアの共有 / Sharing ideas

---

## 不具合報告 / Bug Reports

スクリプトの動作がおかしい場合は Issues へ。
/ If a script behaves unexpectedly, open an Issue.

→ https://github.com/nobufumi-tego/ai-cli-project-template/issues/new/choose

Issue を開く際は必ず以下を含めてください：
/ Please always include:

1. OS（Windows 11 / macOS / Linux）
2. `check-setup.py` の出力全文 / Full output of `check-setup.py`
3. エラーメッセージ全文 / Full error message

---

## インストールを元に戻したい場合 / Want to undo the installation?

→ [docs/recovery.md](docs/recovery.md) を参照してください。
/ See [docs/recovery.md](docs/recovery.md).

---

## セキュリティの問題 / Security Issues

脆弱性を発見した場合は Issues に公開投稿せず、GitHub の
[Private vulnerability reporting](https://github.com/nobufumi-tego/ai-cli-project-template/security/advisories/new)
を使って報告してください。

/ If you discover a vulnerability, please do **not** post it publicly in Issues.
Use GitHub's [Private vulnerability reporting](https://github.com/nobufumi-tego/ai-cli-project-template/security/advisories/new) instead.
