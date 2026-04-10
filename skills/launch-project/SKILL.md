---
name: launch-project
description: "Scaffold a new research project: creates method.md, agenda.md, CLAUDE.md with standard Big 5 folder structure. Removes the friction of starting from scratch every time."
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

## Phase 5: Generate CLAUDE.md

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
  Files: agenda.md, method.md, CLAUDE.md
  Folders: scripts/, figures/, data/, docs/, archive/
  
  Next: add-dir [path] to connect, then start working.
```

## Design Principles

- **Minimum viable scaffold**: Create just enough structure to start. The user fills in details.
- **No empty ceremony**: Don't create files that won't be used (e.g., no method.md for pure writing projects).
- **Convention over configuration**: Use the same structure every time so muscle memory builds.
- **agenda.md first**: The task tracker is always the first file to populate.

## Integration

- After launch: use `/update-me` to resume work
- During work: agenda.md tracks progress, method.md tracks decisions
- End of session: `/end-session` captures learnings
