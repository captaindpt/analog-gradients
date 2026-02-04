# NeuroCore Verification Evidence (Competition Snapshot)

**Date:** 2026-02-03  
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
./build.sh coincidence_detector
./build.sh xor_spike2
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
scripts/sweep_neuro_tile4_coupled.sh
python3 scripts/analyze_lif_ode_fit.py
python3 scripts/analyze_temporal_sensitivity.py
scripts/analyze_lif_energy.sh
scripts/run_lif_corner_evidence.sh
scripts/run_sparse_temporal_benchmark.sh
scripts/run_temporal_gradient_benchmark.sh
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
| Coincidence Detector | `results/coincidence_detector_test.txt` | PASS | spike-domain temporal AND: only coincident A+B input spikes |
| XOR Spike2 | `results/xor_spike2_test.txt` | PASS | spike-domain XOR: spikes for 10/01 and suppression for 00/11 |
| GPU Core (baseline) | `results/gpu_core_test.txt` | PASS | Verified digital foundation remains intact |

## Neuro Tile4 Highlights

- Membrane maxima: `0.818V` for channels 0-3
- Spike pulse counts: `13` per channel
- First spike times (ns): `47.5`, `49.5`, `51.5`, `53.5`

## Regression Health

- Full stack regression (`./build.sh all`) passes after analog-path additions.
- Build runner is now fail-closed (`set -euo pipefail` + stale artifact purge +
  fresh raw/result timestamp checks).
- Timestamped build logs/manifests are emitted per run under
  `results/_runlogs/` (example:
  `results/_runlogs/build_all_20260203_152948.manifest.txt`).
- Metrics rollup for concept paper/video: `competition/metrics-summary.md`.
- Diagram outputs for submissions: `competition/diagrams/*.svg`.
- Waveform data exports: `competition/data/*.csv`.
- Waveform plot outputs: `competition/plots/*.svg`.
- Robustness sweep snapshot: `competition/sweeps/neuro_tile4_coupled_sweep_summary.md`.

## Coupled-Tile Robustness (Refined Sweep)

- Sweep grid: `r_fb={600,700,800,900,1000,1100,1200,1300,1500}`
- Leak grid: `rleak={5M,6M,7M,8M,9M,10M,12M}`
- Total points: `63`, PASS points: `63`
- Run archive root:
  `results/neuro_tile4_coupled/sweeps/20260202_215026/`
- Latest CSV/summary:
  - `competition/sweeps/neuro_tile4_coupled_sweep.csv`
  - `competition/sweeps/neuro_tile4_coupled_sweep_summary.md`

## Full-Flow Smoke Bring-Up (Implementation Readiness)

- Target: `implementation/fullflow_demo/rtl/alu4_flow_demo.v`
- Replay command: `scripts/run_fullflow_smoke.sh`
- Stage status:
  - DC: launches with configured license env, but degrades to fallback netlist
    due `DB-1` target-library mismatch
  - Innovus: PASS with DEF/post-route netlist/GDS artifacts
  - Calibre DRC: PASS with summary output (`0` violations in smoke checks)
- Full artifact index: `competition/full-flow-smoke-evidence.md`

## Founder Thesis Evidence (Math-Oriented)

- ODE fit summary: `competition/analysis/lif_ode_fit_summary.md`
- Temporal sensitivity summary: `competition/analysis/temporal_sensitivity_summary.md`
- Energy-per-event summary: `competition/analysis/lif_energy_summary.md`
- Corner-conditioned ODE/energy summary:
  `competition/analysis/lif_corners/20260202_224254/lif_corner_summary.md`
- Mixed-signal gating summary: `competition/mixed-signal-smoke-evidence.md`
- Computation demo summaries:
  - `results/coincidence_detector_test.txt`
  - `results/xor_spike2_test.txt`
  - `competition/analysis/sparse_temporal_benchmark_summary.md`
  - `competition/analysis/temporal_gradient_learning_summary.md`

