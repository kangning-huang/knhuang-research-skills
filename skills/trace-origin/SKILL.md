---
name: trace-origin
description: "Trace a paper's intellectual roots: find the 1-2 deepest knowledge trunks it recombines. Based on the Innovation Depth principle — innovation magnitude scales with recombination depth. Use standalone or as an enrichment layer for /read-ken or any bib-note pipeline."
allowed-tools: ["Read", "WebSearch", "WebFetch", "Grep", "Glob", "Bash", "Agent"]
---

# Trace-Origin: Intellectual Ancestry Tracer

**Usage**: `/trace-origin [PDF path | citation key | paper description]`

**Purpose**: Find the 1-2 deepest intellectual roots (knowledge trunks) that a paper recombines. Not "what does this paper cite?" but "what deep traditions collide here?"

**Theory** (Innovation Depth): Innovation magnitude scales with recombination depth. Leaf recombination → incremental papers. Branch recombination → new subfields. Trunk recombination → paradigm shifts. This skill measures that depth.

---

## Core Metaphor: The Knowledge Tree

```
ROOT        Physics / Mathematics / Philosophy
             │
TRUNK       Information Theory    Evolutionary Biology    Economics
             │                     │                       │
BRANCH      Coding theory         Population genetics     Trade theory
             │                     │                       │
TWIG        Error-correcting      Neutral theory          Gravity models
             │                     │                       │
LEAF        Specific 2024 paper   Specific 2024 paper     Specific 2024 paper
```

**The question**: When a paper recombines ideas, how deep is the last common ancestor of those ideas? A paper fusing two 2020 papers from the same lab = leaf LCA. A paper fusing information theory with evolutionary biology = trunk LCA. The deeper the LCA, the bigger the innovation.

---

## ENFORCED 4-PHASE WORKFLOW

Complete all phases IN ORDER.

---

## Phase 1: Paper Identification

### Case A: PDF path provided
```bash
pdftotext -f 1 -l 3 -layout "[PDF path]" - 2>/dev/null | head -80
```
Extract: title, authors, abstract, and crucially the **introduction's framing** — how do the authors position their contribution?

### Case B: Citation key provided (e.g., "Bettencourt2007")
Ask the user for the PDF, or do a web search for the paper by author + year.

### Case C: Paper description provided
```
WebSearch: "[description] paper [year if known]"
```

### Extract the Paper's Self-Declared Lineage

From the introduction, identify:
- **What fields does the paper claim to bridge?** (explicit interdisciplinary framing)
- **What seminal works does the intro cite?** (not all references — just the ones framing the contribution)
- **What problem framing do they use?** (the metaphor/framework reveals the trunk)

