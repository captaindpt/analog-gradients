# Temporal Gradient Learning Summary

Finite-difference learning on transistor simulations (`neuro_tile4_coupled`).

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
- target shift (ns): `1.000,1.000,1.000,1.000`
- target spike counts: `15,15,15,15`
- penalties: missing=`400.0`, count_weight=`12.0`, order_weight=`35.0`, order_margin_ns=`0.2`
- energy weight schedule: `0.250000 -> 1.000000`
- anchor probe split: `train`
- energy reference (pJ): `134.270707`

Initial vs final:

| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 0.318085 | 0.315872 | 1000.000 | 8000000.000 | 1.800000 | 11.175 | 13.756 | 14.715 | 15.227 | 134.271 |
| final | 1.065497 | 1.060791 | 1009.077 | 7999986.593 | 1.800000 | 11.169 | 13.749 | 14.711 | 15.225 | 134.273 |

Initial vs final term contribution (% of total loss):

| State | timing % | count % | order % | energy % |
|-------|----------|---------|---------|----------|
| initial | 21.405 | 0.000 | 0.000 | 78.595 |
| final | 6.146 | 0.000 | 0.000 | 93.854 |

- Final generalization gap (holdout-train): `-0.004706`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | timing% | energy% | e_w | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|---------|---------|-----|--------------|----------------|----------------|
| 0 | 0.318085 | 0.315872 | 0.068085 | 0.000000 | 0.000000 | 0.250000 | 21.405 | 78.595 | 0.250 | -0.289963 | 0.002073 | -1.119351 |
| 1 | 0.566801 | 0.564937 | 0.066821 | 0.000000 | 0.000000 | 0.499980 | 11.789 | 88.211 | 0.500 | -0.287069 | 0.000209 | -1.014585 |
| 2 | 0.816754 | 0.813282 | 0.066681 | 0.000000 | 0.000000 | 0.750074 | 8.164 | 91.836 | 0.750 | -0.292821 | 0.000299 | -0.860753 |
| 3 | 1.066288 | 1.061561 | 0.066280 | 0.000000 | 0.000000 | 1.000008 | 6.216 | 93.784 | 1.000 | -0.277739 | -0.000346 | -0.765872 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_163109/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_163109/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_163109/temporal_gradient_learning_loss.svg`
