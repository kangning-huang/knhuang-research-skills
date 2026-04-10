---
name: manage-refs
description: "DOI-verified citation pipeline: resolve DOIs via CrossRef, build refs.bib, validate citation pools. Use when introducing ANY source not already in the Bib folder, or when building reference lists for grants/papers."
tools: Read, Write, Bash, WebFetch, Grep, Glob, mcp__google-scholar__search_google_scholar_key_words, mcp__google-scholar__search_google_scholar_advanced
---

# Citation Management Skill

Verified citation pipeline for note-taking and grant writing. Every citation must be DOI-verified before use. Your local bib folder (if any) is ground truth.

## Protocol

### Step 1: Check Local First
```
Local bib folder = ground truth (skip if you don't have one)
→ Glob your bib folder for *AuthorYear*
→ If found: extract metadata from YAML (already PI-verified)
→ If not found: proceed to Step 2
```

### Step 2: Resolve DOI via CrossRef
```bash
python3 ~/.claude/skills/manage-refs/scripts/doi_to_bibtex.py "10.xxxx/yyyy"
```
- Fetches metadata from `api.crossref.org/works/{DOI}`
- Verifies title + authors + journal match claimed citation
- Outputs BibTeX entry with mandatory `url` field (clickable DOI link)
- Flags mismatches before presenting to user

### Step 3: Search by Title (when DOI unknown)
```bash
python3 ~/.claude/skills/manage-refs/scripts/doi_to_bibtex.py --search "paper title author"
```
- Searches CrossRef by bibliographic query
- Returns top 3 matches for user selection
- Then resolves selected DOI as in Step 2

### Step 4: Validate refs.bib (for grant pipelines)
```bash
python3 ~/.claude/skills/manage-refs/scripts/validate_citations.py refs.bib --check-dois
```
- Parses BibTeX file
- Checks every DOI resolves correctly
- Reports pass/fail per entry

### Step 5: Extract Metadata (DOI / PMID / arXiv)
```bash
python3 ~/.claude/skills/manage-refs/scripts/extract_metadata.py "10.xxxx/yyyy"
python3 ~/.claude/skills/manage-refs/scripts/extract_metadata.py --pmid 12345678
python3 ~/.claude/skills/manage-refs/scripts/extract_metadata.py --arxiv 2301.12345
```

### Step 6: Search Literature

**Primary — Google Scholar MCP** (all disciplines, rate-limited):
```
mcp__google-scholar__search_google_scholar_key_words(query="keyword1 keyword2", num_results=10)
mcp__google-scholar__search_google_scholar_advanced(query="keyword", author="LastName", year_range=["2020","2025"])
```
For each result: extract DOI → run `doi_to_bibtex.py` to verify.

**Secondary — PubMed** (biomedical/life sciences, no rate limit):
```bash
python3 ~/.claude/skills/manage-refs/scripts/search_pubmed.py "keyword1 keyword2" --max 10
```
Use when Scholar is rate-limited, or for ecology/biology papers that PubMed indexes well.

## Output Formats

### Inline Citation (for Idea/Bib notes)
```
- AuthorA, B.C. & AuthorD, E.F. (Year). "Title." *Journal*, Vol(Issue), Pages. [DOI](https://doi.org/XXX)
```

### BibTeX Entry (for grant refs.bib)
```bibtex
@article{author2025,
  author = {Last, First and Last2, First2},
  title = {Full Title},
  journal = {Journal Name},
  year = {2025},
  volume = {1},
  pages = {1--10},
  doi = {10.xxxx/yyyy},
  url = {https://doi.org/10.xxxx/yyyy},
  annote = {Why cited: one-line justification}
}
```

## Key Rules

1. **Local bib = ground truth** — always check your local bib folder before external search
2. **Every DOI must resolve** — if CrossRef returns wrong match, FLAG it
3. **Never guess metadata** — if DOI unresolvable, mark `[UNVERIFIED — PI to confirm]`
4. **Pool-only constraint** (grants) — once refs.bib is built, no downstream phase may add citations without verification
5. **URL-as-verification** — every reference includes clickable DOI link. Fake = broken link.

## Past Errors

- **DOI mismatch caught by CrossRef**: A web search once returned wrong DOI `10.1016/j.tibtech.2004.01.006` for Csete & Doyle (2004) — it resolved to a completely different paper (Vajda & Camacho). Only CrossRef API validation caught the swap. Lesson: never trust a DOI you didn't resolve yourself.
- **Reference-prose disconnection**: When 12+ authors are name-dropped in narrative without parenthetical citations, the reference page ends up disconnected from the prose. Always tie names to bib keys at the point of mention.
