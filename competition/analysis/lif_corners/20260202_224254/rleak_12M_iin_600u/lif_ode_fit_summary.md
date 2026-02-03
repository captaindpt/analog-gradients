# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_600u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -2.381898e+07 1/s
- b = -1.052764e+07 1/s
- c = -4.430025e+07 1/s
- d = 9.289728e+07 V/s
- implied tau (from a) = 41.983 ns
- derivative RMSE = 1.718116e+08 V/s
- derivative R^2 = 0.032097
- one-step reconstruction RMSE = 8.590578e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 22
  - a = 1.243028e+09 1/s
  - b = -5.108910e+10 1/s
  - c = -7.536483e+09 1/s
  - d = 9.202219e+10 V/s
  - phase derivative RMSE = 1.297551e+08 V/s
  - phase derivative R^2 = 0.749834
- reset samples = 273
  - a = -1.004834e+08 1/s
  - b = 1.037355e+10 1/s
  - c = 1.084635e+09 1/s
  - d = -1.817981e+09 V/s
  - phase derivative RMSE = 1.788744e+08 V/s
  - phase derivative R^2 = 0.015985
- decay samples = 104
  - a = 1.358106e+08 1/s
  - b = -1.264289e+08 1/s
  - c = -5.838067e+07 1/s
  - d = 1.277041e+08 V/s
  - phase derivative RMSE = 3.242890e+04 V/s
  - phase derivative R^2 = 0.991324

- piecewise derivative RMSE = 1.510641e+08 V/s
- piecewise derivative R^2 = 0.251745
- piecewise one-step reconstruction RMSE = 7.553205e-02 V

## Comparison

- derivative R^2 improvement: 0.032097 -> 0.251745 (delta = +0.219648)
- one-step RMSE improvement: 8.590578e-02 -> 7.553205e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_600u/lif_ode_fit_trace.csv`
