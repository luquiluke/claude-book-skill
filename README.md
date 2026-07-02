# /book — a book-writing studio in your voice

A Claude Code skill that writes non-fiction books *as you*, not for you. Feed it anything you've ever written — a few tweets or three old manuscripts — and six specialized agents research, draft, edit, review, and compile chapters that match your sentence rhythm, your vocabulary, your quirks. Built for writers who aren't AI people.

[![Claude Code](https://img.shields.io/badge/Claude_Code-skill-D97706?logo=anthropic)](https://claude.com/claude-code)
[![Python](https://img.shields.io/badge/Python-stdlib_only-blue?logo=python)](https://www.python.org/)
[![Output](https://img.shields.io/badge/Output-.docx-2B579A?logo=microsoftword)](#compiling)
[![Español](https://img.shields.io/badge/Espa%C3%B1ol-es--AR_voseo-74ACDF)](#español-rioplatense-incluido)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> Ideas synthesized from [blader/humanizer](https://github.com/blader/humanizer) (AI-tell taxonomy), [ThomasHoussin/Claude-Book](https://github.com/ThomasHoussin/Claude-Book) (bible-style continuity, validation loops), and stylometry research — rebuilt as a single natural-language-first skill for non-fiction.

## What it does

1. **Interview** — "I want to write a book about X." A two-stage setup interview turns that into a premise, a concrete reader, a chapter map, and a chapter template built for *your* book — not a generic outline.
2. **Learn your voice** — drop writing samples anywhere (files, URLs, Google Drive, Notion, a database, your X/Twitter archive) and the Librarian builds a quantified style fingerprint: sentence-length distribution, punctuation habits, signature words, how you open and close. A calibration test ("which of these three sounds like you?") tunes it before a single chapter is written.
3. **Write chapter by chapter** — Researcher builds a sourced fact sheet → you approve → Writer drafts in your voice → you approve → Editor strips every AI tell → a simulated *target reader* flags anything confusing → Editor fixes it in-voice. Up to three review cycles, then it ships.
4. **Stay consistent** — a continuity file tracks terminology, recurring examples, established figures, and promises made to the reader, so chapter 12 never contradicts chapter 3.
5. **Compile** — one command produces a real book `.docx`: title page, table of contents, chapters, auto-built glossary, endnotes from the fact sheets. Clean built-in template, or formatting cloned from any `.docx` you provide.

## The agents

| Agent | Job |
|---|---|
| **Librarian** | Ingests your writing, builds and maintains the style fingerprint, learns from your edits |
| **Researcher** | Your sources first, web to fill gaps — every claim sourced or ⚠️-flagged, never guessed |
| **Writer** | Drafts the full chapter in your voice, against your chapter template |
| **Editor** | Line edit + anti-AI audit, calibrated to *your* fingerprint — not generic "clean" prose |
| **Reviewer** | Reads as your target reader; flags anything a real reader would stumble on |
| **Compiler** | Assembles the finished `.docx` with front and back matter |

## The anti-AI system

Banned-word lists alone produce generic "clean AI" prose. This skill layers three defenses, in priority order:

- **Your fingerprint is the positive target** — output converges on you, not on "good writing."
- **A five-family tell catalog is the negative filter** — content, language, style, communication, and filler/hedging patterns, audited on every chapter. Spanish books get their own catalog (including English-calque detection: *hacer sentido*, *tomar acción*…).
- **Strict-mimicry whitelist** — if *you* genuinely use a "banned" word (3+ times in your corpus), it's whitelisted with evidence. Your habits outrank the rules.

## Español rioplatense incluido

El skill escribe en cualquier idioma, y el español es ciudadano de primera: catálogo propio de muletillas de IA ("cabe destacar", "no solo… sino también", "en la era digital"), detección de calcos del inglés, y **soporte completo de voseo rioplatense** — conjugación (tenés, querés, hacé, andá), "con vos" jamás "contigo", ustedes siempre, cero peninsularismos. Un libro en voseo no se desliza al tuteo ni una sola vez: el Editor verifica cada verbo en segunda persona. Variantes soportadas: `es-AR` (voseo), `es-419` (tuteo neutro), `es-ES` (peninsular), trato de usted.

## Quick start

### Requirements

- [Claude Code](https://claude.com/claude-code) (any plan — see [session costs](#what-a-session-costs))
- Python 3.8+ (standard library only — compiling the `.docx` needs zero pip installs)

### Install

```bash
# macOS / Linux
git clone https://github.com/luquiluke/claude-book-skill "$HOME/.claude/skills/book"

# Windows (PowerShell)
git clone https://github.com/luquiluke/claude-book-skill "$env:USERPROFILE\.claude\skills\book"
```

Open Claude Code and just talk:

```
I want to write a book about urban beekeeping
here are my old blog posts — learn my style      (or point it at Drive/Notion/your X archive)
write chapter 1
```

## Talking to it

No commands required — "let's work on my book", "that doesn't sound like me", "give me the Word file" all route correctly. Shortcuts exist if you like them:

| Command | Does |
|---|---|
| `/book new` | Setup interview → project scaffold |
| `/book ingest` / `/book style` | Pull writing samples / build or recalibrate the fingerprint |
| `/book outline` | Fill the chapter map |
| `/book write N` | Full pipeline on chapter N |
| `/book import` | Bring in existing drafts (preserve their structure, or mine them as raw material) |
| `/book polish N` / `/book review N` | Editor-only pass / reader-check only |
| `/book compile` | Build the `.docx` |
| `/book status` / `/book list` | Chapter dashboard / all your books |

**Guided mode** (default) pauses for your approval after research and after the draft. Say **"express"** to run the whole pipeline and review only the finished chapter.

## What a session costs

Honest numbers: a full guided chapter runs 5–8 subagents (research, draft, edit, up to 3 reader-review cycles). On a $20/month plan that's a meaningful share of a session window — the skill tells you this up front, once, and never blocks. Express mode and stage-at-a-time work cost less. Prose agents (Writer, Editor) request the strongest available model and fall back gracefully on any plan.

## Project layout

Each book is a plain folder you own — everything is markdown you can read and edit:

```
Books/<your-book>/
├── book.md              premise, reader, chapter template, chapter map
├── style-profile.md     your voice fingerprint (with a changelog of what it learned)
├── state.md             continuity: terminology, examples, facts, promises to the reader
├── sources/style/       drop writing samples here
├── sources/research/    drop reference material here
├── sources/sample.docx  optional: formatting to clone at compile time
├── research/            per-chapter fact sheets with sources
├── manuscript/          the chapters
├── versions/            timestamped backup of every file before every overwrite
└── output/              the compiled .docx
```

## Configuration

- **Books root** — defaults to `~/Documents/Books`; mention a different folder in conversation (or your CLAUDE.md) and the skill uses it.
- **Formatting** — drop any `sample.docx` into `sources/` and the Compiler clones its fonts, styles, and page setup; otherwise you get the built-in book template (Georgia, real heading styles, page numbers, TOC).
- **Back matter** — glossary is auto-built from the terminology the book actually defined; endnotes from the fact sheets; dedication and about-the-author prompted at compile time.

## Docs

| File | What's in it |
|---|---|
| [SKILL.md](SKILL.md) | The orchestrator: pipeline, gates, modes, non-negotiables |
| [references/agent-briefs.md](references/agent-briefs.md) | The six agents' full briefs |
| [references/writing-rules.md](references/writing-rules.md) | The anti-AI catalog and pre-flight checklist |
| [references/style-analysis.md](references/style-analysis.md) | How the voice fingerprint is built, calibrated, and updated |
| [references/ingestion.md](references/ingestion.md) | Source playbooks: files, URLs, Drive, Notion, databases, X archive |
| [references/lang/es.md](references/lang/es.md) | Spanish AI-tells, calque detection, voseo rioplatense grammar |
| [references/project-template.md](references/project-template.md) | Project scaffold and setup interview |

## License

[MIT](LICENSE) — use it, fork it, write your book.
