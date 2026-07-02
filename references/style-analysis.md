# Style Analysis — building and maintaining the voice fingerprint

Methodology for the Librarian. The output, `style-profile.md`, is the single most
important file in a book project: every reader-facing word the skill produces is
constrained by it. The doctrine is **strict mimicry** — the profile describes how the
author actually writes, not how they "should" write, and downstream agents replicate it
even where generic style advice disagrees.

---

## 1. Corpus tiers

Work with whatever exists — a few tweets or three published books.

| Corpus size | Approach |
|---|---|
| **None** | No-corpus fallback interview (§7). Profile marked `confidence: seed`. |
| **Tiny** (< 500 words) | Extract what's measurable, lean hard on the calibration test, mark `confidence: low`. Recommend the author add more samples when they can. |
| **Small** (500–5,000) | Full fingerprint, flag metrics computed from thin data. `confidence: medium`. |
| **Medium** (5k–50k) | Full fingerprint from everything. `confidence: high`. |
| **Large** (50k+, e.g. whole books) | Don't read everything. Sample ~10 chunks of ~800 words per source, spread evenly (openings, middles, endings — endings especially; they carry the author's closing moves). Compute metrics on the sample; note the sampling in the profile. |

## 2. Register weighting

Not all samples deserve equal weight. Tag each source with a register and weight
book-adjacent material highest:

1. **Book-register** (prior books, long essays, serious blog posts) — primary evidence.
2. **Professional** (reports, newsletters, articles) — strong evidence.
3. **Casual** (tweets, chat, quick emails) — evidence for lexicon and attitude, weak
   evidence for sentence structure (nobody writes chapters like tweets).

When registers conflict, book-register wins. Record which registers fed the profile so
the author understands what it's based on.

## 3. The fingerprint — style-profile.md skeleton

Produce exactly this structure:

```markdown
# Style Profile — [Author name]
Confidence: seed | low | medium | high
Corpus: [N sources, ~N words, registers: …, sampled: yes/no]
Fidelity: strict — this profile is law for Writer and Editor

## Metrics
- Sentence length: median N words; typical range N–N; distribution note
  (e.g. "spiky — 5-word punches against 30-word builders" or "even, 12–18")
- Paragraph length: typical N–N sentences; uses single-sentence paragraphs: yes/no/rarely
- Contractions: always / frequent / rare / never (in book register)
- Punctuation habits: em-dash per 1,000 words ≈ N; semicolons: y/n; parentheticals:
  frequent/rare; question marks per 1,000 ≈ N (rhetorical questions y/n); exclamations: y/n
- Reader address: I / you / we / impersonal — and in what mix. Languages with T-V
  distinction: record the exact system the corpus uses (Spanish: tuteo / voseo /
  usted — e.g. "vos throughout, rioplatense conjugation") and flag any inconsistency
  to the author instead of averaging it away
- Paragraph openers: [the author's actual habits — e.g. "opens with the claim, evidence
  follows"; "often opens with 'And'/'But'"]

## Lexicon
- Signature words/phrases (with observed counts): …
- Words the author never uses (that a model would reach for): …
- Formality register: [placement + evidence]
- Jargon comfort: [explains everything / assumes an educated reader / …]

## Structural habits
- How sections open: …
- How sections close: [recaps? lands a line and stops? bridges forward?]
- Transitions: [explicit connectors vs hard cuts]
- Explanation style: [story-first / claim-first / numbers-first; analogy frequency and
  their source domains]
- Heading style: [sentence case? full sentences? single nouns?]

## Touchstones
[3–5 verbatim passages, 50–150 words each, chosen because they are the most
*characteristic* — not the best — writing in the corpus. Cite the source of each.]

## Whitelist — banned-pattern overrides
[Entries from writing-rules.md's banned lists that this author genuinely uses.
Each entry needs evidence: the item, ≥3 verbatim occurrences with sources.
e.g. — "robust": 5 uses across 3 essays ("robust little routine", …) — allowed.
No evidence = no entry. Empty section is normal.]

## Calibration log
- [YYYY-MM-DD] Variant B chosen ("plainer, fewer asides"); profile adjusted: …

## Changelog
- [YYYY-MM-DD] Created from N sources.
```

## 4. Measuring

Estimates beat false precision. For sentence/paragraph metrics on a bigger corpus, a
quick Python pass (split on `.!?`, count words) is fine — note that abbreviations skew
it slightly and move on. For lexicon, count actual occurrences before calling something
a signature word: a word used twice is not a signature. **The touchstones matter more
than any number** — a Writer who internalizes five characteristic passages beats one
holding twenty statistics.

## 5. Whitelist evidence rule

An entry from the banned lists gets whitelisted only with **≥3 occurrences in the
author's own words** (not quotes of others), ideally across more than one sample. Record
the occurrences in the profile. This is the strict-mimicry contract: the corpus can
override the anti-AI rules, hunches cannot.

## 6. Calibration test — always run after building a profile

The numbers can be right and the feel still wrong. Before the profile goes live:

1. Pick a paragraph-sized topic close to the book's subject.
2. Write it three ways, all consistent with the profile but varying the axes you're
   least sure of (warmth, density, directness, humor).
3. Orchestrator presents all three via AskUserQuestion: "Which sounds most like you?"
   plus what's off about it.
4. Fold the answer into the profile (Calibration log entry). One follow-up round at
   most — the profile keeps learning from real chapters after this (§8).

## 7. No-corpus fallback

The author has nothing written. Interview instead:

- Ask for three writers/books whose voice feels *comfortable* to them (not aspirational —
  comfortable), and what specifically they like.
- Ask them to tell you, in their own typed words, why this book matters — a few
  sentences. That paragraph *is* corpus; mine it.
- Ask the binary habits directly: contractions? addressing the reader as "you"? humor on
  the page? stories or numbers first?
- Build a `confidence: seed` profile, then run the calibration test with **five**
  variants instead of three, twice. The test carries the weight the corpus can't.
- Tell the orchestrator to recommend recalibration after chapter 1 is approved — the
  author's edits to a real chapter are the best sample they'll ever provide.

## 8. Update mode — learning from approvals

Triggered by the orchestrator when the author hand-edits a chapter or gives style
feedback in conversation.

1. **Diff, don't skim.** Compare the author's edited text against the agent's version.
   Each consistent change is a signal: shortened openers, cut adjectives, added asides,
   swapped vocabulary.
2. **Generalize the instance into a habit** ("removed 4 of 5 semicolons" → punctuation
   habit updated), then update the affected profile section.
3. **Changelog every update, dated,** one line per inference, with the trigger
   ("author's edits to ch. 3"). The changelog is how the author audits what the skill
   thinks it knows about them.
4. **Touchstones are append-mostly:** an author-edited passage of a real chapter is the
   highest-grade touchstone available — add the best one. Never delete an
   author-approved touchstone; retire (strike through) only if the author contradicts it.
5. Feedback in plain words ("too stiff") updates the profile the same way — but record
   it as stated intent, and look for what concretely to change in the nearest chapter.

Recalibrating from scratch (`/book style` rerun) rebuilds §§1–6 but always preserves the
Calibration log and Changelog history.
