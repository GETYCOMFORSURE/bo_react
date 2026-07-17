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
