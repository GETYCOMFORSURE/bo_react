# Notes

## 1. Data + featurization

### convention: when assign variables with uppercase letters?
```python
DATA_PATH = "BH_CR_numbers.csv"

CATEGORICAL_COLS = [
    "base_number",
    "ligand_number",
    "aryl_halide_number",
    "additive_number",
]

TARGET_COL = "yield"
```

if the variable's value never changes / reassigned -> uppercase

### convention: X vs x
- X: a matrix 
- x: a vector

## 2. GP model
### why use sklearn rather than pytorch?
- Why: the GP fits on small data (dozens–hundreds of tested reactions). At that scale sklearn's GaussianProcessRegressor is exactly right — one class, .fit() / .predict(return_std=True). PyTorch/GPyTorch is for GPs on huge data needing GPU — overkill here, and reads as over-engineering.
- The split: PyTorch = generative nets (VAE, GAN, and v2's proposer). sklearn = the GP surrogate (not a neural net, no backprop). Your repo uses both, each where it fits. That's judgment, not mess.

### GP surrogate config choices
resource: [scikit-learn's GP User Guide](https://scikit-learn.org/stable/modules/gaussian_process.html)

**Gaussian Processes (GP)** are a nonparametric supervised learning method used to solve regression and probabilistic classification problems.

**Kernel: Matern(nu=2.5), not RBF.**
RBF is infinitely differentiable → assumes the function is *very smooth*.
Matern generalizes RBF with a smoothness knob (nu); nu=2.5 = rougher,
less smooth than RBF. Reaction-yield over ligand/base swaps is bumpy, not
glassy-smooth, so the less-smooth assumption is the more honest one.
Matern is the safe default when you're unsure — RBF is the special
(maximally smooth) case.

**alpha (noise on the kernel diagonal).**
Specifies noise level in the targets; added to the diagonal of the kernel
matrix (= Tikhonov regularization). Two jobs: (1) models real measurement
noise in HTE yields, (2) fixes numeric instability during fitting.
alpha=0 assumes perfect noise-free data → brittle fit + can break numerically.

**normalize_y=True.**
GP prior mean is constant. False → prior mean = 0; True → prior mean =
training data's mean. Yields live in [0,100], nowhere near 0, so without
normalize the zero-mean prior fights the data. Set True.

**predict(return_std=True) → (mean, std).**
GP outputs a *distribution*: posterior mean + standard deviation.
mean = predicted yield; std = uncertainty. EI needs BOTH — std is what
makes exploration possible. Mean-only would collapse EI into pure greedy.
