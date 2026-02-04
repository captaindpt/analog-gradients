# Temporal Gradient Learning Summary

Finite-difference learning on transistor simulations (`neuro_tile4_coupled`).

Training objective:
- Match target first-spike times across trace delays.
- Penalize missing spikes and ordering violations.
- Add optional energy regularization term.

Configuration:
- iterations: `4`
- target mode: `measured_anchor_shift`
- trace delays (ns): `5.000,8.000`
- base target spikes (ns): `47.500,49.500,51.500,53.500`
- target shift (ns): `1.000,1.000,1.000,1.000`
- target spike counts: `15,15,15,15`
- penalties: missing=`400.0`, count_weight=`12.0`, order_weight=`35.0`, order_margin_ns=`0.2`, energy_weight=`2.0`
- energy reference (pJ): `134.270707`

Initial vs final:

| State | loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 3.000000 | 1000.000 | 8000000.000 | 1.800000 | 11.175 | 13.756 | 14.715 | 15.227 | 134.271 |
| final | 2.543306 | 970.631 | 8000006.952 | 1.725716 | 11.392 | 13.957 | 14.948 | 15.453 | 129.858 |

Per-iteration base points:

| iter | loss | timing | count_pen | order_pen | energy_pen | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------|--------|-----------|-----------|------------|--------------|----------------|----------------|
| 0 | 3.000000 | 1.000000 | 0.000000 | 0.000000 | 2.000000 | 1.039153 | -0.008029 | 5.319335 |
| 1 | 2.900509 | 0.915404 | 0.000000 | 0.000000 | 1.985104 | 0.951707 | 0.004334 | 5.712981 |
| 2 | 2.777494 | 0.808695 | 0.000000 | 0.000000 | 1.968799 | 0.910556 | 0.001707 | 5.975878 |
| 3 | 2.657354 | 0.705915 | 0.000000 | 0.000000 | 1.951439 | 0.910054 | 0.000829 | 5.805798 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_151222/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_151222/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_151222/temporal_gradient_learning_loss.svg`
