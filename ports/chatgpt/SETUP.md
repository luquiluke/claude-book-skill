# Book Studio — Custom GPT setup guide

Turns the /book skill into a ChatGPT Custom GPT. One-time setup, ~10 minutes,
requires ChatGPT Plus (GPT creation). The pipeline runs as sequential role passes
with the same two approval gates; the book persists as a `book.zip` the user keeps
(unpacked/repacked by Code Interpreter each session); Word compilation runs the same
stdlib script via Code Interpreter.

## 1. Create the GPT

ChatGPT → Explore GPTs → **+ Create** → Configure tab:

| Field | Value |
|---|---|
| **Name** | Book Studio — write in your voice |
| **Description** | Writes non-fiction books as you, not for you — six editorial roles, your measured voice, real Word output. Español rioplatense incluido. |
| **Instructions** | Paste the entire body of [`GPT-INSTRUCTIONS.md`](GPT-INSTRUCTIONS.md) (everything below the `---`) |

## 2. Capabilities

- ✅ **Code Interpreter & Data Analysis** — required (zip protocol + docx compile)
- ✅ **Web Search** — the Researcher's gap-filling and fact verification
- ⬜ Canvas — optional (nice for reading long chapters)
- ⬜ Image generation — off

## 3. Knowledge files (upload these 7 from the repo)

| Upload | Note |
|---|---|
| `references/writing-rules.md` | Anti-AI catalog + checklist |
| `references/style-analysis.md` | Voice fingerprint methodology |
| `references/agent-briefs.md` | The six role briefs |
| `references/project-template.md` | Setup interview + project scaffold |
| `references/ingestion.md` | Sample-intake playbooks (uploads replace connectors) |
| `references/lang/es.md` | **Rename to `lang-es.md`** before upload (knowledge storage is flat; the instructions reference that name) |
| `scripts/compile_book.py` | Code Interpreter runs it for the .docx |

## 4. Conversation starters

- Start a new book
- Here's my writing — learn my style
- Continue my book (I'll upload my book.zip)
- Compile my book to Word

## 5. Publish

Save → share as **Only me** to test, **Anyone with the link** to share, or **GPT
Store** to publish. Test script before publishing: start a new book (interview should
begin), paste a writing sample (fingerprint + calibration test should follow), say
"write chapter 1" (Researcher pass → Gate 1 question should appear), then "give me
the zip" (download link should arrive).

## Known limits vs. the CLI versions

- Roles run sequentially in one context, not as isolated subagents — the labeled-pass
  discipline in the instructions is the mitigation.
- Persistence is the user's zip; if they lose it, the book state is gone (chapters
  they downloaded survive). The GPT reminds them every session.
- Long guided chapters can hit Plus usage limits — express mode and stage-at-a-time
  are the fallbacks, and the GPT suggests them when needed.
- Keep knowledge files in sync with the repo when the skill updates (re-upload the
  changed files in the GPT editor).