**Output**: 2-4 candidate lineage threads (the paper's own declared ancestry).

---

## Phase 2: Trace Roots Backward (The Dig)

For each candidate lineage thread from Phase 1, trace it backward toward the trunk.

### Step 2a: Identify Seminal Anchors

The paper cites recent work, which cites earlier work, which eventually reaches a seminal anchor — a paper/book/idea that founded or defined a field.

**Strategy**: Use the 2-hop rule.
1. From the paper's key references, pick the 1-2 most foundational (oldest, most cited, most field-defining)
2. Web search those foundational references to find THEIR intellectual origins

```
WebSearch: "[seminal paper/author] intellectual origins influenced by history of [field]"
WebSearch: "[foundational concept] origin history who invented"
```

**🔴 PARALLELIZE**: Launch 2-4 WebSearches simultaneously (one per lineage thread).

### Step 2b: Determine Depth Level

For each lineage thread, classify its depth:

| Depth | Definition | Example |
|-------|-----------|---------|
| **Root** | Foundational discipline (math, physics, philosophy) | Calculus, thermodynamics, logic |
| **Trunk** | Major intellectual tradition (>50 years, >1 field) | Information theory, natural selection, general equilibrium |
| **Branch** | Established subfield (10-50 years) | Urban scaling, neutral ecology, deep learning |
| **Twig** | Active research program (5-15 years) | CD index, transformer architecture |
| **Leaf** | Specific recent contribution (<5 years) | A particular 2024 paper |

**Goal**: Find the deepest divergence point between the paper's lineage threads. That's the innovation depth.

---

## Phase 3: Construct the Root Diagram

### Step 3a: Draw the Ancestry

For each root (1-2, ideally 2), construct a lineage chain:

```
ROOT 1: [Trunk-level tradition]
  └─ [Branch]: [key figure/work, year]
    └─ [Twig]: [more recent development]
      └─ THIS PAPER's contribution from this thread

ROOT 2: [Trunk-level tradition]
  └─ [Branch]: [key figure/work, year]
    └─ [Twig]: [more recent development]
      └─ THIS PAPER's contribution from this thread

RECOMBINATION DEPTH: [Trunk / Branch / Twig / Leaf]
The last common ancestor of Root 1 and Root 2 is at the [X] level.
```

### Step 3b: Name the Innovation Type

Based on recombination depth:

| LCA Depth | Innovation Type | Rarity | Example |
|-----------|----------------|--------|---------|
| Trunk–Trunk | Paradigm shift | Very rare | Darwin (geology × economics → evolution) |
| Trunk–Branch | Field creation | Rare | Bettencourt (physics × urban studies → urban scaling) |
| Branch–Branch | Subfield innovation | Common | Most interdisciplinary papers |
| Twig–Twig | Incremental extension | Very common | Most papers |
| Leaf–Leaf | Replication/refinement | Routine | Follow-up studies |

---

## Phase 4: Output

### Standalone Output (when run as `/trace-origin`)

Present the results as a structured summary:

```markdown
## Intellectual Roots: [Paper Citation]

### Root 1: [Tradition Name]
**Lineage**: [Root] → [Branch] → [Twig] → this paper
**Key ancestor**: [Seminal work/figure]
**What this paper inherits**: [specific concept, method, or framing]

### Root 2: [Tradition Name]
**Lineage**: [Root] → [Branch] → [Twig] → this paper
**Key ancestor**: [Seminal work/figure]
**What this paper inherits**: [specific concept, method, or framing]

### Recombination Analysis
**LCA depth**: [Trunk / Branch / Twig / Leaf]
**Innovation type**: [from table above]
**The recombination**: [1 sentence: what collision of ideas makes this paper possible]
```

### Integration Output (when called from another skill)

Return a compact block to be inserted into the bib note:

```markdown
## Intellectual Roots
- **Root 1**: [Tradition] via [Seminal Work] → [what this paper inherits]
- **Root 2**: [Tradition] via [Seminal Work] → [what this paper inherits]
- **Recombination depth**: [Level] — [1-sentence explanation]
```

---

## Integration Notes (for chaining with other skills)

**Where it fits in `/read-ken`**: After Phase 3 (Field Context). The intellectual roots enrich the "So What?" section with deeper historical grounding.

**Where it fits in any bib-note pipeline**: Between field-context analysis and connection discovery. trace-origin provides the deep ancestry; connection discovery maps to your existing notes.

**How to call from another skill**: Spawn as subagent:
```
Agent: trace-origin analysis
  subagent_type: general-purpose
  prompt: "Run /trace-origin for [paper]. Return the compact integration output block."
```

---

## Examples

### Example: Bettencourt et al. (2007) "Growth, Innovation, Scaling"

**Root 1**: Allometric scaling (biology)
  └─ Kleiber's law (1932): metabolic rate ~ mass^0.75
    └─ West, Brown, Enquist (1997): fractal network theory
      └─ THIS PAPER: applies scaling framework to cities

**Root 2**: Urban economics
  └─ Marshall (1890): agglomeration economies
    └─ Jacobs (1961): diversity drives urban vitality
      └─ THIS PAPER: social network density as mechanism

**LCA depth**: Trunk–Trunk (biology × economics)
**Innovation type**: Field creation (urban scaling as new field)
**The recombination**: What if cities are organisms? Metabolic scaling theory meets agglomeration economics.

---

## Design Philosophy

This skill operationalizes the Innovation Depth principle: every paper has roots, and the depth of those roots tells you the magnitude of the innovation. Most papers are leaf-level recombinations. The ones that matter recombine trunks.

The skill is deliberately lean — it doesn't replace `/read-ken`'s author research or any other skill's connection discovery. It adds one thing: the vertical dimension. Where those skills map the horizontal network (what connects to what), trace-origin maps the vertical ancestry (where does this come from, and how deep?).

## Origin

This skill formalizes a habit Mingzhen learned from Lars Hedin (Princeton ecology). When reading a paper, Lars would ask: where does this idea *really* come from? Not the immediate citation, but the deep root. That habit of digging past the bibliography into the intellectual ancestry is what this skill automates.
