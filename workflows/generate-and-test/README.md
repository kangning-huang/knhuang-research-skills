# Generate-and-Test Harness

A hook-based harness that makes quality checks **automatic** instead of remembered. When an AI assistant writes an artifact, the harness classifies it and reminds you (or blocks the commit) until the matching review skill has run.

## Philosophy

Newell & Simon's *generate-and-test* is a classic weak method: generate a candidate, test it against the goal. With AI assistance the model is the **generator**; your review skills (`/code-review`, `/find-redflag`, `/check-facts`, `/manage-refs`, `/roast-figure`) are the **test**. The problem was never a missing test — it was that running it depended on remembering. This harness makes the test a **reflex**: the harness fires it, not goodwill.

## The dispatch table (output type → test)

| AI output type | Detected by | Test | Enforced by |
|---|---|---|---|
| **code** | major `.py .R .ipynb .jl .sh` edit (≥ `CODE_REVIEW_MIN_LINES`, default 40) | `/code-review` **immediately** (at edit time) | hook |
| **figure** | `figures/` dir or `*plot*`/`*fig*` scripts | `/roast-figure` | hook |
| **prose** | any other authored `.md`/`.tex` (minus operational files) | `/find-redflag` + `/check-facts` (+ `/manage-refs` if it cites sources) | hook |
| **idea / literature note** *(optional)* | files under `GT_IDEA_DIRS` / `GT_BIB_DIRS` | `/find-redflag` + `/manage-refs` + `/check-facts` | hook |

`/code-review` ships with Claude Code. The other tests are skills in this repo — install the suite first (`../../scripts/install.sh`).

**Exempt from the prose test** (operational, not authored content): `README.md`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`. Add more with `GT_PROSE_EXEMPT`.

The idea/literature rows are **off by default**. Set `GT_IDEA_DIRS` / `GT_BIB_DIRS` (colon-separated path fragments) if you keep a note vault and want notes under those folders routed to the literature checks.

## Two speeds (so it never slows daily work)

A hard gate running 20–40 s skills at every turn-end would make interaction crawl. Generate-and-test does not mean test-every-keystroke; it means **every artifact is tested before it is trusted/shipped**, and the artifact boundary is a **commit**.

- **Reflex layer — every turn, instant, never blocks** (`gt-classify.sh`, PostToolUse): classify the just-written file, append it to the ledger. Pure bash + jq, no LLM.
- **Reminder — turn end, instant** (`gt-stop-gate.sh`, Stop): prints which artifacts still owe a test. Non-blocking → loop-proof.
- **Hard gate — commit time** (`gt-commit-gate.sh`, PreToolUse on `git commit`): blocks the commit until every **staged** artifact's test has run (or an audited skip is logged). Fires once per attempt → loop-proof. Applies to prose/idea/figure — **not code**.
- **Code exception — immediate, threshold-triggered**: code is *not* commit-gated (commits stay fast). A major code change fires a `/code-review` nudge at edit time. Trivial edits are logged silently.

## Files

| File | Role |
|---|---|
| `hooks/gt-classify.sh` | PostToolUse(Edit\|Write): classify + log to ledger |
| `hooks/gt-stop-gate.sh` | Stop: print owed tests (non-blocking) |
| `hooks/gt-commit-gate.sh` | PreToolUse(Bash): block `git commit` until staged artifacts tested |
| `hooks/gt-mark.sh` | mark a path verified / audited-skip (run after a test) |
| `$CLAUDE_PROJECT_DIR/.claude/state/gt_ledger.jsonl` | append-only log; latest entry per path wins |
| `$CLAUDE_PROJECT_DIR/.claude/state/gt_audit.log` | human-readable verified/skip trail |

**Ledger semantics:** each edit appends `status:"pending"`. `gt-mark.sh` appends `status:"verified"|"skipped"`. "Owed" = the *latest* entry for a path is `pending`. Re-editing a verified file appends a new `pending` → it is owed again (re-test after change). This self-terminating condition prevents infinite gating.

## Install

```bash
./install.sh        # copies hooks to ~/.claude/hooks/, wires ~/.claude/settings.json (backed up)
# restart Claude Code
```

Re-running is safe (idempotent). To remove:

```bash
./uninstall.sh
```

## Marking a test done

After you run the required skill on an artifact:

```bash
bash ~/.claude/hooks/gt-mark.sh verified <path>
```

### The audited-skip protocol

Not every test applies (prose with no citations does not need `/manage-refs`). Skips are allowed but **never silent**:

```bash
bash ~/.claude/hooks/gt-mark.sh skip <path> "no empirical claims; manage-refs N/A"
```

Every skip lands in `gt_audit.log` with its reason — visible and reviewable.

## Extending it

Adding an output type = one `elif` in `gt-classify.sh` + one row in the `skill()` map in `gt-stop-gate.sh` and `gt-commit-gate.sh`. That is the whole extension cost.

## Make it stricter (optional)

`gt-stop-gate.sh` is non-blocking by default. To turn the turn-end reminder into a hard block, have it emit `{"decision":"block","reason":...}` — but then add a satisfaction-marker check so a verified file cannot re-block (or it will loop).

## Known limits

- Conversational output (an argument made in chat, never written to a file) has no tool event, so it can't be hook-enforced — only a self-imposed rule covers it.
- The commit gate assumes the project dir is the git root. For a project nested inside a larger repo, adjust the `gitroot` handling in `gt-commit-gate.sh`.
- The per-turn layer is LLM-free; it does not run linters. Add `ruff`/`pyright`/etc. as a fast pre-filter if you want.
