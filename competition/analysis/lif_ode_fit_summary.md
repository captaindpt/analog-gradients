# LIF ODE Fit Summary

Input waveform:
- `/home/v71349/analog-gradients/competition/data/lif_neuron_waveform.csv`

Fitted model:

`dV/dt = a*V + b*out + c*spike + d`

- a = -1.044924e+08 1/s
- b = 5.815602e+07 1/s
- c = 7.597979e+07 1/s
- d = -2.304351e+07 V/s
- implied tau (from a) = 9.570 ns

Fit quality:
- derivative RMSE = 1.414429e+08 V/s
- derivative R^2 = 0.029397
- trajectory RMSE = 2.568141e-01 V

Quiet-phase fit (spike < 0.2V):
- quiet samples = 32 / 399
- quiet model: dV/dt = aq*V + bq*out + dq
- aq = 2.387257e+08 1/s
- bq = 3.872944e+08 1/s
- dq = -6.175268e+08 V/s
- quiet derivative RMSE = 2.071324e+08 V/s
- quiet derivative R^2 = 0.102267

Decay-window fit (12ns to 19ns):
- decay samples = 15
- decay model: dV/dt = m*V + q
- m = -1.298245e+08 1/s
- q = 8.809756e+07 V/s
- implied decay tau = 7.703 ns
- decay derivative RMSE = 5.700706e+05 V/s
- decay derivative R^2 = 0.931049

Artifacts:
- `/home/v71349/analog-gradients/competition/analysis/lif_ode_fit_trace.csv`
