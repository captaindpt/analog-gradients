# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_8M_iin_500u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -2.683698e+07 1/s
- b = -4.333276e+07 1/s
- c = -7.219024e+07 1/s
- d = 1.426917e+08 V/s
- implied tau (from a) = 37.262 ns
- derivative RMSE = 1.412367e+08 V/s
- derivative R^2 = 0.032359
- one-step reconstruction RMSE = 7.061834e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 23
  - a = 1.132472e+09 1/s
  - b = -4.488393e+10 1/s
  - c = -6.831518e+09 1/s
  - d = 8.084398e+10 V/s
  - phase derivative RMSE = 1.071002e+08 V/s
  - phase derivative R^2 = 0.752173
- reset samples = 225
  - a = -1.396618e+08 1/s
  - b = 6.114933e+09 1/s
  - c = 9.264018e+08 1/s
  - d = -1.491681e+09 V/s
  - phase derivative RMSE = 1.578107e+08 V/s
  - phase derivative R^2 = 0.025225
- decay samples = 151
  - a = 1.173351e+06 1/s
  - b = -2.290919e+07 1/s
  - c = -1.679507e+07 1/s
  - d = 4.193153e+07 V/s
  - phase derivative RMSE = 5.232703e+04 V/s
  - phase derivative R^2 = 0.985935

- piecewise derivative RMSE = 1.212639e+08 V/s
- piecewise derivative R^2 = 0.286683
- piecewise one-step reconstruction RMSE = 6.063197e-02 V

## Comparison

- derivative R^2 improvement: 0.032359 -> 0.286683 (delta = +0.254324)
- one-step RMSE improvement: 7.061834e-02 -> 6.063197e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_8M_iin_500u/lif_ode_fit_trace.csv`
