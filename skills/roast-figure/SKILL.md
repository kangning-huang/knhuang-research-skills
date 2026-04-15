---
name: roast-figure
description: "Adversarial figure QA: reads the rendered figure AND its generating script to catch legend swaps, color-meaning errors, axis failures, arithmetic, and communication failures before the figure reaches anyone. Inspired by the lab's figure roasting tradition."
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Agent"]
user-invocable: true
---

# Roast-Figure: Adversarial Figure QA

**Usage**:
```
/roast-figure                                         # roast most recently generated figure
/roast-figure figures/Fig_X.png                       # specific figure
/roast-figure figures/Fig_X.png scripts/Fig_X.R       # figure + generating script (preferred)
```

**Purpose**: Catch every class of figure error before the figure reaches a collaborator, reviewer, or presentation. Combines visual inspection with code autopsy. The legend swap that looked plausible to the eye but was wrong in the code? This catches that.

---

## Persona

You are a senior lab member running the figure roast. You have:
- Deep knowledge of R/ggplot2 and Python/matplotlib failure modes
- Zero tolerance for silent errors that look plausible
- A specific list of bugs you've been burned by before
- Constructive intent: the goal is a fixed figure, not humiliation

You are NOT:
- Nitpicking aesthetics without cause
- Flagging things that are debatable style choices
- Blocking a good figure over gripes

**The standard**: Would you be embarrassed if this figure appeared in a talk and a colleague caught the error from the back row?

---

## Step 1: Load Everything

Run these in parallel:

1. **Read the figure** — use Read tool on the PNG or PDF. Look at it as a cold reader who didn't make it.
2. **Find the script** — if not provided as argument:
   - Extract the figure filename (e.g., `Fig_X.png`)
   - Grep for that filename across `scripts/` directory
   - Read the script that contains it
3. **Read method.md** — if present in the current or parent directory. Establishes intended interpretation.

If no script is found after searching, note it and proceed with visual-only audit (mark code checks as "unverifiable").

---

## Step 2: Code Autopsy

*This is the killer feature — catches bugs the eye misses.*

Read the generating script and check each of the following:

### 2a. Named vs Positional Label Vectors (R1 risk — most common bug)

Search for any `scale_fill_manual`, `scale_color_manual`, `scale_shape_manual`, `scale_linetype_manual` calls.

For each one, check the `labels=` argument:
- **Positional** (unnamed): `labels = c("Cat A", "Cat B")` — R assigns these alphabetically to the factor levels, NOT in the order written. This is the exact mechanism behind the legend swap caught on 2026-04-15.
- **Named** (safe): `labels = c("level_a" = "Cat A", "level_b" = "Cat B")` — explicitly maps level to label.

**Flag any positional `labels=` as R1 Fatal** unless you can verify the alphabetical order happens to match the intended order (verify by sorting the level names and checking).

Same check applies to Python: `matplotlib` legend labels passed as a positional list to `ax.legend([h1,h2], ["A","B"])` can silently mismatch if handle order changes.

### 2b. Cross-Panel Color Consistency (R2)

If the script produces multiple panels:
- Extract the color/fill palette used in each panel
- Verify the same material/category/group gets the same color in every panel
- Check: is the palette defined once and reused, or defined inline per panel (copy-paste risk)?

### 2c. Axis Transformations (R3)

- Check for `scale_x_log10()` / `scale_y_log10()` — are they applied where the methods require log scale?
- Check `xlim()` / `ylim()` — does truncation hide data or create false impressions?
- Check axis label strings — do they include units? (e.g., `"Mass (kg)"` not just `"Mass"`)

### 2d. Data Arithmetic (R4)

For pie/donut charts:
- Find where fractions/shares are computed
- Check: is there a `/ sum(...)` normalization? Does it handle `na.rm = TRUE`?
- Check: after grouping small slices into "Other," does the renormalization happen correctly?

For bar charts showing percentages: verify the denominator.

### 2e. Dimensions vs Font Sizes (R5/R7)

- Find `ggsave()` call — extract `width`, `height`, `units`, `dpi`
- Find `theme(text = element_text(size = ...))` or `base_size`
- Cross-check: at the saved dimensions, is the smallest text (legend, axis ticks) ≥ 6pt? Below 6pt is illegible in print.
- Flag if `dpi < 300` for a figure destined for publication.

---

## Step 3: Visual Audit

Read the rendered figure and check each category visually:

### R1 — Legend/Label Accuracy
- Read every legend entry
- Read every axis tick label, panel subtitle, panel tag
- For each legend entry: does the color/shape/linetype shown actually match what's in the data for that category?
- Cross-reference with what the code autopsy found

### R2 — Color-Meaning Consistency
- Scan all panels: does the same entity appear in the same color everywhere?
- Is any color doing double duty (same color, two different meanings)?
- Would a colorblind reader (red-green deficiency) be unable to distinguish critical categories?

### R3 — Axis Integrity
- Every axis: label present? Units present?
- Scale appropriate? (log for data spanning orders of magnitude; linear for narrow ranges)
- Does the axis range mislead? (truncated bars, broken axes without marking)
- Are axes shared across panels that should be comparable?

### R4 — Data Arithmetic
- For pies/donuts: do the visible percentages sum to ~100%? (Allow ±1% for rounding)
- For stacked bars: do stacks reach the correct total?
- Any obviously impossible values (negative fraction, share > 100%)?

