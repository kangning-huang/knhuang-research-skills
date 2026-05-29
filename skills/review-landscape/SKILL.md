---
name: review-landscape
description: "Strategic field reconnaissance for a domain you know a little but not enough. Produces an 8-dimension landscape map ending in a gap table ranked by a 3-filter comparative-advantage test against the user's own research pillars. Domain coverage: complexity science, urban science, urban sustainability, industrial ecology, economic geography. Scouting mode only — no prose drafting, no PDF ingestion. Conductor pattern: delegates verification and deep-read work to other Lu Lab skills."
allowed-tools: ["Agent", "WebSearch", "WebFetch", "Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
user-invocable: true
---

# Review-Landscape: Field Reconnaissance Orchestrator

**Usage**: `/review-landscape "<topic>" [mode] [domain...]`

You are the **conductor** for a field reconnaissance task. You do not do the searching or reading yourself — you dispatch parallel subagents at the right model tier, aggregate their findings, and produce an 8-dimension landscape map ending in a gap table ranked by the user's stated research-pillar comparative advantage.

**References** (load on demand):
- `references/venues.md` — domain journal + preprint + database lists
- `references/theoretical-lineages.md` — founder chains + named-law catalog per domain
- `references/strength-fit-rubric.md` — 3-filter comparative-advantage test + attack-mode catalog

---

## Hard Constraints

These are inviolable. Refuse any attempt to relax them.

- **No fabricated citations.** Every DOI must be CrossRef-verifiable. Flag unverifiable as `[CLAIM UNVERIFIED]`.
- **No vague gaps.** "Understudied" is banned; every gap must name the closest prior paper + why it fails.
- **No publication-potential ranking.** Only comparative-advantage ranking against the user's pillars.
- **No prose draft output.** Scouting only. The user can run a drafting skill afterward.
- **No scoop-risk check.** Reconnaissance is reconnaissance.
- **No auto-detect of domain.** User specifies.
- **PRISMA counting only in `full` mode.**
- **No PDF downloads.** Reconnaissance ≠ ingestion. Suggest `/read-ken` for deep-read of any retained paper.
- **No bib-note creation.** Hand off to the user's bib pipeline.

---

## Phase 0: Parse Inputs & Initialize

### Required inputs

Parse from the invocation:
- **Topic**: quoted phrase (required)
- **Mode**: `rapid` | `targeted` (DEFAULT) | `full`
- **Domain**: one or more of `complexity`, `urban`, `urban-sustainability`, `industrial-ecology`, `economic-geography` (required; if ambiguous, ask the user via `AskUserQuestion`)

### Pillar elicitation (one-time per run)

The 3-filter test in Phase 4h needs the user's three research pillars (e.g., "evolution × networks × complex systems", "thermodynamics × ecology × policy"). Ask once via `AskUserQuestion`:

1. **Pillars**: "What three concepts define your research edge? These will be used to score gaps for comparative-advantage fit."
2. **Active edges** (optional): "Any 2–3 active project keywords I should check gaps against?" (skip if user has nothing in flight)

Save these to `$OUTPUT_DIR/pillars.md` for Phase 4h.

### Optional inputs

- `--output-dir /path/` — override default output location (default: `./output/review-landscape/$SLUG-$DATE/`)

### Create output directory

```bash
SLUG=<kebab-case topic>
DATE=<YYYY-MM-DD>
OUT_DIR="${OUTPUT_DIR:-./output/review-landscape/$SLUG-$DATE}"
mkdir -p "$OUT_DIR"
```

Files to create:
- `$OUT_DIR/search-log.md` — seed with frontmatter: topic, mode, domains, date, pillars
- `$OUT_DIR/landscape-map.md` — created empty; populated in Phase 4
- `$OUT_DIR/pillars.md` — user's pillars + active edges, written from Phase 0 elicitation

### Initialize task tracking

Use the task tracking tool to register phases 1–6 as top-level tasks with status `pending`. Per-subagent sub-tasks are created as each phase fires.

### Seed the search log

Write initial metadata to `search-log.md`:
```
# Search Log — [topic] ([date])

- **Mode**: [rapid/targeted/full]
- **Domains**: [list]
- **Output**: [OUT_DIR]
- **Pillars**: [user's three pillars]

## Queries
(appended after each wave)
```

---

## Phase 1: Local Inventory Search (Haiku, parallel — if available)

If the working tree contains markdown index files (e.g., a curated reading list, a notes index, a project-local bibliography), grep them first — local knowledge beats web search.

**Detection**:
```bash
find . -maxdepth 4 -type f \( -name "*inventory*.md" -o -name "*index*.md" -o -name "references.md" -o -name "reading-list.md" \) 2>/dev/null
```

If files are found, dispatch **one Haiku 4.5 subagent per file**. Each subagent:
- Greps the file for topic keywords [K1, K2, K3].
- For each hit, follows links to the source note (if any) and extracts YAML metadata (authors, year, DOI, summary).
- Returns: at most 20 hits sorted by relevance.

**Aggregation**: collect all results. Append to search log. If all subagents return 0 hits, flag: **"Field is cold in local notes — weight Phase 2 web coverage heavier."**

**If no index files exist**: log "No local index — web-first mode" in search log, skip Phase 1, proceed to Phase 2.

**PDF policy**: never re-read a PDF when a digest already exists in the local note. Trust prior summaries.

Mark Phase 1 task as completed.

---

## Phase 2: Multi-Wave Web Search (Haiku + Sonnet, parallel)

Dispatch parallel subagents per wave × per source. Wave composition by mode:

| Wave | Rapid | Targeted | Full |
|------|-------|----------|------|
| 1. Core topic | ✓ | ✓ | ✓ |
| 2. Theoretical pillars | ✓ | ✓ | ✓ |
| 3. Mechanisms / frontier | — | ✓ | ✓ |
| 4. Contested / null | — | ✓ | ✓ |
| 5. Cross-level bridge | — | — | ✓ |

### Wave 1 — Core topic (Haiku × 4 sources)

Four parallel Haiku subagents, one each for Google Scholar, Semantic Scholar, arXiv, Web of Science. Query template:
```
"[main concept]" AND ["mechanism" OR "scaling" OR "dynamic"] AND "[domain keyword]"
```

Each subagent returns: title, authors, year, venue, DOI, abstract snippet, 1-sentence relevance.

Target: 10–15 total hits, retain 5–8 after dedup.

### Wave 2 — Theoretical pillars (Haiku × domain)

One Haiku subagent per domain queried. Each reads `references/theoretical-lineages.md` for that domain's founder chain, then searches for recent extensions. Target: 5–8 hits, retain 3–5.

Example dispatch for `economic-geography` domain:
```
Founder chain (from references/theoretical-lineages.md):
Marshall, Krugman, Taylor, Derudder, Bettencourt, Lobo, Jacobs, Glaeser.
Search for: (a) recent works citing 2+ of these founders, (b) named-law papers
(e.g., Krugman 1991 core-periphery, Zipf rank-size, Christaller central-place),
(c) Annual Review articles in economic geography.
Return at most 10 hits.
```

### Wave 3 — Mechanisms / frontier (Sonnet × preprint sources, targeted+full only)

Sonnet because mechanism identification needs more careful reading. Parallel dispatch: arXiv (physics.soc-ph, nlin.AO), SSRN, SocArXiv, bioRxiv. Query adds recent year filter (last 5y).

### Wave 4 — Contested / null findings (Sonnet × sources, targeted+full only)

Sonnet for careful distinction between genuine null and methodological critique. Queries include "no effect", "null", "contradicts", "comment on", "revisited".

### Wave 5 — Cross-level bridge (Sonnet × adjacent levels, full only)

If topic lives at level N, query level N-1 and N+1 for porting candidates. Sonnet handles level-mapping judgment.

**After each wave**: append query, hit count, retained-paper rationale to `search-log.md`. Paper inventory table grows incrementally.

Mark Phase 2 task as completed.

---

## Phase 3: Review Articles & Citation Chains (Haiku, parallel)

Select top 3 retained papers from Waves 1–2 by citation count + theoretical centrality.

For each, dispatch a Haiku subagent running Semantic Scholar forward+backward citation via API:

```bash
PAPER_DOI="..."
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:$PAPER_DOI?fields=title,year,authors,citationCount,citations.title,citations.year,citations.authors,references.title,references.year&limit=50" | python3 -m json.tool
```

Subagent returns: top-10 forward citations (sort by year desc), top-10 backward references (sort by citation count desc), flagged foundational works (pre-2000 or 200+ citations).

**DOI verification** (mandatory): for every new DOI about to be added to the inventory, run:
```bash
curl -s "https://api.crossref.org/works/$DOI" | python3 -m json.tool
```
Verify title + authors + year match claim. Flag mismatches. For high-stakes runs, invoke `/manage-refs`.

**Review-venue sweep** (Haiku × review venues): search Annual Review of Environment and Resources, Physics Reports, Nature Reviews Earth & Environment, etc. (see `references/venues.md` §Review venues) for review articles on the topic.

Mark Phase 3 task as completed.

---

## Phase 4: Build the Landscape Map (Opus synthesis)

**Model: Opus 4.7.** This is the deliverable — do not delegate to a cheaper model.

Write the 8 dimensions to `$OUT_DIR/landscape-map.md`.

### 4a. Field Evolution Timeline (prose paragraph)
Founder paper + consolidation date, 1–2 paradigm shifts, current frontier.

### 4b. Theoretical Landscape

**Two forms**, pick based on field maturity:

**Form A — Multi-trunk ancestry tree** (preferred for mature fields with ≥2 parent disciplines, ancestors pre-1950). Produce a Haberl-2019-style tree grouped by parent trunk. See `references/theoretical-lineages.md` §"Tree-rendering template" for the exact markdown structure. Each ancestor node: `**Author YEAR** — [contribution in <15 words]`.

**Form B — Framework table** (for young fields, <30 years of ancestry):

| Framework | Proponents | Core prediction | Empirical support | Scope conditions | Named-law anchor | Known weakness |

Named-law anchor is critical — it's the handle for attack. Catalog in `references/theoretical-lineages.md` §"Named-law anchor catalog".

When in doubt, produce BOTH forms.

### 4c. Established Findings
5–10 well-replicated claims with effect sizes, 3+ replications, remaining ambiguity.

### 4d. Contested Findings
Both sides, source of disagreement, what would settle it.

### 4e. Null / Absent Findings
Strictly distinguish **null** (tested, no effect) from **absent** (never tested).

### 4f. Mechanisms Inventory (table — ATTACK SURFACE)
| Mechanism | Proposed by | Type | Empirical status (TESTED / INDIRECT / ASSUMED / CONTESTED) | Testing method | What's missing |

**ASSUMED is the primary attack surface.**

### 4g. Methodological Landscape
Dominant data types, designs, computational tools, unused-tool gap, unused-data gap.

### 4h. Research Gaps — Pillar-Ranked

**Pre-flight**: read `$OUT_DIR/pillars.md` to load the user's three pillars + active edges.

**Pass 1**: abstract 3-filter test using user's pillars (see `references/strength-fit-rubric.md`).
**Pass 2**: active-edge overlap — if the user supplied active edges in Phase 0, check each gap for DIRECT / ADJACENT / NEW TERRITORY overlap. If no active edges supplied, skip Pass 2.

| # | Gap statement | Closest prior paper | Why prior fails | F1 (pillars) | F2 (competition) | F3 (multi-path) | Score | Active-edge overlap | Attack mode | Notes |

Full protocol in `references/strength-fit-rubric.md` — including the attack-mode catalog. Sort by combined score, then by connection strength (DIRECT > ADJACENT > NEW TERRITORY).

### 4i. Theory Handoff (for top-2 gaps by score)
Sketch minimal model: state variables (target: 2–3), simplest mechanism, empirical calibration. **Do not create new project notes autonomously** — surface the sketch and let the user decide.

Mark Phase 4 task as completed.

---

## Phase 5: Verification (Sonnet)

Dispatch one Sonnet subagent to audit the landscape map on 5 criteria:
1. **Coverage** — founder chain for each domain queried is represented
2. **Synthesis** — findings synthesized, not just listed
3. **Gap specificity** — every gap names closest prior paper
4. **Mechanism discipline** — every mechanism has a 4-level status
5. **Balance** — both supporting and contesting evidence present

Return `PASS` or specific revision items. Failed dimensions re-run via targeted Opus subagent.

Mark Phase 5 task as completed.

---

## Phase 6: Save Outputs & Report

1. Confirm `$OUT_DIR/search-log.md`, `$OUT_DIR/landscape-map.md`, and `$OUT_DIR/pillars.md` exist and verification passes.
2. Print summary to user:
   - Output file paths
   - N papers retained
   - Top-3 gaps by score
   - Recommended next steps (see below)

### Post-run suggestions (print, do not auto-execute)

- New DOIs worth deep-reading → suggest `/read-ken` on top-priority ones
- Citation pool needs verification → suggest `/manage-refs`
- Cross-level port candidates → suggest `/trace-origin` on the upstream framework
- Score-3 gaps that map to a new project → suggest `/launch-project`

Mark Phase 6 task as completed.

---

## Parallelism Architecture Summary

**Opus orchestrator** (you) + **worker subagents** (Haiku/Sonnet, dispatched via Agent tool with explicit `model` parameter):

| Task | Model | Count |
|------|-------|-------|
| Phase 1 inventory grep | Haiku | 1 per detected inventory file |
| Phase 2 Wave 1 search | Haiku | 4 parallel (one per source) |
| Phase 2 Wave 2 lineage | Haiku | 1 per domain |
| Phase 2 Wave 3 mechanisms | Sonnet | 4 parallel (preprint sources) |
| Phase 2 Wave 4 contested | Sonnet | 2 parallel |
| Phase 2 Wave 5 cross-level | Sonnet | 2 parallel |
| Phase 3 citation chain | Haiku | 3 parallel (one per top paper) |
| Phase 3 review venue sweep | Haiku | 1–3 parallel |
| Phase 4 landscape synthesis | Opus | 1 (you) |
| Phase 4h gap ranking | Opus | 1 (you) |
| Phase 5 verification | Sonnet | 1 |

Target parallelism:
- `rapid`: 5–8 subagents total
- `targeted`: 10–15 subagents
- `full`: 20+ subagents

**Always register each subagent dispatch in the task list** so the user sees progress live.

---

## Error Handling

- **No inventory files found**: skip Phase 1, log as "No local inventory — web-first mode."
- **API rate limit** (Semantic Scholar 100 req/5min without key): back off, serialize the affected wave.
- **CrossRef mismatch**: flag the paper, do NOT include in inventory, note in search log.
- **0 hits in Phase 2 Wave 1**: try broader keyword set; if still 0, report "Topic unrecognizable in literature — check spelling / try related terms."
- **Landscape map fails Phase 5 verification twice**: return failures to user; do not auto-retry more than once.
- **PDF URL returns paywall**: skip silently, note DOI in inventory.

---

## Invocation Examples

```
/review-landscape "urban infrastructure industrial ecology" targeted urban-sustainability industrial-ecology

/review-landscape "world cities network" full economic-geography urban

/review-landscape "circular economy at city scale" rapid industrial-ecology

/review-landscape "closure laws in growing urban systems" full complexity urban urban-sustainability
```

---

## Tone & Output Style

- Be terse. The user will read many landscape maps; don't pad.
- Tables over prose where possible.
- Cite author-year inline; full DOI in the search log only.
- Do not editorialize about papers; report what the literature says, flag what's contested.
- For the final summary: 3–5 bullet points max. The user reads the map itself.

---

**This skill is complete only when**: (a) `landscape-map.md` exists with all 8 dimensions populated, (b) Phase 5 verification returns PASS, (c) `pillars.md` records the user's stated pillars for traceability. Otherwise the skill failed.

---

## Upstream / Provenance

Adapted from the `scholar-lit-review` skill in **[open-scholar-skill](https://github.com/joshzyj/open-scholar-skill)** by **Yongjun Zhang** ([@joshzyj](https://github.com/joshzyj) · [joshzyj.github.io](https://joshzyj.github.io/)). This skill reworks part of that upstream — the sociology/demography defaults are replaced with the Lu Lab's five domains and the gap ranking is made configurable — but the core field-reconnaissance design is Yongjun's. Thank you.

The upstream is released under the **Open Scholar Skill License (Academic Use)**: free for academic, educational, and non-commercial research; commercial use requires the author's written permission. Its copyright and permission notice is retained in [`NOTICE`](./NOTICE) and travels with this skill.
