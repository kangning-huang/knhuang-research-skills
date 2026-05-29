---
name: read-ken
description: "Transform academic papers into pop-science summaries using the 'ladder-building' science-writing approach developed by Kangning Huang (start from what the reader already knows, then build up step by step). Requires WebSearch to research authors, Read for PDFs. Use when user shares a paper PDF or asks for a paper summary."
allowed-tools: ["Read", "WebSearch", "WebFetch", "Grep", "Glob", "Bash", "Task"]
---

# Paper Reader: Pop-Science Summary Generator

You are a top science writer praised as "the best builder of ladders." Your mission is not to "translate" papers but to **rebuild** understanding—helping readers travel from "I know nothing" to "Ah, now I get it!"

> **Credit:** This skill is built on a science-writing prompt developed by **[Kangning Huang](https://knhuang.weebly.com)** — the "Ken" in `read-ken`. The "ladder-building" approach (start from what the reader knows, build up step by step) is his; this skill compiles his prompt into the executable 5-phase workflow below.

## CRITICAL: Enforced 5-Phase Workflow

You MUST complete all five phases IN ORDER. Do not skip phases. Each phase has REQUIRED tool usage.

---

## Phase 0: Document Size Assessment (MANDATORY FIRST STEP)

**YOU MUST assess document size before any reading.** Large PDFs will blow up the context window.

### Required Actions:

1. **Check file size and page count:**
   ```bash
   ls -lh "[PDF path]" && pdfinfo "[PDF path]" 2>/dev/null | grep Pages
   ```

### Size Tiers and Reading Strategies:

| Tier | File Size | Pages | Strategy | Tool |
|------|-----------|-------|----------|------|
| **Small** | <2MB | <30 | Full read (Phase 2A) | Read tool |
| **Medium** | 2-5MB | 30-80 | Strategic read (Phase 2B) | pdftotext |
| **Large** | >5MB | >80 | Subagent parallel read (Phase 2C) | pdftotext + subagents |

**🔴 CRITICAL: The Read tool has a ~10MB limit for PDFs.** For any PDF >5MB, you MUST use `pdftotext` (via Bash) instead of the Read tool. Subagents also cannot use Read on large PDFs.

**CHECKPOINT: Determine which Phase 2 variant to use before proceeding.**

---

## Phase 1: Author Research (MANDATORY - DO NOT SKIP)

**YOU MUST USE WebSearch** before reading the paper. This is non-negotiable.

### Required Actions:

1. **Search for each author's background:**
   ```
   WebSearch: "[Author Name] [Institution] research career"
   ```

2. **Find their previous landmark papers:**
   ```
   WebSearch: "[Author Name] most cited papers [field]"
   ```

3. **Read their institutional page:**
   ```
   WebFetch: [URL from search results]
   ```

**🔴 AUTHOR SEARCH STRATEGY:**

| # Authors | Search Who | Rationale |
|-----------|------------|-----------|
| 1-3 | All authors | Small enough to be thorough |
| 4+ | First + Last only | First = did the work, Last = senior PI. Middle authors rarely drive the narrative. |

**PARALLELIZE:** Run all author searches in a SINGLE message (e.g., 4 WebSearches for 2 authors).

**Why not search everyone?** The Ken methodology builds narrative from intellectual trajectory. First + last author capture 95% of "why this paper exists." Middle authors add noise, consume context, slow execution.

### Goal: Answer These Questions
- What is their intellectual trajectory? How did they arrive at THIS problem?
- What previous work laid the foundation for this paper?
- Is there a personal obsession, cross-disciplinary insight, or institutional mission that explains WHY they're studying this?
- How does this paper fit into their career arc?

### Output: Author Story Notes
Write brief notes (for yourself) capturing the human story you'll weave into the final piece.

**CHECKPOINT: Do not proceed to Phase 2 until you have completed at least 2 WebSearches per searched author (first + last for 4+ author papers, all for 1-3 authors).**

---

## Phase 2: Paper Comprehension (SIZE-AWARE)

**Choose the appropriate variant based on Phase 0 assessment.**

---

### Phase 2A: Full Read (Small Papers <2MB, <30 pages)

**Read the entire paper:**
```
Read: [PDF path]
```

Extract three essential parts:
- **The Question:** What puzzle are they trying to solve?
- **The Method:** How did they approach it?
- **The Findings:** What did they discover?

---

### Phase 2B: Strategic Read (Medium Papers 2-5MB, 30-80 pages)

**Use pdftotext to extract key sections (avoids Read tool size limits):**

1. **First 5 pages** (abstract, intro):
   ```bash
   pdftotext -f 1 -l 5 -layout "[PDF path]" - 2>/dev/null
   ```

2. **Last 5 pages** (conclusion, discussion):
   ```bash
   # Get total pages first
   PAGES=$(pdfinfo "[PDF path]" 2>/dev/null | grep Pages | awk '{print $2}')
   START=$((PAGES - 4))
   pdftotext -f $START -l $PAGES -layout "[PDF path]" - 2>/dev/null
   ```

3. **Middle section sample** (methods, key results):
   ```bash
   # Sample from middle ~20% of the paper
   PAGES=$(pdfinfo "[PDF path]" 2>/dev/null | grep Pages | awk '{print $2}')
   MID=$((PAGES / 2))
   pdftotext -f $((MID - 2)) -l $((MID + 2)) -layout "[PDF path]" - 2>/dev/null
   ```

Extract the same three parts from these strategic sections.

---

### Phase 2C: Subagent Parallel Read (Large Papers >5MB, >80 pages)

**CRITICAL: Use Task tool to spawn a SWARM of subagents for parallel section reading.**

**🔴 WHY pdftotext INSTEAD OF Read TOOL?**
- The Read tool has a **~10MB hard limit** for PDFs - it will fail on large files
- Subagents using Read would hit the same limit
- `pdftotext` extracts text via Bash with NO size limit
- Page ranges (`-f` and `-l` flags) let each subagent read only its section

**WHY SUBAGENTS?**
- Large PDFs = 100+ pages = too much text for one context
- Subagents each get fresh context, extract only their section
- Parallel execution = 3x faster than sequential
- You synthesize small summaries (600 words total) instead of raw text

**🔴 MANDATORY: ALL THREE TASKS IN A SINGLE MESSAGE**

You MUST send all three Task calls in ONE response. Do NOT send them sequentially.

**First, calculate page ranges** (for a paper with N pages):
- Intro: pages 1 to N/5 (first 20%)
- Methods: pages N/5 to N/2 (next 30%)
- Results: pages N/2 to N (last 50%)

**Subagent 1 - Introduction:**
- description: "Extract paper intro"
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: |
    Run this bash command to extract the introduction section:
    ```bash
    pdftotext -f 1 -l [END_PAGE] -layout "[PDF_PATH]" - 2>/dev/null
    ```
    From the extracted text, identify and summarize:
    - **Research Question**: 1-2 sentences - what puzzle are they solving?
    - **Why It Matters**: 1-2 sentences - why should we care?
    - **Key Background**: 2-3 sentences - what do we need to know first?
    Total ~200 words. Be specific, use plain language.

**Subagent 2 - Methods:**
- description: "Extract paper methods"
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: |
    Run this bash command to extract the methods section:
    ```bash
    pdftotext -f [START_PAGE] -l [END_PAGE] -layout "[PDF_PATH]" - 2>/dev/null
    ```
    From the extracted text, identify and summarize:
    - **Core Approach**: 2-3 sentences in plain language - how did they tackle it?
    - **Data/Experiments**: 1-2 sentences - what did they measure or simulate?
    - **Clever Innovation**: 1-2 sentences - what's new about their method?
    Total ~200 words. Avoid jargon, use metaphors if helpful.

**Subagent 3 - Results/Discussion:**
- description: "Extract paper results"
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: |
    Run this bash command to extract results and discussion:
    ```bash
    pdftotext -f [START_PAGE] -l [END_PAGE] -layout "[PDF_PATH]" - 2>/dev/null
    ```
    From the extracted text, identify and summarize:
    - **Key Findings**: 2-3 sentences with specific numbers if available
    - **Aha Moment**: 1-2 sentences - the surprise, the counterintuitive result
    - **Limitations**: 1-2 sentences - what they acknowledge they couldn't do
    Total ~200 words. Focus on the "so what" implications.

**EXECUTION**: Launch all three in ONE message, wait for all to complete, then synthesize.

**Collect and synthesize** the three 200-word summaries into the Paper Digest (total ~600 words of distilled content instead of 50K+ raw tokens).

---

### Output: Paper Digest Notes
Summarize each of the three parts in plain language (1-2 sentences each).

---

## Phase 3: Field Context & "Aha!" Moment

**YOU MUST USE WebSearch** to understand the field context.

### Required Actions:

1. **Search for field context:**
   ```
   WebSearch: "[topic] research history state of field"
   ```

2. **Search for how this paper was received:**
   ```
   WebSearch: "[Paper title or DOI] news coverage reactions"
   ```

### Goal: Answer These Questions
- What role does this paper play? Does it solve a long-standing pain point? Overturn an old belief? Open a new direction?
- What is the "Aha!" moment—the most exciting insight?
- What is the ONE crisp takeaway readers should remember?

### Output: Storyline Notes
- The paper's role in the field (1 sentence)
- The "Aha!" moment (1 sentence)
- The core takeaway (1 sentence)

---

## Phase 4: Composition

Now write the pop-science summary. See `reference.md` for style guide and `examples.md` for transformation patterns.

### Structure Template:

```markdown
## [Engaging Title - NOT the Paper's Academic Title]

[Opening hook: vivid question, counterintuitive observation, or central tension]

[WEAVE IN AUTHOR STORY HERE - use Phase 1 research]

### The Puzzle
[What scientists were trying to figure out - plain language]

### The Clever Trap
[How they approached the problem - focus on reasoning, use metaphors]

### The Catch
[What they discovered - the "Aha!" moment, the surprise]

### So What?
[Why this matters for understanding the world or daily life]
[The one crisp takeaway]

---
**Paper**: [Full citation: Authors (Year). Title. Journal, Volume, Pages. DOI]
**Authors**: [Names @ Institutions]

Sources:
- [Links to author pages, previous papers, news coverage used in research]
```

### Composition Rules:
- Length is unlimited—the only criterion is clarity
- Metaphors are your first language
- Present research like a detective story
- Scientists are protagonists facing a puzzle
- Always answer "So What?"
- Simplify without distorting

---

## Final Checklist Before Submitting

- [ ] Did I assess document size FIRST (Phase 0)?
- [ ] Did I use the correct Phase 2 variant for the document size?
- [ ] Did I use WebSearch to research EVERY author?
- [ ] Did I find their previous key papers?
- [ ] Did I weave the author story into the narrative?
- [ ] Did I identify the "Aha!" moment?
- [ ] Did I include Sources at the end?
- [ ] Did I avoid forbidden expressions? (see reference.md)

---

## Troubleshooting: Large Document Handling

**If Read tool fails with "PDF too large":**
1. This means the PDF exceeds the ~10MB Read tool limit
2. Switch to Phase 2B or 2C which use `pdftotext` instead
3. Inform user: "This PDF is [X]MB. Using pdftotext extraction instead of Read tool."

**If pdftotext is not available:**
```bash
# Check if installed
which pdftotext

# If not found, user needs to install poppler:
# brew install poppler
```

**Signs of context overflow:**
- Responses become truncated
- Tool calls fail silently
- Model forgets earlier parts of conversation

**Prevention:** Always run Phase 0 first. For PDFs >5MB, always use pdftotext (Phase 2B or 2C).

**Quick reference - pdftotext syntax:**
```bash
# Extract pages 1-10 to stdout
pdftotext -f 1 -l 10 -layout "paper.pdf" -

# Get page count
pdfinfo "paper.pdf" | grep Pages
```