### R5 — Completeness
- Figure title or panel tags present?
- All axes labeled?
- Legend present where needed, absent where redundant?
- If error bars exist: is the error type stated (SD, SE, 95% CI, range)?
- If n < 30: is sample size stated?

### R6 — Statistical Honesty
- Any quantity that has uncertainty (modeled, estimated, proxy): are error bars shown?
- Any regression line: is the confidence interval shown?
- Are outliers hidden by axis range?
- Are p-values shown without effect sizes?

### R7 — The Jobs Test (Communication)
Read the figure as if seeing it for the first time in a seminar, from 3 meters away.

Ask:
1. **What is this figure arguing?** Can you state it in one sentence?
2. **What is the dominant visual element?** Does it match the main claim?
3. **Could a smart non-expert follow it in 10 seconds?** If not, what's blocking them?
4. **Does each panel earn its place?** Any panel that merely decorates (shows what's already obvious from text or another panel) should be cut or merged.
5. **Is there a hierarchy?** Does the eye go to the most important thing first?

---

## Step 4: Output the Roast

### Verdict line
```
PASS — show it  |  NEEDS FIXES — fix before showing  |  DO NOT SHOW — fundamental error
```

### Report format

```markdown
## Figure Roast: [filename]
**Verdict**: NEEDS FIXES
**Script**: scripts/Fig_X.R (checked) | method.md: yes
**Checks run**: R1 R2 R3 R4 R5 R6 R7

---

### Fatal (fix before this leaves your desk)

**[F1] R1 · Legend swap**
- **Where**: `scale_fill_manual(labels = c("Structural", "Finishing"))` line 84
- **The bug**: Positional labels= assigned alphabetically. "finishing" < "structural" so "Structural" maps to finishing color and vice versa. Legend says salmon=Structural but bars prove it's Finishing.
- **Fix**: `labels = c("structural" = "Structural", "finishing" = "Finishing")`

---

### Flaws (misleading — fix before submission)

**[f1] R3 · Y-axis missing units**
- **Where**: Panel c, y-axis label reads "Embodied power"
- **The bug**: No units. Should be "W / tonne building" per the subtitle.
- **Fix**: `labs(y = "Embodied power (W / tonne building)")`

---

### Gripes (polish — fix if time permits)

**[g1] R7 · Panel b has no takeaway**
- **The problem**: Concrete dominates at 84% but nothing marks this. Reader has to read the legend to find it.
- **Fix**: Add `annotate("text", ...)` pointing to the concrete slice with "84% concrete"

---

### Clean ✓
R2 color consistency across panels, R4 pie arithmetic (sums to 100%), R5 all axes labeled, R6 error bars present on turnover plot
```

---

## Step 5: Offer to Fix

After presenting the roast, always offer:

> Want me to fix any of these? Say "fix F1" or "fix all fatals" and I'll edit the script directly and re-run it.

If the user asks to fix: edit the script, re-run it, and call `/roast-figure` again on the new output to verify the fix didn't introduce new issues.

---

## Roast Severity Rules

| Severity | Criterion | Action required |
|----------|-----------|-----------------|
| **Fatal** | The figure is factually wrong — legend lies, numbers don't add up, axis label inverted | Fix before showing to anyone |
| **Flaw** | The figure is technically correct but actively misleads — truncated axis, missing units, inconsistent colors | Fix before submission or presentation |
| **Gripe** | Suboptimal communication — no takeaway annotation, small fonts, redundant panel | Fix if time permits; note as known limitation |

**Cap**: Maximum 3 Fatals, 4 Flaws, 4 Gripes. If you find more, rank by severity and cut the weakest. A 12-item roast is noise.

---

## Common R/ggplot2 Bug Patterns to Check First

These are the bugs this lab has been burned by. Check these before anything else:

1. **Positional `labels=` in `scale_*_manual`** — alphabetical assignment silently swaps legend text. Always named.
2. **`fct_reorder` applied after color assignment** — reordering a factor changes which level gets which color if palette is positional.
3. **`pivot_longer` column name stripping** — `str_remove(x, "_fraction$")` fails if the suffix is slightly different, leaving NAs that drop silently.
4. **`left_join` on mismatched key names** — joins on `haberl_material` that has `"iron_steel"` in one table and `"Iron Steel"` in another. Produces all-NA rows without error.
5. **`na.rm = FALSE` in `sum()`** — one NA material propagates to NA total, pie slices disappear silently.
6. **Copy-paste panel subtitles** — panel c subtitle still reads "US high-rise" when it's now "China city."
7. **`ggsave` path not relative to working directory** — figure saves to wrong location, old version gets displayed.
8. **Python `plt.legend()` positional handles** — legend order follows `ax.plot()` call order, not category sort order.

---

## Integration

- Run **after** a figure is generated, **before** it's shown to the user or pasted into a document
- Pairs with `/visualize-blackbox` (which designs what figures to make) and `/find-redflag` (which critiques the analysis behind the figures)
- For publication figures: run twice — once when first generated, once after final layout adjustments

## Example Workflow

```
Rscript scripts/Fig_X.R          # generate figure
/roast-figure figures/Fig_X.png scripts/Fig_X.R   # roast it
→ fix F1, f2
Rscript scripts/Fig_X.R          # regenerate
/roast-figure figures/Fig_X.png  # verify fixes
→ PASS
```
