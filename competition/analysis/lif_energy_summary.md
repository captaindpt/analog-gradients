# LIF Energy Summary

Source trace: `/home/v71349/analog-gradients/competition/analysis/lif_energy_trace.csv`

- Total energy (window): `3.270599e-11` J
- Detected spikes: `10`
- Energy per spike (total/spike): `3.270599e-12` J (`3.270599` pJ)
- Event-window mean per spike: `3.270599e-12` J (`3.270599` pJ)
- Event-window std: `2.180490e-13` J (`0.218049` pJ)
- Event-window CV: `0.066669`
- Bootstrap mean (N=2000, seed=42): `3.271731e-12` J
- Bootstrap 95% CI: `[3.154657e-12, 3.424110e-12]` J

Method:
- Integrate `P(t) = VDD * (-I(V_VDD))` from exported trace.
- Detect spike crossings at 0.9V with linear interpolation.
- Partition per-spike windows by midpoints between adjacent spike times.
- Bootstrap the mean per-spike event energy from window energies.

Artifacts:
- Summary TXT: `/home/v71349/analog-gradients/competition/analysis/lif_energy_summary.txt`
- Bootstrap CSV: `/home/v71349/analog-gradients/competition/analysis/lif_energy_bootstrap.csv`
