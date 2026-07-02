# Writing Rules — the anti-AI catalog

Read by the Writer before drafting, and by the Editor as the audit standard. These rules
exist for one reason: the finished book must read like the author wrote every word, not
like a well-prompted model did.

**Precedence:** `style-profile.md` outranks this file. If the profile's whitelist says
the author genuinely uses a banned word or pattern (≥3 occurrences across their corpus),
that entry is allowed *for this author* and the Editor must not remove it. Everything not
whitelisted is enforced exactly as written here.

**Language:** the vocabulary and phrase lists in §§2–4 are English. For books in another
language, read the companion file `references/lang/<code>.md` when it exists (Spanish:
`lang/es.md`, including Argentine voseo) — it replaces §§2–4 and adds variant grammar
rules. The five tell families (§1), structure rules (§5–6), and compression discipline
(§7) apply in every language.

---

## 1. The five families of AI tells

Audit every draft against all five. Most editors catch family 2 and miss the rest.

**Content tells** — inflated significance ("plays a vital role in"), unearned superlatives,
promotional framing of neutral facts, vague attribution ("experts agree", "studies show"
without a named source), symmetric pro/con or "challenges and opportunities" passages,
generic examples that could appear in any book on the subject.

**Language tells** — the banned vocabulary below; copula avoidance ("serves as", "stands
as", "functions as" instead of "is"); negative parallelism ("not just X, but Y"); forced
rule-of-three everywhere; synonym cycling to avoid repeating a plain word; false ranges
("from X to Y" as decoration); subjectless participle openers ("Building on this idea,").

**Style tells** — em/en-dash overuse; bold used for emphasis instead of first-use terms;
lists where prose belongs; Title Case Headings; emoji; curly-quote inconsistency; three
same-length sentences in a row; every paragraph the same size.

**Communication tells** — chatbot residue ("I hope this helps", "let's explore");
narrating the writing ("in this chapter we will"); recapping what was just said;
sycophantic or cheerleading tone; hollow authority ("it is widely recognized that").

**Filler and hedging tells** — wordy scaffolding ("it is important to note that"); stacked
qualifiers; generic conclusions ("ultimately, the journey continues"); signposting
("as mentioned earlier"); staccato drama fragments ("And that changes everything.").

## 2. Banned vocabulary

Remove every instance unless whitelisted by the style profile.

delve — tapestry — nuanced / nuance (as filler) — multifaceted — testament ("a testament
to") — pivotal — underscore(s) (as a verb) — foster(s) — navigate(s) (metaphorically) —
paramount — synergy — robust — leverage (as a verb) — transformative — holistic — embark —
realm — landscape (metaphorically) — cornerstone — comprehensive — seamlessly —
empower(s) — crucial (as filler) — vital (as filler) — utilize — unlock — harness —
showcase — vibrant — game-changer — elevate (metaphorically) — journey (metaphorically)

## 3. Hedge words

Cut them; the sentence almost always improves.

quite — rather — somewhat — essentially — basically — generally — typically — usually —
possibly — potentially — arguably — presumably — seemingly — apparently — in a sense —
in some ways — to some extent — to a degree

**Before:** "Diversification is quite important and can potentially reduce your risk."
**After:** "Diversification reduces your risk."

Exception: a hedge that carries real epistemic content ("this study has not been
replicated") stays. Hedges that only soften confidence go.

## 4. Banned phrases and openers

- "It is important to note that…" / "It's worth noting…" / "Worth mentioning…"
- "As we can see…" / "As mentioned earlier…"
- "In today's [world / landscape / society / fast-paced …]"
- "Let's explore / dive into / take a look at…"
- "Not just X, but Y" and its negative-parallelism cousins
- "At the end of the day…" / "In essence…" / "In summary…" / "In conclusion…"
- "This underscores / highlights the importance of…"
- "A journey toward…" / "paving the way for…"
- "Here's the thing…" / "Here's the part most people miss…" / "Let's be clear…" /
  "Honestly?" / "The truth is…" / "The reality is…" (false-directness openers — AI trying
  to sound casual)
- "First and foremost…" / "It goes without saying…"
- "In other words…" followed by a restatement that adds nothing
- Any sentence that recaps what was just said before moving on

## 5. Structure rules

- **Bullets only where the book's chapter template calls for them** (check book.md).
  Everywhere else, explanations are prose. A list of benefits becomes a paragraph that
  argues them.
- **No recap endings.** Sections end by landing the point or bridging forward — never by
  summarizing themselves.
- **No meta-commentary.** The book doesn't narrate itself. Beyond whatever introduction
  the chapter template requires, never announce what's about to be explained.
- **No vague forward-looking closings** ("challenges lie ahead…"). Bridge to the next
  idea or just stop.

## 6. Style mechanics

- **Em dashes:** default budget 2 per chapter. The style profile overrides this in either
  direction if the corpus shows a different habit.
- **Headers:** sentence case, unless the profile shows the author capitalizes differently.
- **Bold:** first introduction of a term only — never for emphasis.
- **Sentence variety:** if three consecutive sentences land within a few words of the same
  length, rewrite one. Match the *profile's* length distribution, not a generic ideal.
- **Paragraph rhythm:** vary sizes; short paragraphs land punches, longer ones build.
- **No emoji** unless the profile whitelists them (some authors' registers include them).

## 7. Compression

Over-explanation is the most reliable AI tell of all, and no banned-word list catches it.

- Explain a concept once, clearly, and move on. Never restate.
- If a story has landed its point, stop. Do not explain the lesson after the story told it.
- Respect the per-chapter word target in book.md (derived from the author's interview and
  corpus). A chapter 40%+ over target is over-explaining somewhere — find it and cut.
- The test for any paragraph: "am I explaining something I already showed?" If yes, cut
  the explanation.

## 8. Pre-flight checklist

The Writer runs this before submitting; the Editor runs it again before finalizing.

- [ ] No banned vocabulary (minus profile whitelist)
- [ ] No hedge words carrying zero epistemic content
- [ ] No banned phrases or false-directness openers
- [ ] All five tell families audited, not just vocabulary
- [ ] Bullets only where the chapter template allows
- [ ] No section ends on a recap; no meta-commentary anywhere
- [ ] Sentence lengths track the profile's distribution; no three-alike runs
- [ ] Em dashes within budget; bold only for first-use terms; sentence-case headers
- [ ] Every factual claim traces to the fact sheet or carries a ⚠️ flag
- [ ] Word count within the chapter target range from book.md
- [ ] Terminology matches state.md (same term, same meaning, every chapter)
- [ ] Read a random paragraph aloud mentally: does it sound like the touchstone passages
      in style-profile.md? If it sounds like "good writing" instead of *this author's*
      writing, it fails.
