# Matmul4x4 Regime Decomposition (Measured)

Source: `competition/sweeps/matmul4x4_crossover/matmul4x4_crossover.csv`

| Regime | Digital Energy (pJ) | Neuro Energy (pJ) | Ratio (Neuro/Digital) | Winner |
|--------|----------------------|-------------------|------------------------|--------|
| Active products > 0 | 0.029817 | 3.339743 | 112.009x | Digital |
| Active products = 0 | 0.000332 | 0.000050 | 0.151x | Neuro |

Duty-cycle crossover (mixture model):
- Let `alpha` be the fraction of windows with active products.
- Neuro expected energy `<` digital when `alpha < 0.000085` (0.0085%).

Interpretation:
- Current neuro implementation wins clearly in silent/idle windows.
- Current neuro implementation loses strongly when compute is active.
- To win typical sparse compute, active-regime neuro energy must drop by orders of magnitude.
