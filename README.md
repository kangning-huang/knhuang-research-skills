# Kangning Huang Research Skills

16 Claude Code skills for the research lifecycle — from paper-reading to grant-writing to adversarial review — plus narrative transformation tools for understanding and communicating science.

Built by [Kangning Huang](https://kangning-huang.github.io/main/). Forked from the [Lu Lab Research Skills](https://github.com/MingzhenLu/lulab-research-skills) by [Mingzhen Lu](https://www.mingzhenlu-lab.com).

---

## The Suite

| Skill | What it does | Phase |
|-------|--------------|-------|
| `/update-me` | Warm-up briefing: where we left off, what's next | Start session |
| `/end-session` | Capture reusable learnings to memory before `/clear` | End session |
| `/read-ken` | Paper → pop-science summary (ladder-building approach) | Literature |
| `/trace-origin` | Trace a paper's deepest intellectual roots | Literature |
| `/review-landscape` | Field reconnaissance: 8-dimension landscape map + gap table ranked by your research pillars | Literature |
| `/gladwell-interpreter` | Transform papers into Gladwell-style narratives — for rapid understanding or public communication | Literature / Communication |
| `/check-facts` | Verify empirical claims via web search, insert source URLs | Quality |
| `/causal-evidence-analyzer` | Evaluate causal claims using evidence hierarchy (RCT → observational) | Quality |
| `/manage-refs` | DOI-verified citations: CrossRef resolve, `refs.bib`, validate pools | Quality |
| `/visualize-blackbox` | Design diagnostic figures so outsiders can evaluate the analysis | Analysis |
| `/roast-figure` | Adversarial figure QA: legend swaps, color errors, axis failures, arithmetic — caught before anyone sees it | Analysis |
| `/launch-project` | Scaffold a new research project: `method.md` + `agenda.md` + Big 5 structure | Start project |
| `/find-redflag` | Adversarial review: find what Reviewer #2 would attack | Quality |
| `/abt-narrative-critique` | Evaluate proposals/papers using And-But-Therefore storytelling framework (Olson) | Quality |
| `/abt-narrative-critique-zh` | ABT叙事结构评估工具 — Chinese-language variant for NSFC proposals and Chinese journals | Quality |
| `/make-reading-guide` | Generate structured reading guides for papers | Literature |
| `/chaining-transitions` | Make prose flow with known-new chaining (each sentence's tail seeds the next sentence's head) — distilled from Ken's NASA proposal | Writing |

---

## Dependency Map

```
Session lifecycle:
  launch-project ──→ update-me ──→ [work] ──→ end-session

Literature pipeline (understanding):
  review-landscape ──→ read-ken ──→ trace-origin
                           │
                           └──→ gladwell-interpreter (rapid deep-dive on new topics)

Quality pipeline:
  check-facts ──┬──→ causal-evidence-analyzer (for causal claims)
                │
                └──→ manage-refs ──→ find-redflag ──→ abt-narrative-critique

Analysis:
  visualize-blackbox ──→ [generate figures] ──→ roast-figure

Communication pipeline (after publication):
  [published paper] ──→ gladwell-interpreter (public article)
                              │
                              └──→ check-facts (verify simplified claims)
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
git clone https://github.com/kangning-huang/knhuang-research-skills.git
cd knhuang-research-skills
./scripts/install.sh
```

The script symlinks each skill folder into `~/.claude/skills/`. Running `git pull` later updates all skills in place.

### Option 2: Copy (no auto-update)

```bash
cp -R skills/* ~/.claude/skills/
```

### Verify

Open Claude Code and type `/` — you should see the 16 skills listed.

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

This repo is forked from **[lulab-research-skills](https://github.com/MingzhenLu/lulab-research-skills)** by **[Mingzhen Lu](https://www.mingzhenlu-lab.com)** and the Lu Lab at NYU Environmental Studies. The original suite's architecture, verb-first naming, and many skills originate there.

`/review-landscape` is a **fork** of the `scholar-lit-review` skill in **[open-scholar-skill](https://github.com/joshzyj/open-scholar-skill)** by **Yongjun Zhang** ([@joshzyj](https://github.com/joshzyj)). Its 8-dimension landscape-map framework and search→map→verify pipeline are his. Kept under his **Open Scholar Skill License (Academic Use)** — see [`skills/review-landscape/NOTICE`](skills/review-landscape/NOTICE).

`/read-ken` uses a "ladder-building" approach (start from what the reader knows, then build up step by step) for science communication.

`/abt-narrative-critique` and `/abt-narrative-critique-zh` apply the And-But-Therefore storytelling framework from Randy Olson's *Houston, We Have a Narrative* to evaluate scientific writing.

`/gladwell-interpreter` transforms academic papers into Malcolm Gladwell-style narratives, useful for (1) rapidly understanding new topics and (2) writing public-facing articles from published research.

`/causal-evidence-analyzer` evaluates causal claims by ranking evidence from meta-analyses of RCTs (strongest) down to observational correlations (weakest), applying core causal inference concepts like confounding, reverse causation, and selection bias.

---

## License

MIT — **except** `skills/review-landscape/`, which is adapted from open-scholar-skill (Yongjun Zhang) and remains under its **Open Scholar Skill License (Academic Use)**: free for academic, educational, and non-commercial research; commercial use requires the upstream author's written permission. See [`skills/review-landscape/NOTICE`](skills/review-landscape/NOTICE).
