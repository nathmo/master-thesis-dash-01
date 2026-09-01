# CLAUDE.md

Working instructions for this repository. The style rules are not suggestions: they were
established by explicit user decisions and by an editing pass already applied to every chapter
(commit `675da7c`). Follow them when writing or editing prose, and check the compliance list
before reporting an edit as done.

## The repository

Master thesis: *DASH-01, RL Framework to Develop a Bipedal Humanoid Robot Aimed at Breaking the
Speed Record* (EPFL, REHAssist, 2025-26).

- `main.tex` : front matter, abstract, includes `Chapters/ch1`..`ch6` and `Chapters/append`.
- `General/` : `Preamble.tex` (packages), `Settings.tex`, `MathCommands.tex`.
- `Chapters/` : all prose. This is where edits happen.
- `References.bib`, `Figures/`.
- `FilRouge.md` : the author's working outline and notes. Drafting scratch, not thesis prose, and
  not bound by the prose rules below.
- `main.aux`, `.log`, `.fls`, `.fdb_latexmk`, `.bbl`, `.toc`, `.synctex.gz` : build output. Never
  edit.

Build: `latexmk -pdf main.tex`. CI (`.github/workflows/latex.yml`) rebuilds `main.pdf` on every
push to `main` and commits it back, so hand edits to `main.pdf` are lost. Compile before claiming
an edit is finished, and report the page count and any new warnings.

## 1. Absolute rules

**No em dashes. Ever.** Not the character (U+2014), not the LaTeX `---`. This holds in the thesis
and in chat replies to the user alike. Substitutes, in order of preference:

- Paired em dashes (parenthetical interruption): parentheses if the interior contains commas,
  otherwise plain commas.
- Single em dash introducing an explanation, apposition or list: a colon.
- Single em dash before a contrastive tail: a comma, a semicolon, or two sentences.
- Table cell meaning "no data": an en dash (`--`), never `---`.

En dashes stay legal for numeric ranges (`0.010--0.012`) and hyphenated compounds. Decorative
`% --- separator ---` comment lines are invisible in the PDF and may stay.

**No editorializing metadiscourse.** Three banned classes:

- *Boosters*, unearned significance or emphasis: "the most important result", "clearly",
  "strikingly", "notably", "it is important to note that", "crucially".
- *Engagement markers and reader address*, narrating the reader's reaction or steering attention:
  "notice that", "as you can see", "that property is often missed", any second person.
- *Curiosity-gap teases* that promise a payoff instead of delivering the content.

