# LIF Energy Summary (rleak_12M_iin_500u)

Source trace: `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_500u/lif_energy_trace.csv`

- Total energy (window): `3.270926e-11` J
- Detected spikes: `10`
- Energy per spike (total/spike): `3.270926e-12` J (`3.270926` pJ)
- Event-window mean per spike: `3.270926e-12` J (`3.270926` pJ)
- Event-window std: `2.180892e-13` J (`0.218089` pJ)
- Event-window CV: `0.066675`
- Bootstrap mean (N=2000, seed=42): `3.272058e-12` J
- Bootstrap 95% CI: `[3.154951e-12, 3.424493e-12]` J

Method:
- Integrate `P(t) = VDD * (-I(V_VDD))` from exported trace.
- Detect spike crossings at 0.9V with linear interpolation.
- Partition per-spike windows by midpoints between adjacent spike times.
- Bootstrap the mean per-spike event energy from window energies.

Artifacts:
- Summary TXT: `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_500u/lif_energy_summary.txt`
- Bootstrap CSV: `/home/v71349/analog-gradients/competition/analysis/lif_corners/20260202_224254/rleak_12M_iin_500u/lif_energy_bootstrap.csv`
