# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_10M_iin_500u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -2.507383e+07 1/s
- b = -5.287505e+07 1/s
- c = -8.355026e+07 1/s
- d = 1.606666e+08 V/s
- implied tau (from a) = 39.882 ns
- derivative RMSE = 1.411841e+08 V/s
- derivative R^2 = 0.032523
- one-step reconstruction RMSE = 7.059203e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 23
  - a = 1.133284e+09 1/s
  - b = -4.484390e+10 1/s
  - c = -6.844077e+09 1/s
  - d = 8.077191e+10 V/s
  - phase derivative RMSE = 1.070840e+08 V/s
  - phase derivative R^2 = 0.752239
- reset samples = 224
  - a = -1.406183e+08 1/s
  - b = 6.212057e+09 1/s
  - c = 9.287797e+08 1/s
  - d = -1.494806e+09 V/s
  - phase derivative RMSE = 1.580809e+08 V/s
  - phase derivative R^2 = 0.025406
- decay samples = 152
  - a = -8.956189e+06 1/s
  - b = -1.719792e+07 1/s
  - c = -1.416601e+07 1/s
  - d = 3.929966e+07 V/s
  - phase derivative RMSE = 5.329948e+04 V/s
  - phase derivative R^2 = 0.986633

- piecewise derivative RMSE = 1.212033e+08 V/s
- piecewise derivative R^2 = 0.286986
- piecewise one-step reconstruction RMSE = 6.060165e-02 V

## Comparison

- derivative R^2 improvement: 0.032523 -> 0.286986 (delta = +0.254463)
- one-step RMSE improvement: 7.059203e-02 -> 6.060165e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_10M_iin_500u/lif_ode_fit_trace.csv`
