# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_8M_iin_400u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -6.124898e+07 1/s
- b = -2.466423e+06 1/s
- c = -1.059864e+07 1/s
- d = 7.198717e+07 V/s
- implied tau (from a) = 16.327 ns
- derivative RMSE = 1.111039e+08 V/s
- derivative R^2 = 0.033835
- one-step reconstruction RMSE = 5.555197e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 24
  - a = 1.001277e+09 1/s
  - b = -9.458903e+10 1/s
  - c = -1.067677e+10 1/s
  - d = 1.703047e+11 V/s
  - phase derivative RMSE = 9.342539e+07 V/s
  - phase derivative R^2 = 0.699269
- reset samples = 182
  - a = -2.112962e+08 1/s
  - b = 6.007036e+09 1/s
  - c = 8.856748e+08 1/s
  - d = -1.344012e+09 V/s
  - phase derivative RMSE = 1.368385e+08 V/s
  - phase derivative R^2 = 0.030809
- decay samples = 193
  - a = 9.209319e+07 1/s
  - b = -1.050471e+08 1/s
  - c = -4.742185e+07 1/s
  - d = 1.221246e+08 V/s
  - phase derivative RMSE = 3.730160e+04 V/s
  - phase derivative R^2 = 0.990741

- piecewise derivative RMSE = 9.521629e+07 V/s
- piecewise derivative R^2 = 0.290398
- piecewise one-step reconstruction RMSE = 4.760814e-02 V

## Comparison

- derivative R^2 improvement: 0.033835 -> 0.290398 (delta = +0.256563)
- one-step RMSE improvement: 5.555197e-02 -> 4.760814e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_8M_iin_400u/lif_ode_fit_trace.csv`
