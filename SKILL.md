---
name: book
description: >
  Non-fiction book-writing studio for any subject and any author. Six specialized agents —
  Librarian, Researcher, Writer, Editor, Reviewer, Compiler — take a book from idea to
  compiled .docx written in the author's own voice, replicated from their writing samples.
  Use whenever the user invokes /book or a /book subcommand, asks to start, plan, outline,
  write, edit, polish, review, import, or compile a book, manuscript, or chapter; wants
  their writing style analyzed, calibrated, or replicated; wants writing samples ingested
  from files, URLs, Google Drive, Notion, databases, or an X/Twitter archive; or refers to
  any project under the Books folder. Works in any language and regional variant,
  including Spanish (es-AR voseo rioplatense, neutral Latin American, peninsular).
  Trigger on natural phrasing like "let's work on my book," "write the next chapter,"
  "how's the book coming," "make it sound like me," "escribamos el próximo capítulo," or
  "turn my notes into a chapter." EXCEPTION: if a dedicated skill exists for the specific
  book being discussed (e.g., a per-book skill like rift), that skill wins — use it, not
  this one.
---

# /book — a book-writing studio in the author's voice

Writes non-fiction books as the author, not for them. The author's ingested writing
samples become a quantified style fingerprint; every agent downstream treats that
fingerprint as law. Works entirely through natural conversation — commands exist but are
never required.

Reference files (read only what the current action needs — they cost tokens):

| File | When to read |
|---|---|
| `references/project-template.md` | Creating a project, importing drafts, the setup interview |
| `references/agent-briefs.md` | Before spawning any agent (read that agent's section) |
| `references/style-analysis.md` | Style ingestion, calibration, profile updates |
| `references/ingestion.md` | Pulling writing samples or research from any source |
| `references/writing-rules.md` | Never read by the orchestrator — Writer/Editor/Reviewer read it themselves |
| `references/lang/<code>.md` | Language companions (es available) — Writer/Editor read them for non-English books |

---

## Session start

1. **Find the active book.** Read the registry at `<Books root>/registry.md`. The Books
   root defaults to `~/Documents/Books` (Windows: `%USERPROFILE%\Documents\Books`);
   if the user's memory, CLAUDE.md, or conversation names a different root, that wins.
   One book → assume it. Several → infer from the user's words, else ask which. No
   registry → offer `/book new` or `/book import`. (Create the root on first use.)
2. **Load context.** Read the project's `book.md` and skim `state.md` (chapter status
   table). Do not read the manuscript or style profile yet — agents read those.
3. **Cost note.** Once per session, before the first pipeline run, tell the user plainly:
   *"A full guided chapter runs 5–8 agents (research, draft, edit, up to 3 review cycles).
   On a $20/month plan that is a meaningful share of a session window. Say 'express' for
   fewer stops, or work one stage at a time."* Informational only — never block on it.

## Intent routing — natural language first

Users never need commands. Map plain requests to actions; when a request is ambiguous
between two actions, ask one short clarifying question instead of guessing.

| User says something like | Action |
|---|---|
| "I want to write a book about X" / "start a new book" | **New project** |
| "here's my writing" / "learn my style" / mentions samples, tweets, Drive, Notion | **Ingest + style** |
| "make it sound like me" / "that doesn't sound like me" | **Recalibrate** (Librarian update mode) |
| "plan the chapters" / "outline" | **Outline** |
| "write chapter N" / "next chapter" / "keep going" | **Write pipeline** on the next non-final chapter |
| "I already have drafts" / points at existing files | **Import** |
| "tighten/fix/polish chapter N" | **Polish** (Editor only) |
| "is chapter N any good?" / "check it" | **Review** (Reviewer only, notes back) |
| "put the book together" / "give me the Word file" | **Compile** |
| "where are we?" / "status" / "which books do I have?" | **Status / list** |

Command shortcuts (equivalent, for users who like them): `/book new · ingest · style ·
outline · write N · import · polish N · review N · compile · status · list`.

## Modes

- **Guided (default):** approval gates after Researcher and after Writer.
- **Express:** no mid-gates; the user reviews only the finished chapter.

The user can say "express" or "guided" at any point; remember the choice for the session.

---

## Spawning agents

All six agents run as **subagents** via the Agent tool — never inline. For each spawn:

1. Read the agent's section of `references/agent-briefs.md`.
2. Build the prompt: the brief's "Prompt inputs" list tells you exactly which file paths
   and prior outputs to include. Pass prior agent outputs **complete and verbatim** — the
   Writer needs the whole fact sheet, the Editor needs the whole draft. Never summarize a
   handoff.
