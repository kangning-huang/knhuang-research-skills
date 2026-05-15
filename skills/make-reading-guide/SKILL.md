---
name: make-reading-guide
description: "Generate a print-ready HTML reading guide with prioritized chapter checklist and goal-targeted extraction questions. Takes a table of contents (image, PDF, paste, or URL) plus reading context, produces a single self-contained HTML file with tiered chapters, sub-topic checkboxes, and 3 to 5 guided questions per chapter. Use when the user has a book or paper to read and wants a structured plan before diving in."
allowed-tools: ["Read", "Write", "Edit", "WebFetch", "Bash", "Grep", "Glob"]
---

# make-reading-guide: Reading Guide Generator

Given a table of contents (from images, PDF, text paste, or URL) and context about why
the user is reading this material, produce a print-ready HTML reading guide with:
- A project context preamble
- Chapters prioritized into tiers
- Section-level checkboxes for every sub-topic in the TOC
- Guided questions tailored to the user's reading goal

---

## Configuration

This skill needs one user-specific setting before first use.

**Output directory.** Where to save generated guides. Default: `~/reading_guides/`.
You can override by:
1. Editing the default path in Step 6 below, or
2. Setting a path in your project's `CLAUDE.md`, for example:
   `Reading guide output: ~/Documents/MyResearch/reading_guides/`

If the user has never set an output location, ask once on first run and remember it
in `CLAUDE.md` for future invocations.

---

## Step 0: Gather inputs

You need two things. If either is missing, ask before proceeding.

**A. The table of contents.** Accept in any form:
- Images (screenshots of TOC pages): read all visible chapters and sub-topics
- PDF path: read the TOC pages
- Text paste: use directly
- URL: fetch the page
- Already in conversation: use it

Extract chapter numbers, titles, page ranges, and all sub-topic entries within each chapter.

**B. Reading context.** Ask if not provided:
> "Tell me: (1) what is your research goal or project this reading connects to, and (2) what specifically do you need from this material: background, equations, empirical values, conceptual framework, something else?"

If the user is reading for general interest or recreation rather than research, skip
the extraction framing and use a register appropriate to that kind of reading (see
the Material types table near the bottom).

---

## Step 1: Understand the reading goal

Before prioritizing, extract from the user's context:

- The claim they are trying to support: what does their model, argument, or hypothesis say?
- The role this book/paper plays: framework, constraints, empirical data, background, methodology?
- Key variables or questions: what specific things do they need to be able to write down after reading?
- Their active projects: check `CLAUDE.md` and any project memory for ongoing work context. Do not assume project names; use whatever the user's files actually say.

If reading context is rich, synthesize it into three pieces for the preamble:
1. What they are trying to show (the claim)
2. What this material gives them specifically
3. Three standing questions to carry through every chapter

---

## Step 2: Prioritize chapters

Assign every chapter to one of three tiers based on relevance to the stated goal:

| Tier | Label | Meaning |
|------|-------|---------|
| 1 | Core | Read in full, in this order. Most directly feeds the goal |
| 2 | Important | Read after Core. Focus on ★ sections |
| 3 | Reference | Check specific sections only. Read freely if interested |

**Prioritization principles:**
- Tier 1: chapters that contain the equations, mechanisms, or empirical values the user explicitly needs.
- Tier 2: chapters that provide necessary background or adjacent tools.
- Tier 3: chapters that are peripheral to the stated goal but worth knowing.

**Never label a chapter "skip".** Use "Reference" and note what to check.
Include a note in the preamble that tiers set reading order and focus, not permission.

If the user says they find the whole book interesting and don't want to skip:
acknowledge this in the tier note and make the tier descriptions feel like a reading
sequence, not a filter.

**Order within Tier 1:** sequence chapters so that earlier ones provide vocabulary
or tools used by later ones (for example, definitions before mechanisms before
whole-system behavior).

---

## Step 3: Build the project context preamble

Write a preamble section that appears before all chapters. It should contain:

**A. The claim box** (dark background, stands out).
One or two sentences stating what the user is trying to show. Use their exact framing
where possible. Name the key variable or prediction if one exists.

**B. Two columns:**
- Left: "What you are trying to show" with 3 to 4 numbered points
- Right: "What this material gives you" with 3 to 4 numbered points specific to this book/paper

**C. Three standing questions** (green box).
Questions to carry through every chapter. Not comprehension questions, but extraction
targets. Derive these from the user's stated goal in Step 1. They should be specific
to the user's field and project, not generic.

Examples by field (use as templates, not defaults):
- Quantitative / theoretical: (1) What is the constraint inequality, written as an
  equation? (2) What is the scaling relationship and what does the exponent reveal?
  (3) Does the author make the feasible region explicit, or only gesture at it?
- Experimental / empirical: (1) What is the controlled comparison? (2) What numerical
  values can I extract for parameter X? (3) What confound is most threatening to the
  claim?
