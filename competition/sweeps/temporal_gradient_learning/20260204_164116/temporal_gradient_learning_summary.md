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
- energy weight schedule: constant `0.100000`
- anchor probe split: `train`
- energy reference (pJ): `134.270707`

Initial vs final:

| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 0.168085 | 0.166547 | 1000.000 | 8000000.000 | 1.800000 | 11.175 | 13.756 | 14.715 | 15.227 | 134.271 |
| final | 0.165598 | 0.164208 | 1009.068 | 7999976.514 | 1.800000 | 11.170 | 13.749 | 14.710 | 15.225 | 134.278 |

Initial vs final term contribution (% of total loss):

| State | timing % | count % | order % | energy % |
|-------|----------|---------|---------|----------|
| initial | 40.506 | 0.000 | 0.000 | 59.494 |
| final | 39.609 | 0.000 | 0.000 | 60.391 |

- Final generalization gap (holdout-train): `-0.001390`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | timing% | energy% | e_w | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|---------|---------|-----|--------------|----------------|----------------|
| 0 | 0.168085 | 0.166547 | 0.068085 | 0.000000 | 0.000000 | 0.100000 | 40.506 | 59.494 | 0.100 | -0.290578 | 0.002038 | -1.183180 |
| 1 | 0.167334 | 0.166136 | 0.067333 | 0.000000 | 0.000000 | 0.100001 | 40.239 | 59.761 | 0.100 | -0.287177 | 0.000616 | -1.132179 |
| 2 | 0.166633 | 0.165498 | 0.066630 | 0.000000 | 0.000000 | 0.100003 | 39.986 | 60.014 | 0.100 | -0.285651 | 0.000487 | -1.202562 |
| 3 | 0.165628 | 0.165534 | 0.065622 | 0.000000 | 0.000000 | 0.100006 | 39.620 | 60.380 | 0.100 | -0.283117 | 0.000773 | -1.210961 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_164116/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_164116/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_164116/temporal_gradient_learning_loss.svg`
