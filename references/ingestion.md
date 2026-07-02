# Ingestion Playbooks — getting the author's words in

For the Librarian (style corpus) and Researcher (reference material). Destination:
`sources/style/` for voice samples, `sources/research/` for facts. One rule above all:
**never fail hard.** If a connector isn't available, say exactly what to do instead —
the file-drop folder always works.

## Hygiene — applies to every source

- **Only the author's own words.** Strip quoted text, retweets, forwarded content,
  boilerplate signatures, and anything they didn't write. A corpus polluted with other
  people's prose poisons the fingerprint.
- **Tag register on save:** name files `<register>--<desc>.md` (e.g. `casual--tweets-2024.md`,
  `book--old-manuscript-ch1.md`) so weighting (style-analysis.md §2) is mechanical.
- **Dedupe** near-identical drafts of the same piece; keep the latest.
- Save extracted text as UTF-8 `.md`/`.txt` in the project — the original files stay
  wherever they live; never modify them.

## Local files (always available)

- `.txt` / `.md` — Read directly.
- `.docx` — extract with stdlib Python:
  ```bash
  python -c "
  import zipfile, re, sys
  z = zipfile.ZipFile(sys.argv[1])
  xml = z.read('word/document.xml').decode('utf-8')
  xml = re.sub(r'</w:p>', '\n', xml)
  text = re.sub(r'<[^>]+>', '', xml)
  print(re.sub(r'[ \t]{2,}', ' ', text).strip())
  " "path\to\file.docx"
  ```
- `.pdf` — the Read tool handles PDFs (use `pages` for long ones).
- Whole folders: the user can point at any folder ("my essays are in D:\writing") —
  glob it, extract each file, confirm the inventory before analyzing.

## URLs (always available)

Public blogs, Substack, Medium, articles: WebFetch with a prompt like "Return the
article body text verbatim, excluding navigation, comments, and bylines." Paywalled or
login-only pages fail — tell the user to copy-paste or save as PDF instead.

## Google Drive

1. Check for connected Google Drive MCP tools (tool names containing `drive` or
   `google_drive` — e.g. search/fetch style tools). If present: search for the docs the
   user names, fetch content, save to `sources/`.
2. If absent, two good fallbacks — offer both:
   - claude.ai users: enable the Google Drive connector in Settings → Connectors, then
     retry here.
   - Fastest universally: download the files (File → Download → .docx) into
     `sources/style/` — done.

## Notion

Check for Notion MCP tools (`notion-search`, `notion-fetch`). If present: search the
workspace for the pages the user names, fetch, save. If absent: Notion → ••• → Export →
Markdown, drop the export in `sources/`.

## Databases (Airtable, Supabase, etc.)

If a database MCP is connected (Airtable `list_records…`, Supabase `execute_sql`, etc.),
ask the user which base/table and which field holds their writing, pull the text fields,
concatenate to a tagged corpus file. If not connected: export to CSV and drop it in
`sources/` — parse the text column(s) from there.

## X / Twitter

There is no free public API. The reliable path is the official archive export:

1. User: X → Settings → Your account → **Download an archive of your data** (arrives as
   a .zip within ~24h).
2. User drops the zip (or its `data/tweets.js`) into `sources/style/`.
3. Parse — `tweets.js` is JSON behind a JS prefix:
   ```bash
   python -c "
   import json, re, sys, io
   raw = io.open(sys.argv[1], encoding='utf-8').read()
   data = json.loads(raw[raw.index('['):])
   out = []
   for t in data:
       tw = t.get('tweet', t)
       txt = tw.get('full_text', '')
       if txt.startswith('RT @'): continue          # not the author's words
       txt = re.sub(r'https://t\.co/\S+', '', txt).strip()
       if len(txt.split()) >= 5: out.append(txt)    # skip fragments
   print('\n\n'.join(out))
   " "sources\style\tweets.js" > "sources\style\casual--tweets.md"
   ```
   Ask the author whether to keep replies (they're conversational — often the *most*
   voice-rich material, but noisy).

## Email

Gmail MCP connected (`search_threads`, `get_thread`): ask for a search that surfaces
*written-by-them* mail (e.g. `from:me newsletter`), extract only their sent text, tag
as `professional--` or `casual--`. No connector: paste, or forward-and-export to a file.

## Research material (`sources/research/`)

Same mechanics, opposite rule: this is *other people's* words on purpose — papers,
articles, data, notes. Keep provenance: every saved file gets a first line
`Source: <origin, date>` so the Researcher can cite it in fact sheets.
