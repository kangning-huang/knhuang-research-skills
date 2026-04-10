---
name: check-facts
description: "Scan writing for empirical claims (statistics, dates, historical facts, government data) and fact-check each via web search. Inserts verified source URLs inline. Distinct from manage-refs (which verifies DOIs). Use when reviewing drafts, grant narratives, blog posts, or any writing with factual claims."
tools: Read, Edit, Glob, Grep, Agent, WebSearch, WebFetch
---

# Check-Facts Skill

Scans prose for empirical claims and verifies each against primary sources. Covers statistics, historical facts, government data, news claims — anything that is NOT an academic citation (use `/manage-refs` for DOIs).

## Scope

| Check | Don't Check |
|-------|-------------|
| Specific numbers (population, dollars, miles, %) | Academic citations (use `/manage-refs`) |
| Historical assertions ("richest city," "largest bankruptcy") | Theoretical claims or hypotheses |
| Named-source data (ASCE, Census, FEMA) | User's own unpublished data |
| Comparative claims ("grew by X%," "declined from Y to Z") | Opinions or framing choices |
| Event details ("zero structural failures in post-2002 homes") | |

## Workflow

### Phase 1: Scan — Identify Claims

Read the target file. Extract every empirical claim that:
1. Contains a **specific number** (population, dollars, miles, percentages, dates)
2. Makes a **historical assertion** ("richest city," "largest bankruptcy," "first to...")
3. References a **named source** without inline citation (ASCE, Census, FEMA)
4. Uses **comparative language** with specifics ("grew by X%," "declined from Y to Z")

Also check for explicit `[ref]` or `[fact-check]` markers left by the user.

**Output**: Numbered list of claims with line numbers. Present to user and ask: "Check all, or a subset?"

### Phase 2: Check — Parallel Subagents

**Launch one Agent per claim (or batch 2-3 related claims).** Each agent must:

1. **WebSearch** 2-3 query variations
2. Find the **primary source** (government report, official statistics, municipal data — not secondary journalism)
3. Extract the **verified number** with **source URL**
4. Compare to the claim: Confirmed / Close / Wrong / Outdated

**Critical**: Every verified fact MUST come with a clickable URL to the primary source.

### Phase 3: Report — Verdict Table with Sources

```markdown
| # | Claim | Verdict | Verified Value | Source |
|---|-------|---------|---------------|--------|
| 1 | "serving 80,000" | WRONG | ~99,000 (2014) | [Census Bureau](https://url) |
| 2 | "$2.6T gap" | OUTDATED | $3.7T (2025) | [ASCE 2025](https://url) |
```

Verdicts:
- **OK**: Accurate as stated
- **CLOSE**: Minor imprecision (<10% off), acceptable with rounding
- **WRONG**: Materially incorrect, must fix
- **OUTDATED**: Was correct but newer data exists
- **UNVERIFIABLE**: Cannot find primary source

### Phase 4: Fix — Insert Corrections WITH Source Links

**This is the critical step.** When fixing a claim:

1. Replace the incorrect number/fact with the verified value
2. **Insert the source URL** right after the corrected claim so the user can click-verify and decide to keep or remove it

**Format for inserted sources** (context-dependent):

For **grant/formal writing** — footnote-style comment that user can later convert:
```
...serving fewer than 100,000 [Source: Census Bureau estimates, https://census.gov/quickfacts/flintcitymichigan]...
```

For **notes/drafts** — inline markdown link:
```
...serving fewer than 100,000 ([Census Bureau](https://census.gov/quickfacts/flintcitymichigan))...
```

For **`[ref]` markers** — replace `[ref]` with the source:
```
BEFORE: ...continued decades of decline[ref].
AFTER:  ...continued decades of decline ([Census 2020](https://url)).
```

**The user decides** whether to keep, convert to a formal citation, or strip the link. The skill's job is to leave the breadcrumb.

3. For CLOSE claims: flag in the report but do not auto-fix. User decides.
4. For OK claims: optionally insert source link if the claim currently has no backing.

## Invocation

```
/check-facts                          # Check current open file
/check-facts path/to/file.md          # Check specific file
/check-facts --fix                    # Check and auto-fix WRONG/OUTDATED with source links
```

## Key Rules

1. **Source URL is mandatory**: No correction without a clickable link. If no URL found, mark UNVERIFIABLE.
2. **Primary over secondary**: Census Bureau > newspaper citing Census. ASCE report > article about ASCE.
3. **Recency**: Always check if newer data exists (e.g., 2025 ASCE vs. 2021).
4. **Parallel subagents**: Use agents for 3+ claims. Never check sequentially.
5. **Minimal prose changes**: Change only the incorrect number/fact + insert source. Do not rewrite.
6. **Fabrication flag**: Suspiciously specific claims with no obvious source → escalate to user.

## Integration

- **`/manage-refs`**: Academic DOI verification. Check-facts handles everything else (statistics, dates, government figures, etc.).
- Run AFTER writing, BEFORE publishing/submitting.

## Past Errors

- **Stale population figures**: A grant 1-pager cited "serving 80,000" using 2020 census data when the relevant crisis year was 2014 (~99,000). Similar trap: round numbers like "1.85M engineered" turned out to be ~1.8M.
- **Outdated industry reports**: ASCE infrastructure cost cited as "$2.6T" was the prior edition; current 2025 figure is $3.7T. Always check whether a newer release exists.
- **Geographic scope conflation**: A claim about "90,000 regional jobs" once conflated a national total with the regional figure. Always check the geographic scope a source's number refers to.