- Humanities / conceptual: (1) What is the author's core claim and its scope?
  (2) What counter-example would the author have to address? (3) What concept here
  connects to my own argument?

For non-research reading, replace with three questions appropriate to the register
(for fiction: character, world, theme; for personal development: claim, evidence,
application).

**D. Tier note.** One sentence reminding the user that tiers set focus, not reading permission.

---

## Step 4: Write section-level checkboxes

For each chapter, list every sub-topic from the TOC as an individual checkbox item.

- Use a 2-column grid layout (fits more on a printed page).
- Mark sub-topics most directly relevant to the stated goal with ★ (bold + star).
- Do NOT invent sub-topics. Only use what appears in the TOC.
- If the TOC is sparse (no sub-topics listed), leave the chapter as a single checkbox
  and note: "No sub-topics in TOC, read and add your own".
- If the user is partway through a chapter, add an "In Progress" badge to that chapter header.

---

## Step 5: Write guided questions

Write 3 to 5 guided questions per chapter. These are NOT generic comprehension questions.
They must be:

**For research / academic reading:**
- Specific to the user's stated goal (reference their model, variables, or claim).
- Framed as extraction tasks. Examples: "Write down the equation for X", "Does the
  author give a quantitative value for Y, if so record it", "What constraint does Z
  bound?", "How does the author operationalize concept W?".
- Each question should yield something the user can put directly into their model, paper, or notes.

**For general / recreational reading:**
- Chapter-appropriate: plot, themes, character, world-building for fiction;
  argument, evidence, application for nonfiction.
- Personal: connect to why the user said they're reading it.

**Never ask:** "What did you learn about X?" or "Summarize section Y." These are
comprehension checks, not extraction tasks.

---

## Step 6: Generate the HTML file

Output a single self-contained HTML file. Save it to the output directory configured
above (default `~/reading_guides/`):

```
<output-directory>/<ShortTitle>_guide.html
```

If the directory does not exist, create it. Do NOT save to the Desktop unless the user
explicitly requests it.

Naming convention: `<AuthorLastName>_<ShortTitle>_guide.html`
Generic examples: `<author>_<title>_guide.html`, `<firstauthor><year>_guide.html`.

**Required HTML structure:**

```
<header>  Book title, author, year, ISBN/DOI
<project-context>  Preamble (claim box, two columns, standing questions, tier note)
<priority-key>  Core / Important / Reference legend + ★ explanation
<tier-core>
  <tier-label>
  <chapter> × N  (ch-header + subtopics grid + questions box)
<tier-imp>
  <tier-label>
  <chapter> × N
<tier-skim>
  <tier-label>
  <chapter> × N
```

**CSS requirements:**
- Print-ready: `@media print` block that renders checkboxes as printed squares
  (`border: 1px solid #333; background: white; -webkit-appearance: none`).
- B&W print-safe: print styles de-colorize backgrounds to grays, preserve border indicators.
- Page break handling: `page-break-inside: avoid` on chapter blocks;
  `page-break-after: always` on the project-context preamble.
- Font: serif (Georgia or Times New Roman) for print readability.
- 2-column grid for sub-topic checkboxes.
- Tier color coding: green (Core) / blue (Important) / gray (Reference).
- ★ items: bold label + gold star via CSS `::after`.
- "In Progress" badge: yellow pill on chapter header.

**Do NOT use:** external CDN links, JavaScript frameworks, pandoc boilerplate,
Bootstrap, jQuery, or any external dependencies. The file must work offline.

---

## Step 7: Report to user

Confirm:
- File path
- Tier breakdown (how many chapters per tier)
- Any TOC sub-topics that were ambiguous or missing
- Any chapters marked In Progress
- Flag if the standing questions needed to be simplified (non-research reading)

One short paragraph or 4 to 5 bullets. Do not repeat the full guide back.

---

## Handling different material types

| Material | TOC source | Adjustments |
|----------|-----------|-------------|
| Book (non-fiction) | TOC pages (images/PDF) | Full chapter + section breakdown |
| Academic paper | Section headers | Fewer checkboxes; questions focus on methods, results, equations |
| Book (fiction/recreation) | Chapter list or part structure | Skip the extraction framing; use a register appropriate to fiction |
| Course reader / collection | Table of contents + syllabus | Group by week or theme, not chapter number |
| Paper collection | Multiple abstracts | One entry per paper; priority = relevance ranking |

---

## Coordination with a notes skill (optional)

This skill generates the reading PLAN. If you also use a notes-taking skill (such as
a `/note` skill) for post-reading notes, the two are complementary:
- This skill, run before or during reading: checklist + extraction questions.
- A notes skill, run after reading: structured note with citation, quotes, connections to your own work.

If you have a configured notes location, the post-reading note typically lives there
(for example, `<your-reading-folder>/sources/`). Adjust to match your own setup.
