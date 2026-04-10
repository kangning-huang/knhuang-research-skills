---
name: visualize-blackbox
description: "Brainstorm diagnostic and characteristic figures for an analysis. Designs a visual GUI — single-variable distributions, bivariate relationships, and refined multi-facet views — so an outsider can evaluate the analysis without reading code."
allowed-tools: ["Read", "Grep", "Glob", "Bash", "AskUserQuestion"]
---

# Visualize-Blackbox

**Usage**: `/visualize-blackbox` or `/visualize-blackbox <analysis-name>`

**Purpose**: Before or during an analysis, brainstorm a comprehensive menu of diagnostic and characteristic figures that let someone who didn't write the code evaluate the analysis by looking at the figures alone. Figures are the graphical user interface to the black box.

**When to use**:
- Starting a new analysis — design the figure menu before writing code
- Reviewing a completed analysis — check if the existing figures cover all critical facets
- Handing off work — ensure a collaborator can evaluate without reading scripts

---

## Step 1: Understand the Analysis

Read the relevant materials (run in parallel):

1. **The script(s)** — identify inputs, transformations, and outputs
2. **method.md** — understand the analytical logic and key decisions
3. **agenda.md** — find the analysis section for context on goals and status
4. **Existing figures** — catalog what's already been plotted

From these, extract:
- **Input variables**: What raw data enters the pipeline?
- **Intermediate quantities**: What gets computed along the way?
- **Output variables**: What are the final results? (e.g., regression coefficients, scaling exponents, summary statistics)
- **Key decisions/assumptions**: What parameters were chosen by the analyst? (e.g., data source, time window, threshold values)
- **Grouping structures**: What categorical variables exist? (e.g., treatment vs. control, region, species, year)

---

## Step 2: Generate the Figure Menu

Brainstorm figures across **four levels of complexity**, from simple to refined. Think like a reviewer or collaborator seeing this analysis for the first time.

### Level 1: Single-Variable Distributions (Univariate)
> "What does each key variable look like on its own?"

For every important input, intermediate, and output variable, consider:
- Histogram or density plot — is it normal? log-normal? bimodal? skewed?
- Ranked bar chart — which categories dominate?
- Box plot by group — how does the variable distribute across categories?

**Purpose**: Catch data quality issues, reveal skewness, identify dominant categories. These are the cheapest figures to make and often the most informative.

**Example prompts**:
- What is the distribution of the main outcome variable across all observations?
- Which categories contribute the most to the total signal?
- How is the key parameter distributed across subgroups?

### Level 2: Bivariate Relationships (Pairwise)
> "How do pairs of variables relate to each other?"

For every meaningful pair, consider:
- Scatter plot with regression — the workhorse of scaling analysis
- Ratio plot — how does a ratio (e.g., embodied/operational) change with a continuous variable (e.g., city mass)?
- Stacked bar — composition across ordered categories

**Purpose**: Reveal scaling relationships, identify outliers, test whether assumptions hold.

**Example prompts**:
- How does outcome A compare with outcome B across the sample?
- Does the ratio of two related quantities shift with a third variable?
- How does each component's share of one quantity compare with its share of another?

### Level 3: Conditional/Grouped Relationships (Faceted)
> "Does the relationship change when you condition on a third variable?"

- Faceted scatter by group — same relationship, split by category
- Color-coded scatter — third variable as color or size
- Slope comparison — does the scaling exponent differ across subgroups?

**Purpose**: Test whether a single model is adequate or whether subgroups behave differently. Reveals Simpson's paradox, confounders, and interaction effects.

**Example prompts**:
- Does the slope of the main relationship differ across treatment groups?
- How does a categorical confounder affect the headline result?
- Do the largest and smallest units in the sample behave differently from the average?

### Level 4: Sensitivity and Assumption Checks
> "How fragile are the results to my choices?"

- Parameter sweep — vary one assumption (e.g., a key threshold ±50%) and show how the output changes
- Alternative methods side-by-side — same question answered two ways (e.g., two different estimators or data sources)
- Residual plots — are the residuals from the regression well-behaved?
- Influence diagnostics — which data points have outsized leverage?

