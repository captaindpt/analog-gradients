# Temporal Gradient Learning Summary

Finite-difference learning on transistor simulations (`neuro_tile4_coupled`).

Claim scope:
- Classification: **method demo** (internal objective + limited delay-family generalization).
- Not yet an externally valid benchmark against matched digital training/eval protocol.

Training objective:
- Match target first-spike times across trace delays.
- Penalize missing spikes and ordering violations.
- Add optional energy regularization term.

Configuration:
- iterations: `4`
- target mode: `absolute`
- train trace delays (ns): `5.000,8.000`
- holdout trace delays (ns): `6.500,9.500`
- base target spikes (ns): `9.388,11.896,12.985,13.640`
- target shift (ns): `n/a (absolute mode)`
- target spike counts: `15,15,15,15`
- penalties: missing=`400.0`, count_weight=`12.0`, order_weight=`35.0`, order_margin_ns=`0.2`
- energy weight schedule: constant `0.030000`
- anchor probe split: `train`
- energy reference (pJ): `134.270707`

Initial vs final:

| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 0.098085 | 0.096863 | 1000.000 | 8000000.000 | 1.800000 | 11.175 | 13.756 | 14.715 | 15.227 | 134.271 |
| final | 0.095554 | 0.095044 | 1009.108 | 7999984.699 | 1.800000 | 11.169 | 13.750 | 14.711 | 15.225 | 134.278 |

Initial vs final term contribution (% of total loss):

| State | timing % | count % | order % | energy % |
|-------|----------|---------|---------|----------|
| initial | 69.414 | 0.000 | 0.000 | 30.586 |
| final | 68.602 | 0.000 | 0.000 | 31.398 |

- Final generalization gap (holdout-train): `-0.000510`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | timing% | energy% | e_w | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|---------|---------|-----|--------------|----------------|----------------|
| 0 | 0.098085 | 0.096863 | 0.068085 | 0.000000 | 0.000000 | 0.030000 | 69.414 | 30.586 | 0.030 | -0.290866 | 0.002022 | -1.212967 |
| 1 | 0.096705 | 0.096757 | 0.066706 | 0.000000 | 0.000000 | 0.029999 | 68.979 | 31.021 | 0.030 | -0.289688 | -0.000822 | -1.191834 |
| 2 | 0.096722 | 0.096303 | 0.066722 | 0.000000 | 0.000000 | 0.030000 | 68.983 | 31.017 | 0.030 | -0.286504 | 0.000573 | -1.197779 |
| 3 | 0.096248 | 0.095142 | 0.066246 | 0.000000 | 0.000000 | 0.030002 | 68.829 | 31.171 | 0.030 | -0.284617 | 0.000778 | -1.175893 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_183829/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_183829/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_183829/temporal_gradient_learning_loss.svg`
