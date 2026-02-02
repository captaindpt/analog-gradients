# LIF Energy Summary

Source artifact: `/home/v71349/analog-gradients/competition/analysis/lif_energy_summary.txt`

- Total energy (0-200ns): `4.718180e-11` J
- Detected spikes: `10`
- Energy per spike: `4.718180e-12` J (`4.718180` pJ)

Method:
- Integrate `P(t) = VDD * (-I(V_VDD))` over the transient window.
- Count spikes from `spike` threshold crossings at 0.9V.
