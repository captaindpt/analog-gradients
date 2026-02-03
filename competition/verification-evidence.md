# NeuroCore Verification Evidence (Competition Snapshot)

**Date:** 2026-02-02  
**Environment:** Cadence Spectre + OCEAN (`source setup_cadence.sh`)

Full-flow implementation strategy reference:
`competition/full-flow-demo-plan.md`

## Reproducible Commands

```bash
./build.sh synapse
./build.sh lif_neuron
./build.sh neuron_tile
./build.sh neuro_tile4
./build.sh neuro_tile4_coupled
./build.sh neuro_tile4_mixed_signal
./build.sh all
scripts/collect_competition_metrics.sh
scripts/generate_competition_diagrams.sh
scripts/export_competition_waveforms.sh
scripts/generate_waveform_plots.sh
scripts/run_competition_visuals.sh
scripts/run_dc_smoke.sh
scripts/run_innovus_smoke.sh
scripts/run_calibre_smoke.sh
scripts/run_fullflow_smoke.sh
python3 scripts/analyze_lif_ode_fit.py
python3 scripts/analyze_temporal_sensitivity.py
scripts/analyze_lif_energy.sh
```

## Verified Artifacts

| Block | Result File | Status | Key Observation |
|------|-------------|--------|-----------------|
| Synapse | `results/synapse_test.txt` | PASS | Integrate/decay behavior, repeated pulse response |
| LIF Neuron | `results/lif_neuron_test.txt` | PASS | Repeated spiking under pulsed input drive |
| Neuron Tile | `results/neuron_tile_test.txt` | PASS | End-to-end synapse -> membrane -> spike path |
| Neuro Tile4 | `results/neuro_tile4_test.txt` | PASS | 4 channels spike with staggered first spikes |
| Neuro Tile4 Coupled | `results/neuro_tile4_coupled_test.txt` | PASS | channel-0 drive propagates activity to downstream channels |
| Neuro Tile4 Mixed-Signal | `results/neuro_tile4_mixed_signal_test.txt` | PASS | digital `en` gates analog propagation (off before enable, active after) |
| GPU Core (baseline) | `results/gpu_core_test.txt` | PASS | Verified digital foundation remains intact |

## Auditability Snapshot (Latest Full Run)

- Audited command: `./build.sh all`
- Latest manifest: `results/_runlogs/build_all_20260202_184650.manifest.txt`
- Latest log: `results/_runlogs/build_all_20260202_184650.log`
- Manifest includes per-component PASS records with:
  - raw waveform path
  - raw byte size
  - raw mtime (UTC)
  - result-file path and mtime (UTC)
- Note: raw waveforms/logs are intentionally git-ignored; audit evidence is the
  manifest + committed verification summaries.

## Neuro Tile4 Highlights

- Membrane maxima: `0.792V` for channels 0-3
- Spike pulse counts: `14` per channel
- First spike times (ns): `27.5`, `29.5`, `31.5`, `33.5`

## Regression Health

- Full stack regression (`./build.sh all`) passes after analog-path additions.
- Metrics rollup for concept paper/video: `competition/metrics-summary.md`.
- Diagram outputs for submissions: `competition/diagrams/*.svg`.
- Waveform data exports: `competition/data/*.csv`.
- Waveform plot outputs: `competition/plots/*.svg`.
- Robustness sweep snapshot: `competition/sweeps/neuro_tile4_coupled_sweep_summary.md`.

## Full-Flow Smoke Bring-Up (Implementation Readiness)

- Target: `implementation/fullflow_demo/rtl/alu4_flow_demo.v`
- Replay command: `scripts/run_fullflow_smoke.sh`
- Stage status:
  - DC: blocked by `DCSH-1` license; fallback mapped netlist used
  - Innovus: PASS with DEF/post-route netlist/GDS artifacts
  - Calibre DRC: blocked by license; blocked summary captured
- Full artifact index: `competition/full-flow-smoke-evidence.md`

## Founder Thesis Evidence (Math-Oriented)

- ODE fit summary: `competition/analysis/lif_ode_fit_summary.md`
- Temporal sensitivity summary: `competition/analysis/temporal_sensitivity_summary.md`
- Energy-per-event summary: `competition/analysis/lif_energy_summary.md`
- Mixed-signal gating summary: `competition/mixed-signal-smoke-evidence.md`

Current rigor caveats:
- Full-window LIF ODE fit is currently weak (`R^2 = 0.029`); decay-window fit
  is strong (`R^2 = 0.931`) but narrower in scope.
- Coupled-tile temporal slopes are quantized by current measurement resolution
  and sweep granularity; treat as preliminary trend evidence.
