# Temporal Gradient Learning Summary

Finite-difference learning on transistor simulations (`neuro_tile4_coupled`).

Training objective:
- Match target first-spike times across trace delays.
- Penalize missing spikes and ordering violations.
- Add optional energy regularization term.

Configuration:
- iterations: `2`
- target mode: `measured_anchor_shift`
- train trace delays (ns): `5.000,8.000`
- holdout trace delays (ns): `6.500,9.500`
- base target spikes (ns): `47.500,49.500,51.500,53.500`
- target shift (ns): `1.000,1.000,1.000,1.000`
- target spike counts: `15,15,15,15`
- penalties: missing=`400.0`, count_weight=`12.0`, order_weight=`35.0`, order_margin_ns=`0.2`, energy_weight=`2.0`
- energy reference (pJ): `133.968211`

Initial vs final:

| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 3.004516 | 2.995484 | 1000.000 | 8000000.000 | 1.800000 | 11.175 | 13.756 | 14.715 | 15.227 | 134.271 |
| final | 2.781567 | 2.769320 | 984.791 | 8000035.961 | 1.763811 | 11.274 | 13.848 | 14.821 | 15.333 | 132.172 |

- Final generalization gap (holdout-train): `-0.012248`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|--------------|----------------|----------------|
| 0 | 3.004516 | 2.995484 | 1.000000 | 0.000000 | 0.000000 | 2.004516 | 1.039172 | -0.008028 | 5.321257 |
| 1 | 2.904528 | 2.892001 | 0.915003 | 0.000000 | 0.000000 | 1.989525 | 0.937281 | 0.002032 | 5.727231 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_152633/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_152633/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_152633/temporal_gradient_learning_loss.svg`
