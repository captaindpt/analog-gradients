# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_500u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -2.514062e+07 1/s
- b = -5.223141e+07 1/s
- c = -8.283532e+07 1/s
- d = 1.594812e+08 V/s
- implied tau (from a) = 39.776 ns
- derivative RMSE = 1.411857e+08 V/s
- derivative R^2 = 0.032530
- one-step reconstruction RMSE = 7.059284e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 23
  - a = 1.132683e+09 1/s
  - b = -4.505480e+10 1/s
  - c = -6.843678e+09 1/s
  - d = 8.115154e+10 V/s
  - phase derivative RMSE = 1.071020e+08 V/s
  - phase derivative R^2 = 0.752150
- reset samples = 224
  - a = -1.442489e+08 1/s
  - b = 6.964387e+09 1/s
  - c = 9.791884e+08 1/s
  - d = -1.580277e+09 V/s
  - phase derivative RMSE = 1.580272e+08 V/s
  - phase derivative R^2 = 0.026119
- decay samples = 152
  - a = -1.837477e+07 1/s
  - b = -1.280714e+07 1/s
  - c = -1.190931e+07 1/s
  - d = 3.852221e+07 V/s
  - phase derivative RMSE = 5.443255e+04 V/s
  - phase derivative R^2 = 0.986548

- piecewise derivative RMSE = 1.211649e+08 V/s
- piecewise derivative R^2 = 0.287460
- piecewise one-step reconstruction RMSE = 6.058244e-02 V

## Comparison

- derivative R^2 improvement: 0.032530 -> 0.287460 (delta = +0.254929)
- one-step RMSE improvement: 7.059284e-02 -> 6.058244e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_500u/lif_ode_fit_trace.csv`
