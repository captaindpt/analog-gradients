# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/data/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -1.044924e+08 1/s
- b = 5.815602e+07 1/s
- c = 7.597979e+07 1/s
- d = -2.304351e+07 V/s
- implied tau (from a) = 9.570 ns
- derivative RMSE = 1.414429e+08 V/s
- derivative R^2 = 0.029397
- one-step reconstruction RMSE = 7.072143e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 23
  - a = 1.455520e+09 1/s
  - b = -1.799532e+10 1/s
  - c = -8.563682e+09 1/s
  - d = 3.218699e+10 V/s
  - phase derivative RMSE = 1.047229e+08 V/s
  - phase derivative R^2 = 0.779389
- reset samples = 206
  - a = -2.247838e+08 1/s
  - b = 3.550593e+08 1/s
  - c = 3.641824e+08 1/s
  - d = -3.690561e+08 V/s
  - phase derivative RMSE = 1.619979e+08 V/s
  - phase derivative R^2 = 0.027558
- decay samples = 170
  - a = 2.358605e+07 1/s
  - b = 2.485543e+06 1/s
  - c = -3.204357e+07 1/s
  - d = -1.976006e+07 V/s
  - phase derivative RMSE = 7.112596e+04 V/s
  - phase derivative R^2 = 0.999627

- piecewise derivative RMSE = 1.190855e+08 V/s
- piecewise derivative R^2 = 0.311985
- piecewise one-step reconstruction RMSE = 5.954277e-02 V

## Comparison

- derivative R^2 improvement: 0.029397 -> 0.311985 (delta = +0.282588)
- one-step RMSE improvement: 7.072143e-02 -> 5.954277e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_ode_fit_trace.csv`
