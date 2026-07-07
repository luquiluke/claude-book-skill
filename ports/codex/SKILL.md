---
name: book
description: >
  Non-fiction book-writing studio for any subject and any author. Six specialized
  agents — Librarian, Researcher, Writer, Editor, Reviewer, Compiler — take a book from
  idea to compiled .docx written in the author's own voice, replicated from their
  writing samples. Use whenever the user invokes book or a book subcommand; asks to
  start, plan, outline, write, edit, polish, review, import, or compile a book,
  manuscript, or chapter; wants their writing style analyzed, calibrated, or
  replicated; wants writing samples ingested from files, URLs, Google Drive, Notion,
  databases, or an X/Twitter archive; or refers to any project under the Books folder.
  Works in any language and regional variant, including Spanish (es-AR voseo
  rioplatense, neutral Latin American, peninsular). Trigger on natural phrasing like
  "let's work on my book," "write the next chapter," "how's the book coming," "make it
  sound like me," or "escribamos el próximo capítulo." EXCEPTION: if a dedicated skill
  exists for the specific book being discussed, that skill wins.
---

# /book — Codex CLI runtime

This is the Codex-adapted orchestrator. The methodology lives in the shared reference
files in this same skill folder — they are runtime-agnostic and you follow them
exactly as written:

| File | Read when |
|---|---|
| `references/project-template.md` | Creating or importing a project |
| `references/style-analysis.md` | Any style/ingestion work (Librarian methodology) |
| `references/ingestion.md` | Pulling writing samples or research from any source |
| `references/agent-briefs.md` | Before running any agent role |
| `references/writing-rules.md` | Never by you — Writer/Editor/Reviewer read it |
| `references/lang/<code>.md` | Language companions (es available) for non-English books |

Where a reference file mentions tools from other runtimes (an "Agent tool",
"AskUserQuestion", "WebFetch", model names like "opus"), map them as follows —
everything else applies verbatim.

## Runtime mapping

- **Subagents → `codex exec` children.** Each pipeline agent runs as an isolated
  non-interactive child so roles never blur:

  ```
  codex exec -C "<project dir>" --sandbox workspace-write \
    "<role prompt: identity + files to read + task + output file>"
  ```

  Handoff is through files: children write their full output to
  `<project>/.pipeline/<stage>.md` (facts.md, draft.md, edited.md, review-N.md) and
  the next child reads its predecessor's file. Never summarize between stages. Create
  `.pipeline/` per chapter; it is scratch — `versions/` is the real safety net.
  **Fallback:** if `codex exec` fails on this machine (sandbox policy, nesting
  restrictions), run the roles sequentially yourself in this session, one at a time,
  reading each brief fresh before playing its role and never mixing two roles in one
  pass. Say which mode you used.
- **Quality models.** Prose is the product: run Writer and Editor children on the
  strongest model configured on this machine (`-m <model>` or a Codex profile). The
  other agents use the default. If a model flag errors, drop it.
- **Approval gates → plain questions.** Where the flow says gate, stop and ask the
  user in the conversation, then wait. Do not proceed on silence.
- **Web research.** Use Codex's web search if enabled; otherwise fetch with `curl`
  in-sandbox, or mark the item ⚠️ for the user instead of guessing.
- **Connected sources.** Google Drive/Notion/databases arrive via MCP servers in the
  user's Codex config; if absent, use the file-drop fallbacks in ingestion.md.

## Session start

1. **Find the active book.** Read `<Books root>/registry.md`. Books root defaults to
   `~/Documents/Books` (Windows: `%USERPROFILE%\Documents\Books`); a root named in
   AGENTS.md or by the user wins. One book → assume it; several → infer or ask; none →
   offer to start or import one. Create the root on first use.
2. **Load the book.** Read the project's `book.md` and skim `state.md`. Do not read
   the manuscript unless the task needs it.
3. **Cost note (once per session):** a full guided chapter runs 5–8 agent children;
   say so in one line before the first pipeline run. Never block on it.

## Natural language first

No syntax required — route intent:

| The user says… | You do |
|---|---|
| "I want to write a book about X" | Setup interview → scaffold (project-template.md) |
| "here's my writing / learn my style" | Ingest → Librarian analyze → calibration test |
| "write (the next) chapter (N)" | Full chapter pipeline below |
| "that doesn't sound like me" | Librarian update mode → profile changelog |
| "I already have drafts" | Import flow — ask Expand vs Raw material per draft |
| "tighten/polish chapter N" | Editor-only pass, then Reviewer loop |
| "give me the Word file / compile" | Compiler agent |
| "how's the book going / status" | Chapter map status table from book.md |

Commands work as shortcuts too: `book new · ingest · style · outline · write N ·
import · polish N · review N · compile · status · list`.

## The chapter pipeline

```
Researcher → [Gate 1] → Writer → [Gate 2] → Editor → Reviewer ⇄ Editor (max 3 cycles)
```

Guided mode (default): Gate 1 = user approves the fact sheet; Gate 2 = user approves
the draft direction. **Express** (user says so): skip both gates, present only the
finished chapter.

Each child's prompt must contain: its role section from `references/agent-briefs.md`
(tell it to read that file), the project path, the exact input files
(`.pipeline/<prev>.md`, `style-profile.md`, `state.md` as its brief requires), the
book's language + variant from book.md, and the output file to write. Reviewer flags →
spawn Editor in fix-cycle mode with the flags verbatim → Reviewer rereads. You count
the cycles; max 3; leftover flags go to the user, never dropped.

**After the chapter:** back up any file you are about to overwrite to
`<project>/versions/<name>.<YYYYMMDD-HHMMSS>.<ext>` (no exceptions), save the chapter
to `manuscript/`, apply the Writer's State updates to `state.md` (terminology,
examples, facts, cross-refs, promises), update the chapter map row in `book.md` and
the registry's "last touched".

**Voice learning:** when the user hand-edits a chapter or gives voice feedback, run
the Librarian in update mode (style-analysis.md §8) — dated changelog entry, always.

## Compile

The Compiler child follows its brief in agent-briefs.md and runs:

```
python "<this skill folder>/scripts/compile_book.py" master.txt "<project>/output/<Title>.docx" \
  --title "…" --subtitle "…" --author "…" [--sample "<project>/sources/sample.docx"]
```

Stdlib only — no pip installs. `--sample` clones the user's formatting; without it the
built-in book template is used. Word asks to update the TOC on first open — tell the
user that's expected.

## Non-negotiables

- **The author's voice is paramount.** `style-profile.md` is law for reader-facing
  text; its whitelist (≥3-occurrence evidence) overrides writing-rules.md — except
  rules the author has explicitly locked, which bind above everything.
- **The book's language and variant are fixed in book.md.** A voseo book never drifts
  into tuteo.
- **No invented facts.** Sourced, or ⚠️-flagged. Never silently resolved.
- **Never lose the user's words.** versions/ backup before every overwrite.
- **Full outputs between stages.** Children exchange complete files, not summaries.