3. **Models:** spawn Writer and Editor with `model: "opus"` (strongest prose). If the
   Agent call errors on the model override, retry once without it. All other agents
   inherit the session model.

## The chapter pipeline

```
Researcher → [gate] → Writer → [gate] → Editor → Reviewer ⇄ Editor (max 3 cycles) → done
```

1. **Researcher** builds `research/chapter-NN-facts.md`: user-provided sources first, web
   only to fill gaps; every claim carries a source or a ⚠️ uncertainty flag.
2. **Gate 1 (guided only).** Show the fact sheet. AskUserQuestion: anything wrong,
   missing, or to protect? Apply corrections to the fact sheet before continuing.
3. **Writer** drafts the full chapter in the author's voice (style profile + fact sheet +
   state.md + chapter template from book.md). Output ends with a **State Updates** section.
4. **Gate 2 (guided only).** Show the draft. Directionally right? Apply requested changes.
5. **Editor** line-edits against `writing-rules.md` (with the profile's whitelist
   overrides) and the fingerprint. Runs the pre-flight checklist.
6. **Reviewer** reads as the target reader (persona in book.md). Verdict `CLEAR`, or a
   list of flagged passages. If flagged → Editor fixes **in-voice** → Reviewer rechecks.
   Maximum 3 cycles; orchestrator counts. Unresolved flags go into the final note — never
   silently dropped.
7. **Save and update:**
   - Back up first: any file about to be overwritten is copied to
     `versions/<filename>.<YYYYMMDD-HHMMSS>.md` before writing. No exceptions.
   - Write the chapter to `manuscript/chapter-NN-<slug>.md`.
   - Apply the Writer's State Updates to `state.md` (terminology, examples, facts,
     cross-references, promises to the reader) and update the chapter status table.
   - Update the registry row (status, last touched).
8. **Present** the finished chapter inline, then the Editor's open items and any
   unresolved Reviewer flags. Ask what's next.

**Voice doctrine (applies to every stage):** the fingerprint governs *how* things are
said and is replicated strictly, even when generic "good style" disagrees. Reviewer
clarity fixes change *what gets communicated*, and are always rewritten in the author's
voice — never in neutral "clean AI" prose.

## Other workflows

- **New project** — follow `references/project-template.md`: adaptive two-stage
  interview → scaffold the project folder → registry entry → then offer style ingestion
  as the natural next step. Default location: `<Books root>\<slug>\` (user may override).
- **Ingest / style** — spawn Librarian (analyze mode) per `references/style-analysis.md`
  and `references/ingestion.md`. Ends with the calibration test. No samples at all →
  Librarian runs the no-corpus interview fallback.
- **Recalibrate / learning** — after the user hand-edits a chapter or gives style
  feedback ("too stiff"), spawn Librarian (update mode) to fold the signal into
  `style-profile.md` with a dated changelog entry.
- **Outline** — orchestrator + user fill the chapter map in `book.md` (title, one-line
  promise, key points per chapter). Researcher may be spawned for a landscape scan if the
  user wants grounding.
- **Import** — per draft, ask: **Expand** (preserve the draft's structure and concepts;
  agents build around them — rift-style) or **Raw material** (mine content and style;
  restructure freely). Route `{curly brace}` inline comments per the agent briefs.
- **Polish N** — Editor only, then Reviewer loop as usual.
- **Review N** — Reviewer only; findings returned as notes, nothing rewritten.
- **Compile** — spawn Compiler. It assembles title page, TOC, chapters, and the back
  matter the user wants (glossary auto-built from state.md terminology; endnotes from the
  fact sheets; dedication / about-the-author prompted at compile time), then runs
  `scripts/compile_book.py` (clones styles from `sources/sample.docx` when present, else
  the built-in template). Output: `output/<Title>.docx`.
- **Status / list** — status: read book.md chapter table + manuscript folder, show a
  compact table (chapter, stage, words, last touched). List: show the registry.

---

## Non-negotiables

- **The author's voice is law.** Strict mimicry of the fingerprint; whitelist beats the
  banned list when the corpus provides the evidence.
- **No invented facts.** Writers use the fact sheet; anything unsourced is ⚠️-flagged, and
  flags survive into the final note. Agents never resolve a ⚠️ by guessing.
- **Never lose the user's words.** versions/ backup before every overwrite; imported
  drafts are copied in, originals untouched.
- **The book's language is the book's language — variant included.** book.md fixes both
  at creation (e.g. `es-AR · vos`); every agent reads and writes in it. A voseo book
  never drifts into tuteo; regional grammar is enforced as strictly as the voice.
- **One chapter at a time.** Never batch-run the pipeline across multiple chapters in one
  go unless the user explicitly asks.
