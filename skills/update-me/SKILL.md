---
name: update-me
description: "Project warm-up briefing: reads agenda.md (and CLAUDE.md if present) to summarize recent progress, state where we left off, and flag blockers. Use when restarting work on any coding or writing project."
allowed-tools: ["Read", "Grep", "Bash", "Glob", "AskUserQuestion"]
---

# Project Warm-Up Briefing

**Usage**: `/update-me`

**Purpose**: When returning to a project after time away, get a concise briefing on recent progress, current position, and next steps — without re-reading the full agenda.

**Scope**: Works with any project that has an `agenda.md`. Falls back to git log + file modification times if no agenda exists.

---

## Step 1: Locate Project Context

Run in parallel:

1. **Read `agenda.md`** from the working directory (or search one level up if not found). This is the primary source.
2. **Read `CLAUDE.md`** if present — for project structure, conventions, and any session-start protocol.
3. **Get current date**:
   ```bash
   date "+%Y-%m-%d %A"
   ```
4. **Get recent git activity** (last 10 commits, with dates):
   ```bash
   git log --oneline --date=short --format="%h %ad %s" -10
   ```

**If no `agenda.md` exists**: Fall back to git log + recent file modifications. State this explicitly ("No agenda.md found; reconstructing from git history").

---

## Step 2: Parse the Agenda (Internal Reasoning)

Scan `agenda.md` and build a mental model. Do NOT output this step.

### 2a: Find the Active Workstream

The active workstream is the **topmost section with unchecked `[ ]` items**. Identify:
- The section title and when it started (date in header or first checked item)
- The last checked `[x]` item (= last completed step)
- The first unchecked `[ ]` item (= where we pick up)

### 2b: Extract Recent Progress

From the active workstream and any DONE/WORK LOG sections, identify:
- What was accomplished in the last 1-2 sessions (last 3-5 checked items)
- Key decisions made (look for "Decision:", "Key methodological", "Strategy:", or bold rationale text)
- Any data files or scripts produced (file paths mentioned near completed items)

### 2c: Identify Blockers and Dependencies

- Unchecked items that depend on external input (data downloads, collaborator responses, reviews)
- Items flagged with warnings or questions
- Steps that require the user's judgment (parameter choices, scope decisions, data interpretation)

### 2d: Estimate Staleness

Compare the date of the last completed item against today:
- **< 3 days**: "Picking up where you left off"
- **3-14 days**: "Been a bit — here's where things stand"
- **> 14 days**: "It's been a while — fuller context below"

Adjust briefing verbosity accordingly. More context for staler projects.

---

## Step 3: Output the Briefing

**Target**: Under 300 words. Front-loaded: the single most important "what's next" item first.

**Format**:

```markdown
## [Project Name] — Update ([DATE])

**Next up**: [The specific next step, with enough context to act on it immediately]

**Recent progress** ([N] days since last activity):
- [Completed item 1 — what it achieved]
- [Completed item 2]
- [Key decision: X, because Y]

**Where we are**:
- Active workstream: [name]
- Last completed: [step name/number]
- Next step: [step name/number] — [1-sentence description of what it involves]
- After that: [following step, for lookahead]

**Needs your call** [only if blockers exist]:
- [Decision or blocker, with enough context to decide]

**Project pulse** [only if useful]:
- [Completion fraction of current phase, e.g., "Phase 1: 1/6 steps done"]
- [Any stale branches or forgotten threads worth revisiting]
```

**Output rules**:
1. Sections appear ONLY if they have content. Omit empty sections.
2. Never enumerate all completed items — only the last 3-5 relevant ones.
3. File paths and script names are always included when referencing outputs.
4. Decisions include the "because" — not just what was chosen, but why.
5. "Next up" must be specific enough to start working immediately (include file names, data sources, tools needed).
6. For stale projects (>14 days), add a 1-2 sentence "big picture" reminder of what this workstream is trying to achieve and why.

---

## Step 4: Offer to Proceed

After the briefing, ask:

> Ready to pick up on [next step]? Or want to review/change direction first?

Do NOT automatically start executing the next step. Wait for confirmation. The user may want to adjust priorities, revisit a decision, or work on something else entirely.

---

## Edge Cases

### No agenda.md
Reconstruct from git log: group recent commits by theme, identify the most active area, and present as "best guess" of current work. Suggest creating an agenda.md.

### Everything is checked off
Congratulate briefly. Scan for any "Phase 2" or "AFTER X" sections that are now unblocked. Surface those as candidates.

### Multiple active workstreams
List all unchecked sections with their last activity date. Ask which one to focus on, or brief all if there are 3 or fewer.

### Project has WORK LOG or DONE section
Use these as primary evidence of recent progress — they're more reliable than scanning checked items scattered across the agenda.

### First time on this project
No prior sessions to summarize. Focus on: project purpose (from CLAUDE.md or README), current structure, and the first unchecked item. Suggest reading key files before diving in.
