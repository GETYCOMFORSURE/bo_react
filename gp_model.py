"""
gp_model.py — Gaussian Process surrogate for the closed discovery loop.

Role in the loop: the "analyze" step. Fit on reactions tested so far,
predict yield + uncertainty for every untested candidate, so the
acquisition step can decide what to test next.

Design choices (and why):

- Kernel: Matern(nu=2.5), not RBF.
    <your reason — what smoothness assumption fits reaction yield, and why>

- alpha (observation noise on the diagonal):
    <your reason — what real property of HTE data this represents,
     and what breaks at alpha=0>

- normalize_y=True:
    <your reason — GP assumes zero-mean prior; yields are [0,100];
     what goes wrong without it>

- predict(return_std=True) → (mean, std):
    <your reason — which one EI needs and why std is not optional>

Interface:
    fit(X_tested, y_tested)
    predict(X_candidates, return_std=True) -> (mean, std)
"""
