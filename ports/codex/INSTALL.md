# Installing /book for OpenAI Codex CLI

Codex CLI reads the same open [Agent Skills](https://developers.openai.com/codex/skills)
format (SKILL.md + references + scripts) that Claude Code does. The only file that
differs is the orchestrator: Codex gets `ports/codex/SKILL.md`, which maps the
runtime specifics (subagents via `codex exec`, conversational gates, model flags).
Every reference file and the compile script are shared unchanged.

## Install (two commands)

```bash
# macOS / Linux
git clone https://github.com/luquiluke/claude-book-skill "$HOME/.codex/skills/book"
cp "$HOME/.codex/skills/book/ports/codex/SKILL.md" "$HOME/.codex/skills/book/SKILL.md"
```

```powershell
# Windows (PowerShell)
git clone https://github.com/luquiluke/claude-book-skill "$env:USERPROFILE\.codex\skills\book"
Copy-Item "$env:USERPROFILE\.codex\skills\book\ports\codex\SKILL.md" "$env:USERPROFILE\.codex\skills\book\SKILL.md" -Force
```

The copy overwrites the Claude Code orchestrator with the Codex one *in your local
install only*. To update later: `git checkout -- SKILL.md && git pull`, then repeat
the copy.

## Use

Open Codex and just talk — "I want to write a book about urban beekeeping", "here are
my old posts, learn my style", "write chapter 1" — or invoke explicitly with `$book`
or `/skills`. Requirements: Python 3 (compile step, stdlib only). Web search enabled
in Codex improves the Researcher; MCP servers for Google Drive/Notion enable direct
ingestion, with file-drop fallbacks otherwise.

## Other runtimes

Gemini CLI, GitHub Copilot (VS Code agent skills), Cursor, and several community
tools also read the SKILL.md format. The Codex orchestrator's runtime mapping section
is written generically enough to work in most of them — install the same way into the
tool's skills directory and replace the root SKILL.md with `ports/codex/SKILL.md`.
