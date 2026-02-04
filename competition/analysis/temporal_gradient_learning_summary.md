# Temporal Gradient Learning Summary

Finite-difference learning on transistor simulations (`neuro_tile4_coupled`).

Training objective:
- Match target first-spike times across trace delays.
- Penalize missing spikes and ordering violations.
- Add optional energy regularization term.

Configuration:
- iterations: `6`
- target mode: `measured_anchor_shift`
- train trace delays (ns): `4.500,5.500,7.500`
- holdout trace delays (ns): `6.500,9.000,10.500`
- base target spikes (ns): `47.500,49.500,51.500,53.500`
- target shift (ns): `1.000,1.000,1.000,1.000`
- target spike counts: `15,15,15,15`
- penalties: missing=`400.0`, count_weight=`12.0`, order_weight=`35.0`, order_margin_ns=`0.2`, energy_weight=`2.0`
- energy reference (pJ): `133.939983`

Initial vs final:

| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 3.008759 | 2.991241 | 1000.000 | 8000000.000 | 1.800000 | 10.508 | 13.086 | 14.047 | 14.559 | 134.527 |
| final | 2.290754 | 2.276373 | 959.398 | 7999961.196 | 1.685291 | 10.867 | 13.439 | 14.443 | 14.968 | 127.563 |

- Final generalization gap (holdout-train): `-0.014381`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|--------------|----------------|----------------|
| 0 | 3.008759 | 2.991241 | 1.000000 | 0.000000 | 0.000000 | 2.008759 | 1.029558 | -0.000850 | 5.418773 |
| 1 | 2.904784 | 2.886213 | 0.911218 | 0.000000 | 0.000000 | 1.993566 | 0.958004 | -0.001752 | 5.799561 |
| 2 | 2.781550 | 2.763666 | 0.804592 | 0.000000 | 0.000000 | 1.976958 | 0.892723 | 0.000123 | 5.972227 |
| 3 | 2.662926 | 2.646903 | 0.703301 | 0.000000 | 0.000000 | 1.959625 | 0.922997 | 0.004244 | 5.818128 |
| 4 | 2.544510 | 2.528124 | 0.602392 | 0.000000 | 0.000000 | 1.942118 | 0.761197 | 0.000677 | 6.182824 |
| 5 | 2.416879 | 2.400383 | 0.493048 | 0.000000 | 0.000000 | 1.923831 | 0.691632 | 0.004028 | 6.279569 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_155533/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_155533/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_155533/temporal_gradient_learning_loss.svg`
