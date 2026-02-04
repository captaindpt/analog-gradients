# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_10M_iin_600u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -2.389632e+07 1/s
- b = -1.014868e+07 1/s
- c = -4.383287e+07 1/s
- d = 9.216322e+07 V/s
- implied tau (from a) = 41.847 ns
- derivative RMSE = 1.718108e+08 V/s
- derivative R^2 = 0.032090
- one-step reconstruction RMSE = 8.590540e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 22
  - a = 1.243620e+09 1/s
  - b = -5.142908e+10 1/s
  - c = -7.565483e+09 1/s
  - d = 9.263415e+10 V/s
  - phase derivative RMSE = 1.297466e+08 V/s
  - phase derivative R^2 = 0.749867
- reset samples = 273
  - a = -1.000744e+08 1/s
  - b = 1.018598e+10 1/s
  - c = 1.074319e+09 1/s
  - d = -1.800070e+09 V/s
  - phase derivative RMSE = 1.788806e+08 V/s
  - phase derivative R^2 = 0.015896
- decay samples = 104
  - a = 1.390264e+08 1/s
  - b = -1.304993e+08 1/s
  - c = -5.972963e+07 1/s
  - d = 1.326555e+08 V/s
  - phase derivative RMSE = 3.342735e+04 V/s
  - phase derivative R^2 = 0.990779

- piecewise derivative RMSE = 1.510687e+08 V/s
- piecewise derivative R^2 = 0.251687
- piecewise one-step reconstruction RMSE = 7.553434e-02 V

## Comparison

- derivative R^2 improvement: 0.032090 -> 0.251687 (delta = +0.219598)
- one-step RMSE improvement: 8.590540e-02 -> 7.553434e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_10M_iin_600u/lif_ode_fit_trace.csv`
