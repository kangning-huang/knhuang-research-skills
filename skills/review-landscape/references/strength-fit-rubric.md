# Comparative-Advantage Rubric — Personal Pillar Test

For the `/review-landscape` skill. Load when the Opus orchestrator builds Phase 4h (Research Gaps Summary).

The rubric scores each candidate gap on **how well it fits the user's research edge** — not on publication potential. Publication-potential ranking is for funding agencies; this rubric is for personal research selection.

**Two-pass scoring**:
1. **Abstract rubric** — the 3-filter test applied to each gap, using the user's three stated pillars
2. **Active-edge overlap** — optional; runs only if the user supplied active project keywords in Phase 0

A gap that scores 3 on the abstract rubric AND connects to an active edge is **exceptional**. A gap that scores 3 abstractly but doesn't connect to any active edge is still strong — it opens a *new* line of work rather than extending an existing one.

---

## The User's Pillars (read from `$OUT_DIR/pillars.md`)

The Phase 0 elicitation captured the user's three research pillars in `$OUT_DIR/pillars.md`. Load that file before scoring.

The pillars define the user's comparative advantage. A gap is a strong attack target when solving it requires the **triple intersection** of those pillars.

**Common Lu Lab pillar examples** (for orientation; the user defines their own):
- `evolution × networks × complex systems` (theoretical / scaling work)
- `thermodynamics × ecology × urban systems` (metabolism / industrial-ecology work)
- `dynamical systems × empirics × policy` (model-to-application work)
- `field ecology × remote sensing × machine learning` (data-driven ecology)

---

## Pass 1: Abstract 3-Filter Test

### Filter 1: Does the gap touch 2+ of the user's three pillars?

Read the pillar definitions from `$OUT_DIR/pillars.md`. A gap passes Filter 1 when its core mechanism or framing requires combining at least two pillars.

PASS examples (for `evolution × networks × complex systems`):
- "How does network structure co-evolve with adaptive processes in cities?" → all three
- "Scaling laws in urban ecosystem networks" → networks + complex systems
- "Evolution of hierarchical modularity in infrastructure" → all three

FAIL examples (same pillars):
- "How does mutation rate affect adaptation?" → evolution only
- "Community detection in social networks" → networks only
- "Calibrating urban metabolism baseline for Chicago" → none (policy)

The gap fails Filter 1 if only one pillar is touched, regardless of how interesting it is.

### Filter 2: Are others NOT already doing this?

Semantic Scholar query on pillar-intersection + domain, filter last 5 years:
- **< 10 papers** → sparse → PASS
- **10–50 papers** → borderline; PASS if existing work leaves a structural gap
- **> 50 papers** → crowded → FAIL

Red flag: if any high-output researcher (a single PI or lab) has ≥3 papers in the exact intersection in last 3 years, treat the gap as already claimed.

### Filter 3: Does solving this open multiple research paths?

Name 3 plausible follow-up papers. If you can, PASS; if only 1, FAIL. Combinatorial gaps open programs; one-off gaps open a single paper.

---

## Pass 2: Active-Edge Overlap (optional)

Runs only if the user supplied active project keywords in Phase 0 (recorded in `$OUT_DIR/pillars.md` under `active_edges:`).

### Connection check — three levels

For each gap scoring ≥ 2 on Pass 1, assign an active-edge overlap level:

| Level | Criterion | Signal |
|-------|-----------|--------|
| **DIRECT** | Gap extends or validates a specific active project | The gap statement can be rewritten to explicitly test or extend a named active project |
| **ADJACENT** | Gap is in the same theme but is a fresh variant | Same conceptual territory but new angle |
| **NEW TERRITORY** | Gap is genuinely new — no active project is a parent | Opens a new sub-line if pursued; higher risk / higher novelty |

**Annotation format** for each gap in Phase 4h:
```
[Active-edge overlap: DIRECT → "fragility-of-efficiency" project — tests whether the rigidity dark-side manifests at intermediate city sizes]
```

---

## Combined Score Interpretation

