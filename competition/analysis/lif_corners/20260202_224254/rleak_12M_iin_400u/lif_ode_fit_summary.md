# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_400u/lif_neuron_waveform.csv`

## Global Linear Model (Baseline)

`dV/dt = a*V + b*out + c*spike + d`

- a = -6.083100e+07 1/s
- b = -3.295731e+06 1/s
- c = -1.166336e+07 1/s
- d = 7.339595e+07 V/s
- implied tau (from a) = 16.439 ns
- derivative RMSE = 1.111076e+08 V/s
- derivative R^2 = 0.033846
- one-step reconstruction RMSE = 5.555379e-02 V

## Phase-Aware Piecewise Model

Phase labels are derived from measured signals:
- `reset`: `spike > 0.9V` or `out < 0.9V`
- `charge`: outside reset and `dV/dt >= 0`
- `decay`: outside reset and `dV/dt < 0`

Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`

- charge samples = 24
  - a = 9.857334e+08 1/s
  - b = -8.614912e+10 1/s
  - c = -9.908818e+09 1/s
  - d = 1.551132e+11 V/s
  - phase derivative RMSE = 9.435081e+07 V/s
  - phase derivative R^2 = 0.693229
- reset samples = 182
  - a = -2.112744e+08 1/s
  - b = 5.951026e+09 1/s
  - c = 8.848534e+08 1/s
  - d = -1.342514e+09 V/s
  - phase derivative RMSE = 1.368369e+08 V/s
  - phase derivative R^2 = 0.030997
- decay samples = 193
  - a = 1.206312e+08 1/s
  - b = -1.400313e+08 1/s
  - c = -5.911063e+07 1/s
  - d = 1.641293e+08 V/s
  - phase derivative RMSE = 3.741008e+04 V/s
  - phase derivative R^2 = 0.990660

- piecewise derivative RMSE = 9.527012e+07 V/s
- piecewise derivative R^2 = 0.289650
- piecewise one-step reconstruction RMSE = 4.763506e-02 V

## Comparison

- derivative R^2 improvement: 0.033846 -> 0.289650 (delta = +0.255804)
- one-step RMSE improvement: 5.555379e-02 -> 4.763506e-02 V

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_400u/lif_ode_fit_trace.csv`
