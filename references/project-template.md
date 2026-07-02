# Project Template — creating and importing book projects

## Folder layout

Default parent (the Books root): `~/Documents/Books` — Windows:
`%USERPROFILE%\Documents\Books`. A root named in the user's memory, CLAUDE.md, or
conversation overrides the default. Create on first use; the user may place any
individual book elsewhere (registry rows carry full paths). Project slug: kebab-case
short title.

```
Books/
├── registry.md                  ← all books, one row each
└── <slug>/
    ├── book.md                  ← premise, audience, chapter template, chapter map
    ├── style-profile.md         ← the voice fingerprint (Librarian owns it)
    ├── state.md                 ← continuity bible (orchestrator maintains it)
    ├── sources/
    │   ├── style/               ← author's writing samples (drop anything here)
    │   ├── research/            ← reference material for the book's content
    │   └── sample.docx          ← optional: formatting to clone at compile time
    ├── research/                ← chapter-NN-facts.md fact sheets
    ├── manuscript/              ← chapter-NN-<slug>.md (the book itself)
    ├── versions/                ← timestamped backups, made before every overwrite
    └── output/                  ← compiled .docx
```

## registry.md format

```markdown
# Books
| Slug | Title | Path | Language | Status | Last touched |
|---|---|---|---|---|---|
| garden-year | A Year in the Garden | C:\...\Books\garden-year | en | drafting 4/12 | 2026-07-02 |
```

If the registry is missing but the Books folder has projects, rebuild it by scanning for
`book.md` files.

## The setup interview (`/book new`)

**Stage 1 — always, five questions.** Conversational, one or two at a time, not a form:

1. **Subject & working title** — what is the book about, in their words?
2. **Reader** — who picks this up? Age, background, what they already know. (This becomes
   the Reviewer's persona — get it concrete: "small-business owners who hate spreadsheets,"
   not "adults.")
3. **Transformation** — what can the reader do or understand after the last page that
   they couldn't before? (This is the book's spine; every chapter must serve it.)
4. **Size & language** — rough ambition (short 20k? standard 50k? big 80k+?) and the
   book's language (default: the language of their writing samples). For languages with
   meaningful variants, pin the variant and reader address now — Spanish especially:
   ¿tuteo, voseo o usted? ¿es-AR rioplatense, latino neutro o peninsular? Detect the
   likely answer from the samples (an Argentine corpus is full of voseo) and confirm
   rather than ask cold. Record it as e.g. `es-AR · vos (voseo rioplatense)`.
5. **Raw material** — existing drafts, notes, or research to import? Writing samples for
   the style profile?

**Stage 2 — offer, don't force:** "Want to go deeper before we outline? Ten more minutes
on positioning sharpens every chapter." If yes:

- Competing books: what exists, and what's this book's answer to "why does yours exist?"
- The reader's before/after journey mapped to a part-structure (arc).
- Tone boundaries: anything the book must never do (preach, hype, dumb down…).
- The author's relationship to the subject — why *them*? (Feeds the intro and About the
  Author.)

**Then, from the answers, generate the chapter template** — the named sections every
chapter will follow (like rift's 8-section template, but derived from *this* book's genre
and promises). Propose it, let the author edit, store the approved version in book.md.
Also derive the **word target**: total ambition ÷ planned chapters, cross-checked against
the corpus's natural section density once the profile exists (note both numbers; the
range in book.md is the contract).

## book.md skeleton

```markdown
# [Working Title]
Slug: … · Language: [code + variant + address, e.g. `es-AR · vos (voseo rioplatense)`
or `en`] · Created: YYYY-MM-DD

## Premise
[2–4 sentences: subject + the book's answer to "why this book?"]

## Reader
[Concrete persona. What they know, what they want, why they picked this up.]

## Transformation
[What the reader can do/understand after the last page.]

## Positioning  (stage 2; optional)
[Competing books and this book's difference. Tone boundaries.]

## Chapter template
[The named sections every chapter follows, in order, with per-section length notes.]

## Targets
Total: ~N words · Per chapter: N–N words · Chapters: ~N

## Chapter map
| # | Title | Promise (one line) | Key points | Status |
|---|---|---|---|---|
| 1 | … | … | … | outlined / researched / drafted / edited / final |
```

## state.md skeleton

```markdown
# State — [Title]   (continuity bible; orchestrator updates after every chapter)

## Terminology            ← doubles as the compiled glossary
| Term | Definition used in the book | Introduced in |
|---|---|---|

## Recurring examples & stories
| Example | Established details (don't contradict) | Appears in |
|---|---|---|

## Established facts & figures
| Fact/figure | Context | Chapter |
|---|---|---|

## Cross-references
[Chapter N points the reader to chapter M for …]

## Promises to the reader
[ "We'll cover X in chapter N" — every promise must eventually be delivered or cut ]

## Chapter notes
| # | One-paragraph summary once drafted |
|---|---|
```

`style-profile.md` starts as a stub ("Not yet built — run style ingestion"); its real
skeleton lives in style-analysis.md §3.

## Import flow (existing drafts)

1. Copy originals into `sources/` (never touch the user's files); extract text.
2. Map drafts to chapters in the chapter map (create rows as needed).
3. **Per draft, ask:** **Expand** — its structure and concepts are the backbone,
   preserved in order, agents build around them (right when the draft *is* the author's
   plan) — or **Raw material** — mined for content and voice, restructured freely (right
   for rough notes). Record the choice in the chapter map row.
4. Drafts are corpus too: register-tag a copy into `sources/style/` (`book--draft-chN.md`)
   unless the author says the draft isn't in their voice.
5. `{curly brace}` comments inside drafts are author instructions — the pipeline routes
   them (fact questions → Researcher, prose directions → Writer).

## Versioning policy

Before any overwrite of `manuscript/*`, `book.md`, `state.md`, or `style-profile.md`:
copy the current file to `versions/<name>.<YYYYMMDD-HHMMSS>.<ext>`. Cheap insurance,
no exceptions. Restoring = copying back; mention it if the user regrets a change.
