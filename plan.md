# Mini Closed-Loop Discovery Engine (Reaction Yield)

*Note: the "test" step is a lookup into a public dataset, not a physically run reaction. This project implements the decision-making layer of a closed discovery loop, with experiments simulated.*

## Summary

An in-silico closed-loop discovery engine on the Buchwald–Hartwig HTE dataset. Each round the system proposes a candidate, "tests" it (dataset lookup as a simulated experiment), learns from the result, and picks the next — reaching near-maximum yield in far fewer experiments than random screening. A small, transparent reproduction of the design–test–analyze loop behind data-driven reaction development.

**Scope:** this demonstrates the decision-making layer of a discovery loop — the "make/test" step is simulated (dataset lookup), not real synthesis.

## Goal

Build a working, fully-understood closed-loop pipeline on a public benchmark, prioritizing clarity and correctness over sophistication.

---

## Project structure

```
discovery_loop/
├── data/               # BHpredict CSV
├── featurize.py        # data loading + featurization
├── gp_model.py          # Gaussian Process surrogate (the "analyze" model)
├── acquisition.py       # Expected Improvement (the "decide what to test next" step)
├── loop.py              # main closed-loop controller
├── baseline.py           # random-search baseline
├── run_experiment.py     # orchestration
├── plot_results.py       # results plotting
└── README.md
```

---

## Build stages (v1 — the loop over a fixed candidate pool)

1. **Data + featurization** — Load CSV, inspect columns, one-hot encode the 4 categorical dimensions → X (45 cols), y = yield. `[vibe code 🤖 — standard pandas wrangling]`
2. **GP surrogate (analyze)** — Matern kernel (vs RBF), `alpha` (noise), `normalize_y`, `predict(return_std=True)` = posterior mean + uncertainty. `[write by hand 🧠 — justify kernel/config choices]`
3. **Sanity-check the GP** — Hold out a random test split from the tested pool, fit the GP, compare R²/RMSE against the RF benchmark (~0.83 / ~11.3%). Not expected to match exactly, just land in the same neighborhood. If it's wildly off, stop and debug the kernel/features here — don't carry a bad surrogate into EI or the loop. `[vibe code 🤖 — sklearn `train_test_split` + `r2_score`, trivial to add]`
4. **Acquisition — Expected Improvement (decide)** — Implement EI from the math; the mean/uncertainty balance, the `xi` explore/exploit parameter, masking already-seen points. `[write by hand 🧠 — core math, easy to get subtly wrong]`
5. **Closed loop (design→test→analyze)** — init random subset → fit GP on tested → EI over untested pool → pick argmax → "test" it (reveal known yield) → append → refit. Track `best_yield_so_far` per round. `[write by hand 🧠 — the control flow that ties the loop together]`
6. **Random-search baseline** — Same budget, random pick each round, track best-so-far. `[vibe code 🤖 — trivial]`
7. **Multi-seed averaging + xi sweep** — Run loop + random over ~20 seeds; average curves with std shading. Add a third curve: high-`xi` (explore) vs low-`xi` (exploit). `[vibe code 🤖 — looping over existing stages]`
8. **Results plot** — X = experiments run, Y = best yield found. Curves: loop, random, xi sweep. Annotate the experiments-saved gap (e.g. "90% of max in ~15 vs ~70 rounds"). `[vibe code 🤖 — matplotlib polish]`
9. **Descriptor featurization** — Swap 45 one-hot cols → 120 DFT descriptor cols already in the file. Attempt after stage 8 is solid. `[vibe code 🤖 — same shape as stage 1]`

---

## v2 — Generative proposer (the upgrade that makes it a discovery *engine*)

*Attempt only after v1 is solid.*

- **The change:** replace the *fixed candidate pool* with a *generative model that proposes new candidates* each round, instead of selecting from a pre-enumerated list. Now the loop can explore beyond the dataset.
- **v2a (bridge):** train a simple generative model (VAE) over the reaction/feature representation; each round, generate candidates → score with the GP + EI → "test" the closest real datapoint as the oracle. `[write by hand 🧠 — uses a simple VAE]`
- **v2b (stretch):** swap the proposer for a diffusion model; same loop. `[write by hand 🧠]`
- **Honest scope note:** the oracle is still simulated (nearest known datapoint / surrogate), so this shows *generative proposal inside a closed loop*, not real synthesis.

---

## Dataset

- Source: Ahneman, Estrada, Lin, Dreher, Doyle, *Science* 2018. Mirror: [thisisntnathan/BHpredict](https://github.com/thisisntnathan/BHpredict) (CSV + PKL, includes 120 DFT features).
- Structure: 15 aryl/heteroaryl halides × 4 ligands × 3 bases × 23 isoxazole additives (Glorius fragment-additive screen) → ~4,140–4,608 reactions incl. controls; ~3,720 usable after dropping missing yields.
- ~30% of reactions are zero/near-zero yield (failed region included by design — the loop keeps failures in, like real HTE data).
- Feature options in the same file: 45 one-hot columns (v1) or 120 DFT descriptors (stage 8).
- Reference benchmark: original random-forest ≈ R² 0.83, RMSE ~11.3% out-of-sample (sanity target for the GP).

---

## Build order rule

Always keep a working version; introduce only one new piece at a time. Ship v1 (one-hot, fixed pool) end-to-end before descriptors (stage 8) or the generative proposer (v2).
