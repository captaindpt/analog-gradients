# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_10M_iin_400u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -6.105234e+07 1/s
- b = -2.790539e+06 1/s
- c = -1.102730e+07 1/s
- d = 7.252349e+07 V/s
- implied tau (from a) = 16.379 ns
- derivative RMSE = 1.111062e+08 V/s
- derivative R^2 = 0.033841
- one-step reconstruction RMSE = 5.555309e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 24
  - a = 9.848167e+08 1/s
  - b = -8.532807e+10 1/s
  - c = -9.828669e+09 1/s
  - d = 1.536353e+11 V/s
  - phase derivative RMSE = 9.447533e+07 V/s
  - phase derivative R^2 = 0.692441
- reset samples = 182
  - a = -2.111550e+08 1/s
  - b = 5.960449e+09 1/s
  - c = 8.838649e+08 1/s
  - d = -1.340913e+09 V/s
  - phase derivative RMSE = 1.368380e+08 V/s
  - phase derivative R^2 = 0.030916
- decay samples = 193
  - a = 1.167040e+08 1/s
  - b = -1.354433e+08 1/s
  - c = -5.755007e+07 1/s
  - d = 1.587529e+08 V/s
  - phase derivative RMSE = 3.747697e+04 V/s
  - phase derivative R^2 = 0.990635

- piecewise derivative RMSE = 9.527822e+07 V/s
- piecewise derivative R^2 = 0.289507
- piecewise one-step reconstruction RMSE = 4.763911e-02 V

## Comparison

- derivative R^2 improvement: 0.033841 -> 0.289507 (delta = +0.255667)
- one-step RMSE improvement: 5.555309e-02 -> 4.763911e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_10M_iin_400u/lif_ode_fit_trace.csv`
