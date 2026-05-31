# Lu Lab Research Skills

13 Claude Code skills for the research lifecycle — from paper-reading to grant-writing to adversarial review — plus a generate-and-test harness that fires those reviews automatically. Verb-first naming, shareable across the lab group.

Built by [Mingzhen Lu](https://www.mingzhenlu-lab.com) and the Lu Lab at NYU Environmental Studies.

---

## The Suite

| Skill | What it does | Phase |
|-------|--------------|-------|
| `/update-me` | Warm-up briefing: where we left off, what's next | Start session |
| `/end-session` | Capture reusable learnings to memory before `/clear` | End session |
| `/read-ken` | Paper → pop-science summary (built on [Kangning Huang](https://knhuang.weebly.com)'s prompt) | Literature |
| `/trace-origin` | Trace a paper's deepest intellectual roots | Literature |
| `/review-landscape` | Field reconnaissance: 8-dimension landscape map + gap table ranked by your research pillars | Literature |
| `/check-facts` | Verify empirical claims via web search, insert source URLs | Quality |
| `/manage-refs` | DOI-verified citations: CrossRef resolve, `refs.bib`, validate pools | Quality |
| `/visualize-blackbox` | Design diagnostic figures so outsiders can evaluate the analysis | Analysis |
| `/roast-figure` | Adversarial figure QA: legend swaps, color errors, axis failures, arithmetic — caught before anyone sees it | Analysis |
| `/launch-project` | Scaffold a new research project: `method.md` + `agenda.md` + Big 5 structure | Start project |
| `/find-redflag` | Adversarial review: find what Reviewer #2 would attack | Quality |
| `/abt-narrative-critique` | Evaluate proposals/papers using And-But-Therefore storytelling framework (Olson) | Quality |
| `/abt-narrative-critique-zh` | ABT叙事结构评估工具 — Chinese-language variant for NSFC proposals and Chinese journals | Quality |

---

## Dependency Map

```
Session lifecycle:
  launch-project ──→ update-me ──→ [work] ──→ end-session

Literature pipeline:
  review-landscape ──→ read-ken ──→ trace-origin (enrichment layer)

Quality pipeline:
  check-facts ──→ manage-refs ──→ find-redflag
  abt-narrative-critique (standalone, or after drafting intro/abstract)

Analysis:
  visualize-blackbox ──→ [generate figures] ──→ roast-figure
```

---

## Workflows

Beyond the slash-command skills, the repo ships a **harness** — automation that wires the skills together.

| Workflow | What it does |
|----------|--------------|
| [`generate-and-test`](workflows/generate-and-test/) | Git hooks that auto-fire the right review skill (`/code-review`, `/find-redflag`, `/check-facts`, `/roast-figure`) the moment an AI writes code, prose, or a figure — and block `git commit` until each artifact has been reviewed. Quality becomes a reflex, not a thing you remember. |

Install separately (after the skills): `cd workflows/generate-and-test && ./install.sh`

---

## Install

Requires [Claude Code](https://claude.com/claude-code) installed.

### Option 1: Symlink (recommended — auto-updates on `git pull`)

```bash
git clone https://github.com/MingzhenLu/lulab-research-skills.git
cd lulab-research-skills
./scripts/install.sh
```

The script symlinks each skill folder into `~/.claude/skills/`. Running `git pull` later updates all skills in place.

### Option 2: Copy (no auto-update)

```bash
cp -R skills/* ~/.claude/skills/
```

### Verify

Open Claude Code and type `/` — you should see the 11 skills listed.

---

## Uninstall

```bash
./scripts/uninstall.sh
```

Removes only the symlinks this repo created. Leaves other skills in `~/.claude/skills/` untouched.

---

## For Lab Members: Getting Started

1. Install Claude Code CLI: https://claude.com/claude-code
2. Install this suite (see above)
3. Start every work session with `/update-me`, end with `/end-session`
4. When reading a paper: `/read-ken` first, then `/trace-origin` if you want to dig deeper
5. Before submitting anything: `/check-facts` → `/manage-refs` → `/find-redflag`

---

## Design Principles

**Verb-first naming.** Every skill starts with a verb (update, end, read, trace, check, manage, visualize, launch, find). Makes the action clear and the suite recognizable.

**Composable, not monolithic.** Each skill does one thing. The pipelines (literature, quality, session) chain them via dependency.

**Written for autonomy.** Skills get pre-granted tool permissions so they execute without constant "may I?" interruptions. Trust the workflow DNA; let the compiled protein run.

---

## Contributing

PRs welcome from lab members. To propose a new skill:

1. Fork, add `skills/<verb-noun>/SKILL.md`
2. Follow the verb-first naming convention
3. Include a `description:` YAML field — this is what the LLM uses to decide when to invoke
4. Open a PR with a one-paragraph motivation

---

## Acknowledgments

`/review-landscape` is a **fork** of the `scholar-lit-review` skill in **[open-scholar-skill](https://github.com/joshzyj/open-scholar-skill)** by **Yongjun Zhang** ([@joshzyj](https://github.com/joshzyj)). Its 8-dimension landscape-map framework and search→map→verify pipeline are his; the Lu Lab retargeted the domains, swapped in a comparative-advantage gap ranking, and limited it to scouting. Kept under his **Open Scholar Skill License (Academic Use)** — see [`skills/review-landscape/NOTICE`](skills/review-landscape/NOTICE). Thank you, Yongjun.

`/read-ken` is built on a science-writing prompt developed by **[Kangning Huang](https://knhuang.weebly.com)** — the "Ken" the skill is named for. His "ladder-building" approach (start from what the reader knows, then build up step by step) is the method; this suite compiles it into a repeatable workflow. Thank you, Ken.

`/abt-narrative-critique` and `/abt-narrative-critique-zh` apply the And-But-Therefore storytelling framework from Randy Olson's *Houston, We Have a Narrative* to evaluate scientific writing. Originally developed in **[Kangning Huang](https://knhuang.weebly.com)**'s [science_narrative_skills](https://github.com/kangning-huang/science_narrative_skills) repo and merged here to consolidate all research skills in one suite.

---

## License

MIT — **except** `skills/review-landscape/`, which is adapted from open-scholar-skill (Yongjun Zhang) and remains under its **Open Scholar Skill License (Academic Use)**: free for academic, educational, and non-commercial research; commercial use requires the upstream author's written permission. See [`skills/review-landscape/NOTICE`](skills/review-landscape/NOTICE).
