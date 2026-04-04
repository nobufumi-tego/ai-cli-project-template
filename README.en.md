# ai-cli-project-template

🇯🇵 [日本語版 README はこちら](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/powered%20by-uv-DE5FE9.svg)](https://github.com/astral-sh/uv)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code/overview)
[![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-compatible-4285F4.svg)](https://github.com/google-gemini/gemini-cli)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-74aa9c.svg)](https://github.com/openai/codex)
[![EN / JA](https://img.shields.io/badge/lang-EN%20%2F%20JA-orange.svg)](#)

A universal **Python / LaTeX / Word** project template compatible with **Claude Code**, **Gemini CLI**, and **Codex CLI**.
Run `scripts/init-project.py` interactively to auto-generate `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and more —
tailored to your project type. Includes a verified uv installer and a zero-dependency environment diagnostic. EN/JA bilingual.

**Supported OS**: Windows 11 / macOS / Linux

---

### Who is this for?

| Audience | Go to |
|---|---|
| Comfortable with terminal basics (`cd`, running commands) | Read this page |
| New to the command line | [Beginner Setup Guide (EN)](docs/beginner-guide.en.md) |

> **For complete beginners:**
> Setup requires installing multiple tools.
> We recommend having an experienced person nearby or following along via screen share for your first time.
> Run [`scripts/check-setup.py`](#environment-diagnostic-script) first — it auto-detects what's missing.

---

## Supported AI CLIs

| AI CLI | Provider | Config files | Use case |
|---|---|---|---|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) | Anthropic | `CLAUDE.md` `.claude/` | Code generation, refactoring, testing |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google | `GEMINI.md` `.gemini/` | Code generation, documentation |
| [Codex CLI](https://github.com/openai/codex) | OpenAI | `AGENTS.md` `.codex/` | Code generation, automation |

All three tools share **`AGENTS.md` as a common instruction file**.
`CLAUDE.md` and `GEMINI.md` contain only `@AGENTS.md` — all content is centralized in one place.

```
Update AGENTS.md once → changes apply to all 3 tools instantly
```

---

## Quick Start

```bash
# 1. Install Git & uv (see uv_setup/ for verified installers)
./uv_setup/install.sh        # macOS / Linux
.\uv_setup\install.bat       # Windows 11

# 2. Clone
git clone https://github.com/<your-name>/<your-repo>.git
cd <your-repo>

# 3. Diagnose environment (auto-detects what's missing)
python  scripts/check-setup.py --lang en   # Windows
python3 scripts/check-setup.py --lang en   # macOS / Linux

# 4. Initialize project (interactive)
uv run python scripts/init-project.py
```

## Environment Diagnostic Script

`scripts/check-setup.py` checks Git, uv, Python, VS Code, and AI CLIs in one run,
and shows OS-specific install instructions for anything missing.
**Runs on Python standard library only — no uv or external packages needed.**

```
======================================================
  Setup Check Script
  OS: Linux / Python 3.12.13
======================================================

[Required]
  ✓  Git: git version 2.39.5
  ✓  uv: uv 0.11.2
  ✓  Python 3.12.13  (recommended version)
[Recommended]
  ✓  VS Code: 1.114.0  (recommended editor)
[AI CLI (optional)]
  ✓  Node.js: v24.0.0  (required for AI CLIs)
  ✓  Claude Code: 2.1.92  (AI CLI)
  !  Gemini CLI not found  (optional)
       Install: npm install -g @google/gemini-cli
  ...
======================================================
  ✓ All required tools are installed.
  Next step:
    uv run python scripts/init-project.py
======================================================
```

---

## Who should use this?

| Situation | How this template helps |
|---|---|
| Want to start using Claude Code / Gemini CLI / Codex CLI but don't know how to configure them | Generates shared AGENTS.md config for all 3 tools at once |
| Tired of writing AGENTS.md and CLAUDE.md from scratch every project | Just pick a preset — files are auto-generated |
| Setting up a Python ML / AI research project structure | uv + ruff + mypy + pytest, ready to go |
| Want to use AI CLIs for LaTeX paper writing | LaTeX preset generates a paper-oriented AGENTS.md |
| Need everyone on the team to reproduce the same environment | uv_setup/ gives anyone the same env, from zero |
| Starting from a machine with no Python installed | uv installs Python itself — no prior setup needed |
| Command-line beginner struggling with environment setup | check-setup.py diagnoses what's missing in one run |

---

## Supported Project Types

| No. | Type | Required tools |
|---|---|---|
| 1 | Python ML / AI Research | uv |
| 2 | Data Analysis | uv |
| 3 | Web API (FastAPI) | uv |
| 4 | CLI Tool | uv |
| 5 | Python Library | uv |
| 6 | LaTeX Paper | TeX Live / MiKTeX |
| 7 | Word Paper | Word / LibreOffice |
| 8 | Custom | any |

See [docs/example-agents.md](docs/example-agents.md) for a sample of the generated `AGENTS.md`.

---

## Generated Files

| File | Python | LaTeX | Word |
|---|---|---|---|
| `AGENTS.md` | ✓ | ✓ | ✓ |
| `CLAUDE.md` | ✓ | ✓ | ✓ |
| `GEMINI.md` | ✓ | ✓ | ✓ |
| `README.md` | ✓ | ✓ | ✓ |
| `pyproject.toml` | ✓ | — | — |
| `.gitignore` (LaTeX additions) | — | ✓ | — |
| `sections/` `figures/` `refs.bib` `.latexmkrc` | — | ✓ | — |
| `docs/` `figures/` `refs/` | — | — | ✓ |

---

## Repository Structure

```
.
├── AGENTS.md                     # Common AI CLI instruction file
├── CLAUDE.md / GEMINI.md         # Per-CLI files (one-line @AGENTS.md import)
├── uv_setup/                     # Verified uv + Python installers
│   ├── install.sh / install.bat  #   OS-specific installers
│   └── README.md
├── scripts/
│   ├── init-project.py           # Interactive project initializer
│   └── check-setup.py            # Environment diagnostic (stdlib only)
├── .claude/
│   ├── settings.json             # Hooks and permission settings
│   ├── commands/
│   │   ├── test-run.md           # /project:test-run
│   │   └── check-conventions.md  # /project:check-conventions
│   ├── rules/python-conventions.md
│   └── skills/ml-research/SKILL.md
├── .gemini/commands/
├── .codex/
│   └── config.toml               # Codex CLI config (model, sandbox, MCP)
├── src/ tests/ notebooks/ data/ configs/
├── docs/
│   ├── beginner-guide.md         # Beginner setup guide (Japanese)
│   ├── beginner-guide.en.md      # Beginner setup guide (English)
│   └── example-agents.md         # Sample generated AGENTS.md
└── pyproject.toml
```

---

## Installing AI CLIs (optional)

AI CLIs are optional — you can develop fully without them.

```bash
# Node.js required first (winget install OpenJS.NodeJS.LTS, brew install node, etc.)
npm install -g @anthropic-ai/claude-code   # Claude Code
npm install -g @google/gemini-cli          # Gemini CLI
npm install -g @openai/codex               # Codex CLI
```

First-time auth: run `claude` (Anthropic account), `gemini` (Google account),
or set `OPENAI_API_KEY` environment variable for Codex.

---

## Development with Claude Code

```bash
cd your-project && claude
```

`AGENTS.md` is auto-loaded, giving Claude Code full context of your project's
conventions and structure from the start.

```
# Implementation request
Implement a DataLoader class in src/data/loader.py with type hints and docstrings.

# Bug fix
uv run pytest returns the following error: [paste error]. Find and fix the cause.

# Custom commands
/project:test-run           # Run tests → summarize results
/project:check-conventions  # Check code against AGENTS.md conventions
```

---

## Support & Troubleshooting

| Situation | Where to go |
|---|---|
| Stuck or got an error during setup | [GitHub Discussions](https://github.com/nobufumi-tego/ai-cli-project-template/discussions) or [Issues](https://github.com/nobufumi-tego/ai-cli-project-template/issues/new/choose) |
| Want to undo the installation | [docs/recovery.md](docs/recovery.md) |
| Full support information | [SUPPORT.md](SUPPORT.md) |

---

## Security

`.env` / `*.key` / `*.pem` / `credentials.json` / `data/raw/` / `settings.local.json` /
large files (`*.pt` `*.pkl` `*.mp4`) are all excluded via `.gitignore`.

---

## License

[MIT License](LICENSE) © 2026 nobufumi yoshida

The scripts and configuration files in this repository are licensed under the MIT License.
Files generated by `scripts/init-project.py` (AGENTS.md, README.md, etc.) belong entirely to the user and are not subject to this license.
