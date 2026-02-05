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
- target spike counts: `1,1,1,1`
- penalties: missing=`400.0`, count_weight=`12.0`, order_weight=`35.0`, order_margin_ns=`0.2`
- energy weight schedule: constant `0.030000`
- anchor probe split: `train`
- energy reference (pJ): `1000000000.000000`

Initial vs final:

| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |
|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|
| initial | 448.030000 | 448.030000 | 1000.000 | 8000000.000 | 1.800000 | -1.000 | -1.000 | -1.000 | -1.000 | 1000000000.000 |
| final | 448.030000 | 448.030000 | 1000.000 | 8000000.000 | 1.800000 | -1.000 | -1.000 | -1.000 | -1.000 | 1000000000.000 |

Initial vs final term contribution (% of total loss):

| State | timing % | count % | order % | energy % |
|-------|----------|---------|---------|----------|
| initial | 89.280 | 10.714 | 0.000 | 0.007 |
| final | 89.280 | 10.714 | 0.000 | 0.007 |

- Final generalization gap (holdout-train): `0.000000`

Per-iteration base points:

| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | timing% | energy% | e_w | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |
|------|------------|--------------|--------|-----------|-----------|------------|---------|---------|-----|--------------|----------------|----------------|
| 0 | 448.030000 | 448.030000 | 400.000000 | 48.000000 | 0.000000 | 0.030000 | 89.280 | 0.007 | 0.030 | 0.000000 | 0.000000 | 0.000000 |

Artifacts:
- Eval CSV: `competition/sweeps/temporal_gradient_learning/20260204_184918_count_stress/temporal_gradient_learning.csv`
- Trace CSV: `competition/sweeps/temporal_gradient_learning/20260204_184918_count_stress/temporal_gradient_trace.csv`
- Loss plot: `competition/sweeps/temporal_gradient_learning/20260204_184918_count_stress/temporal_gradient_learning_loss.svg`
