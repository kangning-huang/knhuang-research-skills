---
name: causal-evidence-analyzer
description: Analyze causal relationships by searching for and evaluating scientific evidence. Use when the user asks whether X causes Y, inquires about causal mechanisms, or wants to distinguish causation from correlation. Triggers include questions like "does X cause Y", "is there a causal relationship between", "what's the evidence that X leads to Y", or "causation vs correlation" discussions.
---

# Causal Evidence Analyzer

Evaluate causal claims by searching for scientific evidence and organizing findings by strength of causal inference.

## Evidence Hierarchy

Rank and label all evidence using these levels (strongest to weakest):

| Level | Type | Causal Inference Strength |
|-------|------|---------------------------|
| **1** | Meta-analysis of RCTs | Strongest—synthesizes multiple experiments |
| **2** | Randomized Controlled Trial (RCT) | Strong—random assignment isolates cause |
| **3** | Natural/Quasi-experiment | Moderate—exploits exogenous variation |
| **4** | Regression analysis (observational) | Weak—susceptible to confounding |
| **5** | Expert opinion/Descriptive correlation | Insufficient for causal claims |

## Workflow

### 1. Parse the Causal Question

Identify:
- **Exposure/cause (X)**: The proposed causal factor
- **Outcome (Y)**: The effect being investigated
- **Population**: Who/what is affected (if specified)
- **Mechanism**: Proposed pathway (if specified)

### 2. Search for Evidence

Search for academic/scientific sources using queries like:
- `"X causes Y" meta-analysis`
- `"X" "Y" randomized controlled trial`
- `"X" "Y" causal effect`
- `"X" "Y" systematic review`

Prioritize: peer-reviewed journals, Cochrane reviews, NBER/working papers from reputable institutions, government health agencies (CDC, WHO, NIH).

### 3. Evaluate and Classify Each Source

For each piece of evidence:
1. Identify study design → assign evidence level (1-5)
2. Note sample size and effect magnitude
3. Identify potential confounders acknowledged or unaddressed
4. Note replication status (single study vs. replicated finding)

### 4. Synthesize Findings

Write a prose narrative that:
1. **Leads with the strongest evidence** (Level 1-2 if available)
2. **Explicitly labels each evidence level** inline (e.g., "A Level 1 meta-analysis of 23 RCTs found...")
3. **Identifies key confounders** that complicate causal inference
4. **Notes alternative explanations** (reverse causation, common cause, selection bias)
5. **Distinguishes causation from association** clearly

### 5. State Conclusion with Appropriate Hedging

Use calibrated language based on evidence strength:

| Evidence Available | Appropriate Conclusion Language |
|--------------------|--------------------------------|
| Consistent Level 1-2 evidence | "Strong evidence supports a causal relationship" |
| Level 2-3 with some inconsistency | "Moderate evidence suggests X may cause Y, though..." |
| Only Level 3-4 evidence | "Observational evidence shows association; causation not established" |
| Only Level 5 or conflicting evidence | "Current evidence insufficient to determine causality" |

## Causal Inference Concepts to Apply

**Confounders**: Variables that influence both X and Y, creating spurious association. Always ask: "What third factor could explain this relationship?"

**Reverse causation**: Y might cause X instead. Example: Depression associated with unemployment—but does unemployment cause depression, or does depression cause job loss?

**Selection bias**: Non-random sampling can create apparent relationships. Example: Hospital patients sicker than general population.

**Dose-response**: Stronger evidence if more X → more Y (or less Y if protective).

**Temporality**: Cause must precede effect. Cross-sectional studies cannot establish this.

**Biological/theoretical plausibility**: Is there a credible mechanism? Absence weakens causal claims.

## Output Format

Structure response as prose paragraphs (not bullet lists), including:

1. **Opening**: Restate the causal question and preview the conclusion
2. **Evidence review**: Discuss findings organized from strongest to weakest evidence, with explicit level labels
3. **Confounders and limitations**: Key threats to causal inference
4. **Conclusion**: Calibrated statement on whether causation is established, with appropriate hedging

Always cite sources with enough detail to locate them (authors, year, journal if available).
