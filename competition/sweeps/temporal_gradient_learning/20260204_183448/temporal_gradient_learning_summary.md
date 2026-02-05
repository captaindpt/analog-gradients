# Temporal Gradient Learning Summary

Finite-difference learning on transistor simulations (`neuro_tile4_coupled`).

Training objective:
- Match target first-spike times across trace delays.
- Penalize missing spikes and ordering violations.
- Add optional energy regularization term.

Configuration:
- iterations: `1`
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
| final | 0.096705 | 0.096757 | 1002.300 | 7999987.870 | 1.800000 | 11.168 | 13.754 | 14.714 | 15.226 | 134.267 |

Initial vs final term contribution (% of total loss):

| State | timing % | count % | order % | energy % |
|-------|----------|---------|---------|----------|
| initial | 69.414 | 0.000 | 0.000 | 30.586 |
| final | 68.979 | 0.000 | 0.000 | 31.021 |

- Final generalization gap (holdout-train): `0.000052`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | timing% | energy% | e_w | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|---------|---------|-----|--------------|----------------|----------------|
| 0 | 0.098085 | 0.096863 | 0.068085 | 0.000000 | 0.000000 | 0.030000 | 69.414 | 30.586 | 0.030 | -0.290866 | 0.002022 | -1.212967 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_183448/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_183448/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_183448/temporal_gradient_learning_loss.svg`
