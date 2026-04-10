---
name: end-session
description: "Lean memory capture before /clear. Scans conversation for reusable patterns, appends max 5 bullet points to project MEMORY.md. Prevents memory bloat."
allowed-tools: ["Read", "Edit", "Write", "Bash", "Grep"]
---

# End Session Skill

**Usage**: `/end-session`

**Purpose**: Extract lean, reusable learnings from the current conversation and append to project MEMORY.md before `/clear`.

**Philosophy**: Memory is expensive (loaded every session). Only patterns with future reusability earn a slot. When in doubt, don't record.

---

## Step 1: Identify Project MEMORY.md

The per-project MEMORY.md path follows Claude Code's convention:

```bash
# Find the current project's memory directory
ls ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null
```

Claude Code stores per-project memory under `~/.claude/projects/<encoded-project-path>/memory/MEMORY.md` — the encoded path is the project's absolute path with `/` replaced by `-`. Use the `ls` command above to find the correct one for the current project.

Read the existing MEMORY.md to understand current contents and avoid duplicates.

---

## Step 1.5: Co-Update (AUTOMATIC, not a prompt)

Before scanning for learnings, check whether scripts were modified but `method.md` or `agenda.md` were not updated in the same session. **If drift is detected, perform the co-update yourself — do NOT ask the user.**

```bash
# Compare modification times: scripts vs method.md/agenda.md
# Look for scripts modified MORE RECENTLY than method.md or agenda.md
stat -f "%m %N" */scripts/*.R */scripts/*.py */method.md agenda.md 2>/dev/null | sort -rn
```

### If scripts were changed but `method.md` was NOT updated:
1. Read the modified script(s) and the current `method.md`
2. Add/update the relevant section in `method.md` documenting: what the script does, inputs, outputs, key decisions
3. Report: "Co-updated method.md for [script name]"

### If scripts were changed but `agenda.md` was NOT updated:
1. Read the relevant section of `agenda.md`
2. Mark completed items with `[x] [YYYY-MM-DD]` and add a one-line result summary
3. If a new script was created, add it as a completed item under the appropriate section
4. Report: "Co-updated agenda.md for [work done]"

**This is not optional.** The co-update rule exists because method.md and agenda.md drift causes future sessions to start with stale context. Fix it now, not later.

---

## Step 2: Scan Conversation for Learnings

Review the entire conversation for these categories (in priority order):

1. **Error patterns** — mistakes made and how they were fixed (highest value)
2. **Workflow shortcuts** — faster ways to do things discovered during session
3. **Tool gotchas** — unexpected behavior from tools, APIs, or commands
4. **Project-specific insights** — structural knowledge about this codebase
5. **Reusable strategies** — approaches that would help in future sessions

**Filter criteria** (MUST pass ALL):
- Will this help in a FUTURE session? (not just this one)
- Is this NOT already documented in CLAUDE.md or project CLAUDE.md?
- Is this NOT obvious or trivially re-discoverable?
- Would forgetting this cause wasted time or repeated errors?

---

## Step 3: Draft Bullets

Write 1-5 bullet points. Each bullet:
- **Max 1 line** (~15 words)
- **Actionable** — tells future-Claude what to DO or AVOID
- **Specific** — includes the actual command, path, or pattern
- **No fluff** — no "I learned that..." or "Remember to..."

**Good examples**:
```
- `node_sync.py` must run AFTER `link_type1_tree.py` (dependency order)
- Squarespace receipts: NOT emailed; must log in → Settings → Billing → Invoices
- Gmail MCP: read Name note FIRST for email, never use web search results
```

**Bad examples** (reject these):
```
- Always double-check things before proceeding  ← too vague
- The agenda.md file is important  ← obvious
- We discussed grant writing today  ← not actionable
```

---

## Step 4: Check for Zero-Value Session

If nothing passes the filter criteria, say:

> "Nothing worth remembering this session. Safe to /clear."

This is the CORRECT outcome for routine sessions. Do not force learnings.

---

## Step 5: Append to MEMORY.md

Group under a topic header (reuse existing headers when possible, create new ones sparingly).

**Format**:
```markdown
## [Topic Name]
- Bullet point here
- Another bullet point
```

**Rules**:
- If a topic header already exists, append under it
- If new topic, create header and append at end of file
- Never duplicate existing bullets (check first!)
- Never delete or modify existing content

---

## Step 6: Confirm

Output:

```
Memory updated (N items). Safe to /clear.
```

If zero items:
```
Nothing worth remembering this session. Safe to /clear.
```

---

## Bloat Prevention Rules

**MEMORY.md is loaded into system prompt every session.** Lines after 200 are truncated. Guard this space fiercely.

- **Max 5 bullets per session** — hard limit
- **Max 200 lines total** — if approaching, consolidate or move older items to topic files
- **Topic files** (e.g., `memory/debugging.md`, `memory/patterns.md`) — for detailed notes that don't need to be in system prompt. Link from MEMORY.md.
- **Quarterly review** — if MEMORY.md > 150 lines, prune items that are now in CLAUDE.md or no longer relevant

---

## Anti-Patterns

- Recording what was DONE (that's the work log's job)
- Recording conversation topics (not actionable)
- Recording things already in CLAUDE.md (duplication)
- Recording one-off facts (e.g., "the meeting is at 3pm")
- Recording obvious things ("use python3 not python")
- Exceeding 5 bullets (discipline > completeness)
