# Mini Bayesian Optimization for Reaction Yield

**Summary**
A closed-loop Bayesian optimization demo on the Buchwald–Hartwig HTE dataset that reaches near-maximum yield in far fewer experiments than random screening — a small, transparent reproduction of the core optimization loop used in data-driven reaction development.

**Goal**
Build a working, fully-understood BO pipeline on a public reaction-yield benchmark, prioritizing clarity and correctness over sophistication.

**Timeline:** ~5 focused days.

---

## Project structure

```
bo_reaction_demo/
├── data/                  # BHpredict CSV
├── featurize.py           # data loading + featurization
├── gp_model.py            # Gaussian Process surrogate
├── acquisition.py         # Expected Improvement
├── bo_loop.py             # main optimization loop
├── baseline.py            # random-search baseline
├── run_experiment.py      # orchestration
├── plot_results.py        # results plotting
└── README.md
```

## Build stages

1. **Data + featurization** — Load CSV, inspect columns, one-hot encode the 4 categorical dimensions → X (45 cols), y = yield. `[vibe code — standard pandas wrangling]`
2. **GP surrogate** — Matern kernel (vs RBF), `alpha` (noise), `normalize_y`, `predict(return_std=True)` = posterior mean + uncertainty. `[write by hand — need to justify kernel/config choices]`
3. **Acquisition — Expected Improvement** — Implement EI from the math; the mean/uncertainty balance, the `xi` explore/exploit parameter, and masking already-seen points. `[write by hand — core math, easy to get subtly wrong]`
4. **BO loop** — init random subset → fit GP on seen → EI over full space → pick argmax unseen → reveal known yield → append → refit. Track `best_yield_so_far` per iteration. `[write by hand — the control-flow logic that ties everything together]`
5. **Random-search baseline** — Same budget, random pick each step, track best-so-far. `[vibe code — trivial]`
6. **Multi-seed averaging + xi sweep** — Run BO + random over ~20 seeds; average curves with std shading. Add a third curve: BO high-`xi` (explore) vs low-`xi` (exploit). `[vibe code — plumbing/looping over existing stages]`
7. **Results plot** — X = experiments run, Y = best yield found. Curves: BO, random, xi sweep. Annotate the experiments-saved gap (e.g. "90% of max in ~15 vs ~70"). `[vibe code — matplotlib styling/polish]`
8. **Descriptor featurization (v2)** — Swap 45 one-hot cols → 120 DFT descriptor cols already in the file. Attempt after stage 7 is solid. `[vibe code — same shape as stage 1]`

---
## Dataset

- Source: Ahneman, Estrada, Lin, Dreher, Doyle, *Science* 2018. Mirror: [thisisntnathan/BHpredict](https://github.com/thisisntnathan/BHpredict) (CSV + PKL, includes 120 DFT features).
- Structure: 15 aryl/heteroaryl halides × 4 Buchwald ligands × 3 bases × 23 isoxazole additives (Glorius fragment-additive screen) → ~4,140–4,608 reactions incl. controls; ~3,720 usable after dropping missing yields.
- ~30% of reactions are zero/near-zero yield (failed region included by design).
- Feature options in the same file: 45 one-hot columns (v1) or 120 DFT descriptors (v2).
- Reference benchmark: original random-forest ≈ R² 0.83, RMSE ~11.3% out-of-sample (sanity target for the GP).

---

Here's the content from the screenshot formatted as markdown:
markdown- Source: Ahneman, Estrada, Lin, Dreher, Doyle, *Science* 2018. Mirror: [thisisntnathan/BHpredict](https://github.com/thisisntnathan/BHpredict) (CSV + PKL, includes 120 DFT features).
- Structure: 15 aryl/heteroaryl halides × 4 Buchwald ligands × 3 bases × 23 isoxazole additives (Glorius fragment-additive screen) → ~4,140–4,608 reactions incl. controls; ~3,720 usable after dropping missing yields.
- ~30% of reactions are zero/near-zero yield (failed region included by design).
- Feature options in the same file: 45 one-hot columns (v1) or 120 DFT descriptors (v2).
- Reference benchmark: original random-forest ≈ R² 0.83, RMSE ~11.3% out-of-sample (sanity target for the GP).

---
## Deliverables

- Clean repo + reproducible README.
- Results plot (BO vs random vs xi sweep, with experiments-saved annotation).
- Held-out GP sanity check (R²/RMSE in the ~0.83 / ~11% ballpark).

---

## Build order rule

Always keep a working version; introduce only one new piece at a time. Ship v1 (one-hot) end-to-end before attempting v2 (descriptors).