Computation-demo highlight (temporal AND / coincidence):
- A-only -> `0` spikes
- B-only -> `0` spikes
- A+B coincident -> `1` spike
- A+B offset -> `0` spikes
- First coincident spike time: `12.229 ns`

Computation-demo highlight (XOR):
- 00 -> `0` spikes
- 10 -> `1` spike
- 01 -> `1` spike
- 11 -> `0` spikes
- First output spikes (10/01): `~12.1 ns`

Current quantitative highlights from refined temporal analysis:
- `dt_spike0/dr_fb` mean `≈ -0.599 ns/kOhm` (`R2≈0.9997`)
- `dt_spike1/dr_fb` mean `≈ -0.751 ns/kOhm` (`R2≈0.9997`)
- `dt_spike2/dr_fb` mean `≈ -0.481 ns/kOhm` (`R2≈0.9999`)
- `dt_spike3/dr_fb` mean `≈ -0.170 ns/kOhm` (`R2≈0.9821`)

Current quantitative highlights from ODE/energy rigor pass:
- ODE derivative fit `R2` improved from `0.029` (global baseline)
  to `0.312` (phase-aware piecewise).
- Energy per spike (total/spike): `3.270599 pJ`
- Bootstrap 95% CI for mean energy/spike: `[3.154657, 3.424110] pJ`

Corner-conditioned highlights (9 points):
- Energy/spike range: `3.111603 - 3.408821 pJ`
- Piecewise ODE `R2` range: `0.249740 - 0.290398`
- Global ODE `R2` remains low: `0.032090 - 0.033846`

Current rigor caveats:
- Global single-phase ODE remains weak; current improvement relies on
  phase-aware piecewise fitting (`competition/analysis/lif_ode_fit_summary.md`).
- Energy uncertainty is currently derived from single-run event-window
  bootstrap; cross-run/environment variance is still future work.

## Literature Context (Energy, Non-Normalized)

| Platform | Metric | Value | Source |
|----------|--------|-------|--------|
| **NeuroCore LIF** | energy/spike | **3.27 pJ** | This work |
| Intel Loihi | energy/synaptic op | 23.6 pJ | Davies et al. 2018 |
| IBM TrueNorth | energy/synaptic event | ~26 pJ | Merolla et al. 2014 |
| SENECA (digital) | energy/synaptic op | ~2.8 pJ | PMC 2023 |
| Analog CMOS LIF (28nm) | energy/spike | 1.61 fJ | arXiv 2024 |
| SOI LIF (2017) | energy/spike | ~35 pJ | PMC 2017 |

**Interpretation guardrail:** This table is context-only. Metrics are not
fully normalized (different workloads, technology nodes, routing assumptions,
and event definitions). Treat it as directional positioning, not an
apples-to-apples ranking.

**Energy definition:** Total energy from VDD during one integrate-fire-reset cycle, including membrane charging, threshold detection, and reset discharge.

## Timing Gradients and Learning Potential

Measured temporal sensitivities (∂t_spike/∂r_fb):
- Channel 0: -0.599 ns/kΩ (R² ≈ 0.9997)
- Channel 1: -0.751 ns/kΩ (R² ≈ 0.9997)
- Channel 2: -0.481 ns/kΩ (R² ≈ 0.9999)
- Channel 3: -0.170 ns/kΩ (R² ≈ 0.9821)

These are empirical local gradients compatible with **EventProp**-style
continuous-time backpropagation (Wunderlich et al., Nature Sci. Rep. 2021).
The high R² values indicate smooth, predictable timing response, which is a
prerequisite for gradient-based learning. This does **not** yet constitute a
full in-circuit training demonstration.

## Prior Art Positioning

Coincidence detection hardware exists in various forms:
- Clocked CMOS detectors (synchronous, different paradigm)
- Resonate-and-fire analog neurons (different model)
- System-level delay-line modules (higher abstraction)

**NeuroCore differentiator (current stage):** CMOS LIF temporal-AND with
quantified energy, timing sensitivity, and corner verification. This is a
characterized compute primitive; full learning/plasticity proof is still
future work.
