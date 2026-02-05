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
- iterations: `1`
- target mode: `absolute`
- train trace delays (ns): `5.000,8.000`
- holdout trace delays (ns): `6.500,9.500`
- base target spikes (ns): `9.388,11.896,12.985,13.640`
- target shift (ns): `n/a (absolute mode)`
- target spike counts: `15,15,15,15`
- penalties: missing=`400.0`, count_weight=`12.0`, order_weight=`35.0`, order_margin_ns=`5.0`
- energy weight schedule: constant `0.030000`
- anchor probe split: `train`
- energy reference (pJ): `134.270707`

Initial vs final:

| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 1481.522717 | 1480.722571 | 1000.000 | 8000000.000 | 1.800000 | 11.175 | 13.756 | 14.715 | 15.227 | 134.271 |
| final | 1460.794877 | 1460.378348 | 1171.877 | 7993916.192 | 1.800000 | 11.068 | 13.628 | 14.632 | 15.181 | 134.354 |

Initial vs final term contribution (% of total loss):

| State | timing % | count % | order % | energy % |
|-------|----------|---------|---------|----------|
| initial | 0.005 | 0.000 | 99.993 | 0.002 |
| final | 0.002 | 0.000 | 99.996 | 0.002 |

- Final generalization gap (holdout-train): `-0.416528`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | timing% | energy% | e_w | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|---------|---------|-----|--------------|----------------|----------------|
| 0 | 1481.522717 | 1480.722571 | 0.068085 | 0.000000 | 1481.424632 | 0.030000 | 0.005 | 0.002 | 0.030 | -152.791966 | 1.056832 | -114.567125 |

Artifacts:
- Eval CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_185702_order_stress/temporal_gradient_learning.csv`
- Trace CSV: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_185702_order_stress/temporal_gradient_trace.csv`
- Loss plot: `/home/v71349/analog-gradients/competition/sweeps/temporal_gradient_learning/20260204_185702_order_stress/temporal_gradient_learning_loss.svg`
