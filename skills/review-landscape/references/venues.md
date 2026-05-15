# Venue Reference — Tier-1 Targets by Domain

For the `/review-landscape` skill. Load when dispatching Wave 1–2 search subagents.

**Note**: sociology/demography journals (ASR, AJS, Demography, Social Forces) are excluded by design — they are the upstream skill's defaults and irrelevant for Lu Lab domains.

---

## General high-tier (all domains)

- *Nature*
- *Science*
- *PNAS* (Proceedings of the National Academy of Sciences)
- *Science Advances*
- *Nature Communications*
- *Nature Reviews* (domain-matched: *Nature Reviews Earth & Environment*, *Nature Reviews Physics*, etc.)

---

## Complexity science

### Journals
- *Physical Review E*
- *Physical Review X (PRX)*
- *Nature Physics*
- *Chaos*
- *Entropy*
- *Journal of Statistical Mechanics: Theory and Experiment*
- *Journal of Complex Networks*
- *EPJ Data Science*
- *Complexity*
- *PLOS Complex Systems*
- *Physica A: Statistical Mechanics and its Applications*

### Preprints
- **arXiv**: `physics.soc-ph` (physics and society), `nlin.AO` (adaptation and self-organizing systems), `q-bio.PE` (populations and evolution), `cs.SI` (social and information networks)

### Conferences
- NetSci (International Conference on Network Science)
- CCS (Conference on Complex Systems)
- ICCS (International Conference on Complex Systems)

---

## Urban science

### Journals
- *Nature Cities*
- *Nature Human Behaviour*
- *npj Urban Sustainability*
- *Environment and Planning B: Urban Analytics and City Science*
- *Journal of Urban Economics*
- *Regional Science and Urban Economics*
- *Urban Studies*
- *Cities*
- *Journal of the Royal Society Interface* (cross-over for scaling / biological-urban analogy work)
- *Computers, Environment and Urban Systems*

### Preprints
- **SSRN** (urban econ section)
- **SocArXiv**

### Databases & conferences
- GaWC (Globalization and World Cities Research Network)
- AAG Annual Meeting

---

## Urban sustainability

### Journals
- *Nature Sustainability*
- *Nature Cities*
- *Nature Energy*
- *Nature Climate Change*
- *Environmental Research Letters (ERL)*
- *One Earth*
- *Environmental Science & Technology*
- *npj Urban Sustainability*
- *Environmental Research: Infrastructure and Sustainability*
- *Global Environmental Change*
- *Sustainable Cities and Society*
- *Building and Environment*
- *Energy and Buildings*

### Preprints
- **SSRN** (env econ section)
- **EarthArXiv** (Earth science preprints)

---

## Industrial ecology

### Journals
- *Journal of Industrial Ecology*
- *Resources, Conservation and Recycling*
- *Environmental Science & Technology*
- *Nature Sustainability*
- *Nature Food* (food-system metabolism)
- *Ecological Economics*
- *Journal of Cleaner Production*
- *Resources, Environment and Sustainability*
- *Environmental Research Letters*
- *Resources Policy*
- *International Journal of Life Cycle Assessment*

### Preprints
- **SSRN** (environmental economics)

### Conferences
- ISIE (International Society for Industrial Ecology) biennial meeting

---

## Economic geography

### Journals
- *Journal of Economic Geography*
- *Regional Studies*
- *Economic Geography*
- *Papers in Regional Science*
- *Journal of Urban Economics* (overlap)
- *Environment and Planning A: Economy and Space*
- *Progress in Human Geography*
- *Regional Science and Urban Economics*
- *Cambridge Journal of Regions, Economy and Society*

### Preprints & working papers
- **SSRN**
- **NBER working papers** (heavy overlap with urban econ + spatial equilibrium work)

---

## Review venues (Phase 3 — consensus mapping)

### Annual Reviews
- *Annual Review of Environment and Resources*
- *Annual Review of Resource Economics*
- *Annual Review of Ecology, Evolution, and Systematics*
- *Annual Review of Condensed Matter Physics* (scaling + complexity cross-over)

### Domain-specific reviews
- *Physics Reports* (complexity, scaling laws, network physics)
- *Reviews of Modern Physics* (physics-side complexity, statistical mechanics)
- *Earth-Science Reviews*
- *Nature Reviews Earth & Environment*
- *Renewable and Sustainable Energy Reviews*
- *Progress in Physical Geography*

---

## Database priorities (Phase 2 subagent routing)

| Database | Primary use | Strength | API |
|----------|-------------|----------|-----|
| **Web of Science** | IE, econ geography, urban sustainability | Coverage of energy/materials journals better than Scopus | Yes (institutional) |
| **Google Scholar** | Citation chains ("Cited by N") | Best coverage of preprints + book chapters | No (scrape-only) |
| **Semantic Scholar** | Programmatic forward+backward citation traversal | Free API, 100 req/5min without key | `api.semanticscholar.org/graph/v1/` |
| **CrossRef** | DOI verification (mandatory before ingestion) | Authoritative metadata | `api.crossref.org/works/` |
| **arXiv** | Complexity preprints (physics.soc-ph, nlin.AO, q-bio.PE) | Open access | Yes |
| **SSRN** | Urban econ, env econ, econ geography preprints | Paywalled downloads but abstracts free | No |
| **SocArXiv** | Urban studies preprints | Open access | Yes |
| **bioRxiv** | Any biology-sourced scaling work | Open access | Yes |
| **EarthArXiv** | Earth science / urban sustainability preprints | Open access | Yes |
| **OpenAlex** | Secondary citation graph (successor to MAG) | Free, no rate limit | `api.openalex.org/works/` |

---

## Query construction patterns

### Basic Boolean template
```
"[main concept]" AND ["mechanism" OR "scaling" OR "dynamic"] AND "[domain keyword]"
```

### Example constructions
```
"urban scaling" AND ("superlinear" OR "sublinear") AND ("infrastructure" OR "innovation")
"industrial symbiosis" AND ("material flow" OR "energy flow") AND "circular economy"
"urban metabolism" AND ("input-output" OR "material flow accounting" OR "MFA")
"agglomeration" AND ("productivity" OR "innovation") AND ("spatial" OR "geography")
"complex systems" AND ("emergence" OR "self-organization") AND ("scaling law" OR "power law")
```

### Synonyms to expand (all domains)
- **scaling** = power law = allometry = dimensional analysis
- **mechanism** = pathway = channel = mediator = process
- **network** = graph = topology = connectivity
- **metabolism** = throughput = flux = material flow = energy flow
- **resilience** = robustness = antifragility = redundancy
- **complexity** = emergence = self-organization = nonlinear dynamics
- **agglomeration** = clustering = concentration = density effects

### Temporal filtering
- Recent frontier: add `after:2022` in Google Scholar; `publicationdate:[2022 TO 2026]` in Web of Science
- Foundational works: search JSTOR or specific founder names
