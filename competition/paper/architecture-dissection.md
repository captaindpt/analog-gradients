# NeuroCore Architecture Dissection (Paper Notes)

Date: 2026-02-02

This note is the paper-facing technical breakdown of the neuromorphic path:

1. `synapse`
2. `lif_neuron`
3. `neuron_tile`
4. `neuro_tile4`
5. `neuro_tile4_coupled`
6. `neuro_tile4_mixed_signal`

## 1) Synapse Primitive

Source:
- `netlists/synapse.scs`
- `ocean/test_synapse.ocn`
- `results/synapse_test.txt`

Mechanism:
- Pulse-controlled transistor charges `post` node.
- `C_POST` stores charge, `R_DECAY` leaks it.
- Two-inverter buffer converts analog `post` into robust digital-like `out`.

Model:
- `dVpost/dt = Iinj/Cpost - Vpost/(Rdecay*Cpost)`
- `tau_syn = Rdecay * Cpost = 16ns` with current defaults.

Evidence highlights:
- Integrate + decay + recharge confirmed.
- Output pulse count: 6.

## 2) LIF Neuron

Source:
- `netlists/lif_neuron.scs`
- `ocean/test_lif_neuron.ocn`
- `results/lif_neuron_test.txt`

Mechanism:
- Input current charges membrane capacitor.
- Leak resistor creates exponential decay pressure.
- Inverter pair acts as threshold detector.
- Reset NMOS discharges membrane after spike event.

Hybrid model:
- Subthreshold: `Cmem * dVmem/dt = Iin - Vmem/Rleak`
- Event/reset: when `Vmem` crosses threshold, spike -> reset path turns on.

Evidence highlights:
- 10 spikes in 200ns window.
- `Vmem(max)` above 1.6V in latest report.

## 3) Neuron Tile (Synapse + LIF Composition)

Source:
- `netlists/neuron_tile.scs`
- `ocean/test_neuron_tile.ocn`
- `results/neuron_tile_test.txt`

Mechanism:
- Synapse output feeds membrane via coupling resistor.
- Demonstrates full local compute path:
  `input pulse -> analog integration -> threshold event`.

Evidence highlights:
- Synapse decay behavior visible at tile level.
- 11 spike-node pulses in latest report.

## 4) Neuro Tile4 (Parallel Temporal Channels)

Source:
- `netlists/neuro_tile4.scs`
- `ocean/test_neuro_tile4.ocn`
- `results/neuro_tile4_test.txt`

Mechanism:
- Four replicated channels with staggered input delays.
- Structure turns known phase offsets into ordered spike timing.

Evidence highlights:
- All channels spike.
- Ordered first-spike timing preserved across channels.

## 5) Neuro Tile4 Coupled (Feed-Forward Propagation)

Source:
- `netlists/neuro_tile4_coupled.scs`
- `ocean/test_neuro_tile4_coupled.ocn`
- `results/neuro_tile4_coupled_test.txt`

Mechanism:
- Only channel-0 receives external pulse.
- Feed-forward coupling injects upstream spike activity into downstream channels.
- Uses resistive and transistor-assisted coupling links.

Evidence highlights:
- All downstream channels activate from channel-0 drive.
- Feed-forward first-spike ordering is preserved in latest report.

## 6) Neuro Tile4 Mixed-Signal (Digital Control of Analog Propagation)

Source:
- `netlists/neuro_tile4_mixed_signal.scs`
- `ocean/test_neuro_tile4_mixed_signal.ocn`
- `results/neuro_tile4_mixed_signal_test.txt`

Mechanism:
- Digital `en` signal gates analog feed-forward transistors.
- Before enable: downstream channels stay quiescent.
- After enable: downstream channels propagate spikes.

Evidence highlights:
- Enable edge detected near 140.5ns.
- Pre-enable downstream spikes: 0.
- Post-enable downstream spikes: active on channels 1..3.

## Big-Picture Assembly

The architecture computes in continuous-time trajectories and event timing:

- state variables: membrane and synaptic voltages,
- events: spike threshold crossings,
- coupling: latency transfer between channels,
- control: optional digital gating over analog pathways.

This is the core narrative for the paper:
clockless analog dynamics perform computation, while digital flow evidence
supports engineering credibility and reproducibility.
