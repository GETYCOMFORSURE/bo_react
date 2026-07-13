# ReactOpt — "Should you keep screening this space?"

An AI-native reaction discovery engine that estimates whether a parameter
space has a ceiling worth chasing — not just a faster BO.

**Total core: ~42–50 hours of focused work**

Tags: 🤖 = safe to vibe code (boilerplate/infra) | 🧠 = write it myself

## 1. Setup & data foundation — ~5–7 hrs 🤖

- Repo scaffolding, environment (Python, PyTorch, RDKit, BoTorch/GPyTorch), clean structure — 1 hr
- Load a public HTE dataset (Doyle/Dreher Buchwald–Hartwig, or Perera Suzuki) — 1.5 hrs
- EDA: yield distributions, missing values, understand the search space — 1.5 hrs
- Define the search space object (categorical: catalyst/ligand/base/solvent; continuous: temp/conc/time) — 1.5 hrs

## 2. Molecular featurization — ~5–6 hrs 🤖

- RDKit: parse SMILES for catalysts/ligands, generate Morgan fingerprints + descriptors — 2.5 hrs
- Encoding for mixed categorical/continuous inputs (one-hot vs. fingerprint-based) — 2 hrs
- Sanity checks + a small featurization test — 1 hr

## 3. Baselines & simulation harness — ~5–6 hrs 🤖

- Closed-loop simulator that queries the dataset as if running experiments — 2.5 hrs
- Random search + grid/exhaustive search baselines — 1.5 hrs
- Metrics + logging (best-yield-so-far, experiments-to-target), multi-seed support — 2 hrs

## 4. Bayesian optimization core — ~10–12 hrs 🧠

- GP surrogate (BoTorch/GPyTorch, or from-scratch for extra credibility) — 4 hrs
- Acquisition functions: EI + UCB, with the ask–tell loop — 3 hrs
- Mixed-variable / molecular kernel (e.g., Tanimoto over fingerprints) — 3 hrs
- Debugging + tuning the loop — 2 hrs

## 5. Ceiling detection — the differentiator — ~8–10 hrs 🧠

- Posterior over the max: sample functions from the GP posterior, take the max of
  each → distribution over the achievable ceiling, with uncertainty — 4 hrs
- "Stop / keep going" decision rule: report the posterior ceiling estimate +
  credible interval each step; flag when the ceiling is confidently below a
  useful threshold — 2.5 hrs
- Calibration check: on datasets with a known true max, does the ceiling
  estimate converge, and is the uncertainty honest? — 2.5 hrs

## 6. Benchmark experiments & the headline plot — ~4–5 hrs 🤖

- Run all methods across many seeds, aggregate — 2 hrs
- Headline chart: posterior estimate of the space's ceiling (with shrinking
  credible band) vs. experiments, on a low-ceiling space — showing the system
  correctly calls it dead well before exhaustive screening would. Overlay
  true max as a dashed line. — 2 hrs
- Supporting table: experiments-to-confident-ceiling-call — 1 hr

## 7. Write-up & demo — ~5–6 hrs 🤖 (draft) / 🧠 (claims & conclusions)

- README: problem, method, results, reproducibility — 2 hrs
- Short technical blog post: the ceiling insight, headline result, honest
  limitations, "what I'd build next with real wet-lab data" — 2 hrs
- 2-minute Loom demo — 1.5 hrs

## Optional (only if ahead)

- **Transfer-learning teaser** (~4–5 hrs) 🧠: warm-start on one reaction using
  data from a related one — mirrors ReactWise's approach. Demoted from core;
  legitimate as a "what I'd do next."
- **Thin UI** (~4 hrs) 🤖: minimal Streamlit/CLI — pick space → suggested
  experiment → log → repeat.


Nothing here is real until the Doyle dataset loads.
"""
