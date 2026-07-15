# Notes

## 1. Data + featurization

**convention: when assign variables with uppercase letters?**

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

**convention: X vs x*
- X: a matrix 
- x: a vector