| 3-filter score | Active-edge overlap | Meaning |
|---------------|---------------------|---------|
| **3** | DIRECT | Exceptional — extends current active work. Top priority. |
| **3** | ADJACENT | Strong — same theme, new variant. Fast to frame. |
| **3** | NEW TERRITORY | Strong, exploratory — opens a new line. |
| **2** | DIRECT | Moderate — partial fit but reinforces current work. |
| **2** | ADJACENT | Moderate — consider, depending on capacity. |
| **2** | NEW TERRITORY | Defer unless strong external signal (grant fit, collaborator ask). |
| **1** | Any | Hand off to a collaborator whose strength dominates the active pillar. |
| **0** | Any | Not user's zone. Note and skip. |

If Pass 2 is skipped (no active edges supplied), interpret on Pass 1 alone.

---

## Attack Mode Catalog (annotation)

Once a gap is prioritized, *how* to attack it? Annotate each gap with its likely attack mode.

### 1. Minimal Dynamic Model (2–3 ODEs → phenomenon)

Strogatz-aesthetic. Verbal gap → parsimonious coupled-ODE system produces the phenomenon. Best when the gap has a clearly-named upstream law that can be re-derived with one corrected assumption.

### 2. Cross-Level Scaling Port

Framework validated at level N, imported to level N+1 without checking level-N assumptions. Attack = identify the assumption violation, fix with a minimal model.

Reference exemplar: Bettencourt 2007 imports West-Brown-Enquist biological scaling to cities — the "reproduction is automatic" assumption fails when scaled to human demographics.

### 3. Closure Law Correction

Framework treats an open system as closed (or vice versa), hiding a conservation constraint. Attack = restore the closure law and show what changes.

Reference exemplar: Single-compartment urban models that assume closed-city populations; real cities have migration → two-compartment formulation.

### 4. Biology → Social Port Repair

Biological equation used outside biological scope. Surface the hidden biology assumption; show where it breaks.

Reference exemplar: West-Brown-Enquist fractal vasculature → urban infrastructure analogy; breaks when infrastructure isn't fractal-optimized.

### 5. Temporal Dynamization

Static framework + new longitudinal data → show how the static picture obscures dynamics.

Reference exemplar: Urban scaling laws as static cross-sectional → time-resolved city trajectories reveal regime shifts.

### 6. Aggregation / Disaggregation

Phenomenon at macro scale absent at micro (or vice versa). Show the aggregation mechanism, or demonstrate it destroys the phenomenon.

Reference exemplar: Country-level demographic averages that mask within-city heterogeneity.

---

## Output Template for Phase 4h

```markdown
## 4h. Research Gaps — Pillar-Ranked

| # | Gap statement | Closest prior paper | Why prior fails | F1 (pillars) | F2 (competition) | F3 (multi-path) | Score | Active-edge overlap | Attack mode | Notes |
|---|--------------|---------------------|-----------------|--------------|------------------|-----------------|-------|---------------------|-------------|-------|
| 1 | [gap, 1 sentence] | [Author Year venue] | [what prior misses] | ✓ [pillars touched] | ✓ [paper count] | ✓ [3 follow-ups] | **3** | DIRECT → [active project name] | Minimal model | [optional: collaborator suggestion] |
| 2 | ... | ... | ... | ✓ | ✗ 80+ papers | ✓ | 2 | ADJACENT | Temporal dynamization | ... |
| ... |
```

Sort descending by score, then by connection strength (DIRECT > ADJACENT > NEW TERRITORY). Score-3 DIRECT gaps expand into Phase 4i (Theory Handoff) — sketch the minimal model.

---

## Pre-flight Checklist (Opus orchestrator runs before Phase 4h)

1. Read `$OUT_DIR/pillars.md` → load user's three pillars + (optional) active edges
2. Score each gap: Pass 1 filters, then (if active edges supplied) Pass 2 overlap → assign combined tag
3. Output table sorted by combined strength

---

## Do Not Do

- **Do not rank by publication potential.** Comparative-advantage ranking only.
- **Do not use generic rubrics** (novelty × feasibility × impact). Those are for funding agencies, not personal research selection.
- **Do not invent additional filters.** Abstract rubric stays 3 filters; active-edge check stays 3 levels. Simplicity wins.
- **Do not propose creating new project files autonomously.** Score-3 + NEW TERRITORY gaps surface the *need* for a new project; the user decides whether to launch it (suggest `/launch-project`).