Banned in headings too, as **payoff titles**: a title whose second half advertises significance or
promises the answer instead of stating it ("The hopping lineage's assumptions, and why DASH-01
breaks all three"). The legitimate form is the **message title**, which states the finding outright
("The drive's position loop is 0.8\,Hz", "Peak torque is what the gearbox delivers, not what the
datasheet quotes"). Test: does the title give the answer, or make the reader read on for it?
Giving it is required, withholding it is banned.

Significance is demonstrated by evidence, not asserted by the narrator. If something matters,
attach the reason as an explicit claim in the discussion, not as an adjective. When editing
existing text, strip these constructions rather than rewording them.

## 2. Sentence mechanics (Simplified Technical English lite)

Five controlled-language rules adapted from ASD-STE100, already applied to every chapter. Measured
outcome to hold: mean sentence length 14.7 words, p90 24, longest 42, at most 8 percent of
sentences over 25 words.

1. One idea per sentence, 25 words maximum.
2. Fixed terminology: one term per concept, for the whole document.
3. Explicit agent, present tense for facts about the system.
4. No noun stack longer than three, no unanchored "this" or "it".
5. One topic per paragraph.

Three conventions standardised along the way:

- **Voice.** Passive voice. Never write a sentence with "I" or "we" (author decision, 2026-09-01,
  reversing the earlier first-person convention; remaining first-person sentences are converted as
  chapters get edited). "The author" and "one" stay banned too. Keep the agent recoverable where
  it matters ("the workspace is recorded by backdriving the leg").
- **Spelling.** British throughout.
- **Terminology.** "drive" for the integrated CubeMars unit (not motor controller, board, driver,
  drive electronics). "robot" for the physical machine, "plant" for the model, and "machine" is not
  a synonym for either. "hip roll", not "abduction". "centre of mass" in prose. "4-bar".

## 3. Argument structure

The thesis is a first-principles design-rationale document, not an IMRaD paper. The justification
chain is the skeleton: physics and measurement first, then constraints, then the design that
follows from them, then validation.

1. **Chain rule.** Every section produces something a later section consumes: a number, a range, a
   criterion, or a table row. If nothing downstream uses it, cut it or move it to the appendix.
2. **Roadmap paragraph.** Open each chapter with two to four sentences: what it establishes and why
   it follows the previous one. Close by naming what it hands to the next.
3. **Justify before proposing.** No design decision appears before the constraint that forces it.
4. **Mark epistemic status.** Every claim is one of four kinds, and the last two are marked out
   loud: derived (show the equation), measured or cited (reference on the spot), assumed (write
   "assuming", and give the value), opinion (write "in my view"). An unmarked opinion is a defect.
5. **Section pattern.** Setup, equation, symbol list with units, substitution with the worst-case
   number, result, then the design consequence and its cost. End on the consequence, not on the
   number.
6. **Name the cost.** Any claimed advantage states its price in the same paragraph.
7. **Declare exclusions where they bite**, with the reason (out of scope, time, requires a dynamic
   controller). Limitations go inline, not only in a closing section. Silence implies coverage.
8. **Measurement before assumption.** An assumed plant number stays labelled as assumed until it is
   measured. When measurement reverses it, say so, and say what it changed.
9. **Adversarial review of anything that produces a number.** Rewards, simulators, estimators and
   evaluators each produced a confident wrong answer in this project. Prose that reports a number
   also reports how the number was checked.

## 4. Numbers and units

10. Every quantity carries a unit, and every symbol is defined once, at first use, in a definition
    list. Units take a thin space: `200\,Hz`, `0.8\,m/s`, `12\,kg`. `siunitx` is loaded if a macro
    form is wanted, but `\,` is the established convention across the chapters.
11. Compute the worst case first, then state the practical target as a range.
12. State the precision claimed ("order of magnitude", "$\approx$"). Never report more digits than
    the input justifies.
13. No orphan numbers. Any number that decides something carries a derivation or a source. This
    applies to efficiencies, rates and datasheet figures as much as to measurements.
14. One number format per document: no mixing of `1'745` and `1300`.

## 5. Tables, figures, LaTeX

15. Comparison tables reuse the same row set and the same ordinal scale across the whole document,
    so that two tables can be diffed column by column. Numbers and ordinal ratings may share a
    table without apology.
16. Every table and figure has a unique caption. Two objects never share caption text.
17. `\cref` for all internal references (cleveref is loaded with `noabbrev, capitalise`). Never
    bare `\ref`.
18. `booktabs` rules, `enumitem` lists with `leftmargin=*`, `\paragraph{...}` for message-titled
    sub-blocks, `\textbf{Term.}` as list lead-ins, `\emph` for concept emphasis.
19. A prose editing pass does not touch tables, equations, figures or numbers. If a prose edit
    requires changing a number, stop and say so.

## 6. Before reporting an edit as done

- `grep -n -- '---' Chapters/*.tex` and `LC_ALL=C.UTF-8 grep -nP '\x{2014}' Chapters/*.tex`, since
  the two forms render identically. The `LC_ALL` prefix is required: plain `grep -P` fails on this
  machine with "supports only unibyte and UTF-8 locales". From PowerShell:
  `Select-String -Path Chapters\*.tex -Pattern ([char]0x2014)`. Ignore `%` comment lines.
- Spellcheck. The recurring failure mode is French interference: *accomodate*, *bellow* for below,
  *wheights*, *non negligeable*, *deccelerate*, *addoption*, *tunning*, *comming*, plus dropped
  verbs and article slips.
- No label, `\cref` target or citation key lost.
- `latexmk -pdf main.tex` exits clean, and the page count is reported.

## 7. Committing

Commit after every change, without waiting to be asked. This is standing authorisation: do not ask
first, just commit once the build is clean.

- Commit the author's own uncommitted edits too. They work in the editor between turns, so the
  working tree usually holds their changes as well as mine. Sweep them into the same commit rather
  than leaving them stranded.
- Commit only after `latexmk -pdf main.tex` exits clean. A broken build is not committed.
- Do not commit `main.pdf`. CI rebuilds it on every push to `main` and commits it back, so a hand
  committed PDF is overwritten and only creates merge conflicts. It stays modified in the working
  tree, and that is expected.
- Do not push unless asked. Committing is automatic, publishing is not.
- One commit per logical change, with a subject line that names what changed and why.
