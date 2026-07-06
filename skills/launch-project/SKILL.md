---
name: launch-project
description: "Scaffold a new research project: creates method.md, agenda.md, CLAUDE.md, and AGENTS.md with standard Big 5 folder structure. CLAUDE.md/AGENTS.md embed the lab's truth-over-harmony, coding-discipline, and research-integrity guardrails. Removes the friction of starting from scratch every time."
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "AskUserQuestion"]
user-invocable: true
---

# Launch-Project: Research Project Scaffolding

**Usage**: `/launch-project` or `/launch-project /path/to/new/project`

**Purpose**: Set up a new research project with the standard Lu Lab scaffold so you can start working immediately instead of creating boilerplate files.

## Phase 1: Gather Project Info

Ask the user (one prompt, not multiple):

1. **Project name** — short, descriptive (e.g., "UrbanRoots", "WasteScaling")
2. **Project type** — code | write | analysis (determines which folders matter)
3. **One-sentence description** — what is this project about?
4. **Path** — where to create it. Ask the user; suggest a sensible default if they have a project parent directory configured.

If a path was provided in the invocation, skip the path question.

## Phase 2: Create Folder Structure

### Big 5 (always created)
```
ProjectName/
├── scripts/      # Code, analysis scripts
├── figures/      # Visualizations, plots
├── data/         # Input data, intermediate outputs
├── docs/         # Documentation, references
└── archive/      # Old versions, deprecated files
```

### For code/analysis projects, also create:
```
├── method.md     # Approach, decisions, technical details
└── agenda.md     # Task tracking (from template)
```

### For write projects, also create:
```
├── drafts/       # Working drafts
└── agenda.md     # Task tracking (from template)
```

## Phase 3: Generate agenda.md

Use the standard template:

```markdown
# [Project Name] — Agenda

> [One-sentence description]

## DEADLINES

- [ ] **DAILY**: [leave blank for user]

---

### Week of [current week]

---

## TASKS
- [ ] [First task — user fills in]

## DONE

## WORK LOG
```

Run `date` to get the current week header correct.

## Phase 4: Generate method.md (code/analysis only)

```markdown
# [Project Name] — Method

## Objective
[One-sentence description from Phase 1]

## Approach
[To be filled]

## Data
| Source | Description | Path |
|--------|-------------|------|

## Key Decisions
| Date | Decision | Rationale |
|------|----------|-----------|

## Dependencies
- Python 3.x
- [To be filled]
```

## Phase 5: Generate CLAUDE.md and AGENTS.md

Both files guide whichever AI agent works in this project (Claude Code reads `CLAUDE.md`; other agent tools read `AGENTS.md`). They are full duplicates of each other — same content, two filenames — so keep them in sync if either is edited later.

Each file has two parts: a **project-specific header** (from Phase 1/2) and a **fixed guardrails block** (verbatim every time, not user-customized).

### Project-specific header

```markdown
# [Project Name]

## What This Project Does
[One-sentence description]

## Quick Start
1. Run `/update-me` to see current state
2. Check `agenda.md` for active tasks
3. [Project-specific instructions — user fills in]

## File Structure
[Auto-generated from Phase 2]

## Conventions
- Follow user-level CLAUDE.md conventions (if one exists at `~/.claude/CLAUDE.md`)
- agenda.md is the single source of truth for project state
- method.md tracks technical decisions (co-update with agenda.md)
```

### Guardrails block (append verbatim to both files, after the header)

```markdown
## Core Principle: Truth Over Harmony

Good research demands truth-seeking, not social harmony. Humans are social animals, not truth-seeking animals, and AI assistants are trained to be agreeable — both failure modes must be resisted here.

- If my logic is wrong, say so directly.
- If my interpretation conflicts with the data, side with the data.
- Do not flatter, hedge, or treat my seniority as evidence I am correct.
- I will push back on your reasoning just as hard. That is not conflict — it is how we arrive at something true.

## Coding Principles

These four principles reduce common LLM coding mistakes. They bias toward caution over speed; for trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify. (Note: this rule applies to *code*, not to documenting analytical decisions in `docs/method.md` — see DNA-Protein Rule below.)

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

Test: every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Run the analysis" → "Match expected output ranges, then check across scenarios"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## The DNA-Protein Rule

- **`docs/method.md`** = DNA: documents every analytical decision, data transformation, parameter choice, and rationale. You should be able to regenerate any script from `method.md` alone.
- **`scripts/`** = Protein: executable code that implements `method.md`. Expendable and replaceable.
- **Co-update rule**: when you write or modify a script, update `method.md` in the same action. Code without an updated `method.md` is rejected.

## Research Integrity

Every number that appears in a paper or report must satisfy one of two conditions:

1. It was produced by analysis code in `scripts/` operating on data in `data/`, with the result written to `data/` or `figures/`; **or**
2. It was cited from a source recorded in `docs/`'s references.

**Never fabricate, mock up, or estimate placeholder numbers.** If a number isn't available yet, leave a clearly marked `[TK]` placeholder and flag it — do not invent. If asked to "just put something there for now," refuse and explain why. (`TEST_MODE=true` synthetic data is for code testing only and must never reach the paper.)

## Manuscript Markdown ↔ LaTeX Co-Update Rule

*(Applies once the project has a manuscript draft — e.g. `write`-type projects with files in `drafts/`.)*

The manuscript has two parallel files that must stay synchronized:

- **`drafts/[project-name]_manuscript.md`** — Markdown version for editing in Typora
- **`drafts/[project-name]_manuscript.tex`** — LaTeX version for compilation

**Co-update rule**: When either file is edited, immediately update the other to match. The markdown is the human-editable source; the LaTeX is the compilable output.

Key conversion notes:

- Math: Markdown uses `$...$` inline / `$$...$$` display (Typora-compatible); LaTeX uses `\(...\)` / `\[...\]` or `$...$`
- Figures: Markdown uses `![caption](path)`; LaTeX uses `\includegraphics` with `\caption`
- Tables: Markdown tables are simpler; LaTeX tables preserve precise formatting
- Citations: Markdown uses `<!-- TODO manage-refs -->` comments; LaTeX uses `\cite{}`
- Subscripts: Markdown uses `~text~` (Typora); LaTeX uses `_{text}`
```

## Phase 6: Register and Connect

1. **Git init** (if not already in a git repo):
   ```bash
   git init
   git add .
   git commit -m "Initial scaffold via launch-project"
   ```

2. **Suggest add-dir**: Tell the user to run `add-dir [path]` to connect this project to Claude Code's working directories.

## Phase 7: Confirm

Output a brief summary:
```
Project scaffolded: [ProjectName]
  Path: [full path]
  Type: [code/write/analysis]
  Files: agenda.md, method.md, CLAUDE.md, AGENTS.md
  Folders: scripts/, figures/, data/, docs/, archive/
  
  Next: add-dir [path] to connect, then start working.
```

## Design Principles

- **Minimum viable scaffold**: Create just enough structure to start. The user fills in details.
- **No empty ceremony**: Don't create files that won't be used (e.g., no method.md for pure writing projects).
- **Convention over configuration**: Use the same structure every time so muscle memory builds.
- **agenda.md first**: The task tracker is always the first file to populate.
- **Guardrails are non-negotiable**: The Phase 5 guardrails block (Truth Over Harmony, Coding Principles, DNA-Protein Rule, Research Integrity, Manuscript Co-Update Rule) is fixed text, not a template for the user to customize — only the header above it varies per project.

## Integration

- After launch: use `/update-me` to resume work
- During work: agenda.md tracks progress, method.md tracks decisions
- End of session: `/end-session` captures learnings
