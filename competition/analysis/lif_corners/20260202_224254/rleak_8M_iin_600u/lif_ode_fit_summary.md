# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_8M_iin_600u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -3.055361e+07 1/s
- b = 2.193694e+07 1/s
- c = -5.318587e+06 1/s
- d = 3.212535e+07 V/s
- implied tau (from a) = 32.729 ns
- derivative RMSE = 1.714513e+08 V/s
- derivative R^2 = 0.032251
- one-step reconstruction RMSE = 8.572567e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 22
  - a = 1.221053e+09 1/s
  - b = -4.077214e+10 1/s
  - c = -6.531932e+09 1/s
  - d = 7.345193e+10 V/s
  - phase derivative RMSE = 1.300546e+08 V/s
  - phase derivative R^2 = 0.748709
- reset samples = 273
  - a = -7.600512e+07 1/s
  - b = 1.752817e+09 1/s
  - c = 5.086758e+08 1/s
  - d = -8.210660e+08 V/s
  - phase derivative RMSE = 1.787299e+08 V/s
  - phase derivative R^2 = 0.011980
- decay samples = 104
  - a = 1.378390e+08 1/s
  - b = -1.336722e+08 1/s
  - c = -6.028329e+07 1/s
  - d = 1.393407e+08 V/s
  - phase derivative RMSE = 3.155556e+04 V/s
  - phase derivative R^2 = 0.991031

- piecewise derivative RMSE = 1.509613e+08 V/s
- piecewise derivative R^2 = 0.249740
- piecewise one-step reconstruction RMSE = 7.548063e-02 V

## Comparison

- derivative R^2 improvement: 0.032251 -> 0.249740 (delta = +0.217489)
- one-step RMSE improvement: 8.572567e-02 -> 7.548063e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_8M_iin_600u/lif_ode_fit_trace.csv`
