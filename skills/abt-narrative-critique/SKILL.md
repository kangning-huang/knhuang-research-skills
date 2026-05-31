---
name: abt-narrative-critique
description: "Evaluate research proposals and papers using the And-But-Therefore (ABT) storytelling framework from Olson's 'Houston, We Have a Narrative'. Calibrated for environmental science and urban climate research. Use when: (1) User asks to critique or evaluate a research proposal introduction/abstract, (2) User asks to assess whether a paper's framing is compelling for publication, (3) User wants feedback on narrative structure of scientific writing, (4) User mentions ABT framework, Olson, or 'Houston We Have a Narrative'. Provides qualitative critique with severity assessment (fatal vs. improvable), citation verification, and constructive suggestions."
---

# ABT Narrative Critique

Evaluate scientific writing using the And-But-Therefore framework. Focuses on introductions and abstracts of research proposals and papers in environmental/urban science.

## The ABT Framework

Scientific narratives follow: **AND** (context) → **BUT** (tension) → **THEREFORE** (resolution)

- **AND**: Establishes what we know. Cites relevant literature to frame the problem.
- **BUT**: Identifies the critical gap. Creates tension that demands resolution.
- **THEREFORE**: Proposes the solution. Shows how methods/results address the gap.

## Workflow

### 1. Determine Document Type
- **Research proposal**: Forward-looking; "Therefore" focuses on proposed methods and expected contributions
- **Research paper**: Retrospective; "Therefore" includes results and demonstrated impact

See [references/proposal-criteria.md](references/proposal-criteria.md) or [references/paper-criteria.md](references/paper-criteria.md) for type-specific evaluation criteria.

### 2. Extract ABT Components
Parse the introduction/abstract to identify:
- AND section: Background statements, cited literature, established knowledge
- BUT section: Gap statement, tension, "however/but/yet" pivot
- THEREFORE section: Proposed approach, methods justification, expected/demonstrated outcomes

### 3. Evaluate Each Component

#### AND Evaluation
1. **Citation coverage**: Extract all cited works. Search for each using Hugging Face paper search and web search to verify:
   - Citations exist and are from credible sources (peer-reviewed journals, reputable institutions)
   - Cited claims accurately represent source content (no distortion)
   - Coverage is appropriate—neither too sparse (missing key works) nor excessive (unfocused)
2. **Framing quality**: Do citations build a coherent foundation for the research question?

#### BUT Evaluation
1. **Gap clarity**: Is there a clear, specific knowledge gap?
2. **Gap significance**: Why does this gap matter? Consequences for:
   - Scientific field advancement
   - Technology development
   - Policy interventions
   - Societal problems
3. **Logical connection**: Does the gap emerge naturally from the AND section?

#### THEREFORE Evaluation
1. **Method-gap alignment**: Is there a "glove-to-hand" fit between problem and approach?
2. **Feasibility/novelty**: Are methods appropriate and sufficiently innovative?
3. **For papers only**: Do results actually address the stated gap? What are broader implications?

### 4. Verify Citations (Full Retrieval)

For each citation in the AND section:
```
1. Search: Use Hugging Face:paper_search and web_search to locate the paper
2. Fetch: Use web_fetch to retrieve abstract/full text when available
3. Verify: Check that the cited claim matches the source's actual findings
4. Assess: Is this source credible? Peer-reviewed? Recent enough?
```

Flag issues:
- Citation not found or inaccessible
- Claim misrepresents source
- Source is non-peer-reviewed or low credibility
- Key recent literature missing

### 5. Assess Severity

Classify each issue as:
- **Fatal flaw**: Likely to cause rejection; must be addressed (e.g., missing gap statement, methods don't address stated problem, citation misrepresents source)
- **Significant weakness**: Reduces competitiveness but not disqualifying (e.g., gap significance unclear, citations incomplete)
- **Minor issue**: Polish-level improvement (e.g., phrasing, flow)

### 6. Generate Critique

Structure output as:

```
## ABT Narrative Assessment

### Overall Verdict
[One sentence: Strong/Adequate/Weak narrative structure]

### AND (Context & Literature)
[Assessment of framing and citations]
- Severity: [Fatal/Significant/Minor or None]

### BUT (Knowledge Gap)
[Assessment of gap identification and significance]
- Severity: [Fatal/Significant/Minor or None]

### THEREFORE (Resolution)
[Assessment of method-gap fit and implications]
- Severity: [Fatal/Significant/Minor or None]

### Citation Verification
[Summary of citation checks; flag any issues]

### Key Recommendations
**High-level**: [1-2 sentences on most important improvement]

**Specific suggestions**:
1. [Concise, actionable suggestion]
2. [Concise, actionable suggestion]
3. [Concise, actionable suggestion]
```

## Field Calibration: Environmental/Urban Science

When evaluating citation coverage, consider these domain norms:
- Urban climate papers typically cite 20-40 references; introductions draw on 8-15 key works
- Essential literature includes foundational works (Oke, Stewart & Oke LCZ) plus recent advances
- Interdisciplinary framing is valued—connections to public health, energy, planning strengthen the AND
- Methods sections should reference validation studies and data sources

Common fatal flaws in this field:
- Ignoring scale mismatches (e.g., claiming city-level implications from point measurements)
- Citing modeling studies as observational evidence
- Missing recent high-impact papers in rapidly evolving subfields (heat exposure, urban scaling)

## Important Notes

- **Critique only**: Do not rewrite the document. Provide assessment and suggestions.
- **Constructive tone**: Frame feedback to help improve the work, not dismiss it.
- **Acknowledge strengths**: Note what works well alongside areas for improvement.
- **Uncertainty**: If unable to verify a citation, note this rather than assuming incorrectness.
