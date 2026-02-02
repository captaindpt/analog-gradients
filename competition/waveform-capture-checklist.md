# Waveform Capture Checklist (Competition Assets)

Use this checklist to produce screenshots for concept paper and video from verified
PASS runs.

## Prerequisites

```bash
source setup_cadence.sh
./build.sh synapse
./build.sh lif_neuron
./build.sh neuron_tile
./build.sh neuro_tile4
./build.sh neuro_tile4_coupled
```

## Required Screenshots

- [ ] `synapse`: `pre`, `post`, `out` over `0-120ns`
- [ ] `lif_neuron`: `mem`, `spike`, `out` over `0-200ns`
- [ ] `neuron_tile`: `syn_post`, `mem`, `spike` over `0-250ns`
- [ ] `neuro_tile4`: `spike0..spike3` over `0-120ns` (show staggered first spikes)
- [ ] `neuro_tile4`: `mem0..mem3` over `0-120ns`
- [ ] `neuro_tile4_coupled`: `spike0..spike3` over `0-120ns` (show feed-forward propagation)
- [ ] `neuro_tile4_coupled`: `mem0..mem3` over `0-120ns`

## Terminal-Generated Plot Equivalents

- `competition/plots/synapse_waveform.svg`
- `competition/plots/lif_neuron_waveform.svg`
- `competition/plots/neuron_tile_waveform.svg`
- `competition/plots/neuro_tile4_spikes.svg`
- `competition/plots/neuro_tile4_mems.svg`
- `competition/plots/neuro_tile4_coupled_spikes.svg`
- `competition/plots/neuro_tile4_coupled_mems.svg`

## Suggested Caption Snippets

- Synapse: "EPSP-like integrate/decay response under pulsed input."
- LIF neuron: "Membrane integration and threshold-driven spiking."
- Neuron tile: "Composed synapse-to-neuron signal flow produces spikes."
- Neuro Tile4: "Four parallel channels show deterministic staggered first-spike timing."
- Neuro Tile4 Coupled: "Channel-0 drive propagates to downstream channels with delayed spikes."

## Source Evidence

- `competition/metrics-summary.md`
- `competition/verification-evidence.md`