**Purpose**: Preempt Reviewer #2's "but what if you used different values?" These figures are the armor of the analysis.

**Example prompts**:
- How sensitive is the headline result to uncertainty in the key parameter?
- Which observations are outliers in the residual plot, and are they explainable?
- What changes if we swap in an alternative data source for the same quantity?

---

## Step 3: Prioritize and Output

### 3a: Filter

Not every figure is worth making. For each candidate, apply this filter:
- **Does it answer a question a reviewer would ask?** If not, cut it.
- **Does it reveal something not obvious from the numbers alone?** If the table suffices, skip the figure.
- **Is there enough data to make it meaningful?** A bar chart of 3 categories isn't illuminating.

### 3b: Classify by Priority

- **Must-have** — figures that would leave a gap if missing. A reviewer would ask "why didn't you show this?"
- **Should-have** — figures that strengthen the analysis but aren't essential
- **Nice-to-have** — figures for exploration or supplementary material

### 3c: Number Every Proposed Figure

**Assign a sequential number (1, 2, 3...) to each proposed figure**, including already-done figures. This lets the user pick and choose by number (e.g., "generate 2, 5, 8" or "cut 12-16"). Numbering is mandatory — an unnumbered list forces the user to re-read descriptions to communicate choices.

### 3d: Output Format

Present the figure menu as a numbered checklist, organized by the four levels. Each entry should be one line specifying:
1. What to plot (variables, axes)
2. Why it matters (what it reveals)
3. Priority tier

**Template**:

```markdown
## Blackbox Illuminator: [Analysis Name]

**Analysis**: [1-sentence description]
**Script(s)**: [file paths]
**Key variables**: [list the ~5-10 most important]

### Level 1: Distributions
1. [ ] **[Figure name]**: [x-axis] distribution. Reveals [what]. [Priority]
2. [ ] **[Figure name]**: [variable] ranked by [grouping]. Reveals [what]. [Priority]

### Level 2: Relationships
3. [ ] **[Figure name]**: [y] vs [x] scatter. Reveals [what]. [Priority]
4. [ ] **[Figure name]**: [ratio] vs [continuous var]. Reveals [what]. [Priority]

### Level 3: Conditional
5. [ ] **[Figure name]**: [y] vs [x] faceted by [group]. Reveals [what]. [Priority]

### Level 4: Sensitivity
6. [ ] **[Figure name]**: [output] under [parameter sweep]. Reveals [what]. [Priority]

### Existing Figures (already done)
7. [x] **[Figure name]**: [what it shows]. Location: [path]
```

---

## Step 4: Ask for Direction

After presenting the menu, ask:

> Which figures should I generate? Or should I add/remove any from the list first?

Do NOT start generating figures automatically. The menu is the deliverable at this stage. The user decides which to produce.

---

## Principles

1. **Figures are the GUI to the analysis.** If someone can't evaluate your work from the figures alone, you haven't made enough figures.
2. **Start from the inputs, not the outputs.** Showing what went IN is often more revealing than what came OUT. A distribution of turnover rates tells you about the assumptions; a scaling plot tells you about the conclusion.
3. **Every assumption deserves a figure.** If you chose a parameter, show what happens when it changes.
4. **Name the question each figure answers.** A figure without a question is decoration.
5. **Cheapest figures first.** Single-variable distributions take 5 minutes and catch 50% of issues. Don't skip them for the sexy multi-panel plot.

---

## Edge Cases

### Analysis hasn't been coded yet
Design the figure menu from the planned methodology (method.md or agenda.md description). The menu becomes a specification for what the script should produce.

### Analysis is mature with many existing figures
Catalog existing figures first. The menu becomes a gap analysis: what facets are NOT yet covered?

### Multiple scripts in a pipeline
Treat each script's outputs as a separate "black box" layer. Figures at each stage, not just the final output.

### User asks for a specific analysis (e.g., `/visualize-blackbox <subanalysis>`)
Scope the menu to that specific subanalysis. Read the relevant scripts and data, not the whole project.
