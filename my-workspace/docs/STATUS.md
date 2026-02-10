# GPU Building Blocks - Status

**Last Updated:** 2026-02-09

## Build Hierarchy

```
Level 5: CMOS Primitives     ✅ COMPLETE
Level 4: Logic Gates         ✅ COMPLETE
Level 3: Building Blocks     ✅ COMPLETE
Level 2: RTL Components      ✅ COMPLETE
Level 1: Functional Blocks   ✅ COMPLETE
Level 0: System              ✅ COMPLETE
```

Strategic direction reference: `my-workspace/docs/vision.md` (competition
context in `competition/competition-plan.md`).

## Current Development Focus

Build path from verified digital GPU stack to a neuromorphic analog core:

- Memristor paper library + Markdown manifest ✅
- **Physical memristor TCAD exploration (ticket 0020)** 🔄
  - **Approach**: Systematic Sentaurus TCAD sweep through 5 phases (MIM baseline
    -> traps -> defect drift -> hysteresis tuning -> pulse characterization)
  - Codex runbook: `tcad/memristor/CODEX_RUNBOOK.md`
  - Sweep matrix (38 planned runs): `tcad/memristor/config/sweep_matrix.csv`
  - Run harness: `scripts/run_memristor_tcad_sweep.sh`
  - Sentaurus setup: `scripts/setup_sentaurus.sh`
  - PLT extractor: `scripts/extract_plt_to_csv.py`
  - Phase 1 example run (10nm HfO2 MIM, DC 0-1V):
    `tcad/memristor/runs/example_phase1_mim_10nm/` — CONVERGED, zero current
    (expected: no conduction mechanism in Phase 1)
  - Known issue: `BarrierTunneling` keyword rejected by SDevice vX-2025.09.
    Correct tunneling syntax must be resolved before Phase 2 sweep.
  - Anchor paper: Strukov 2008
  - Spec: `my-workspace/docs/reference/MEMRISTOR_PRIMITIVE_SPEC.md`
  - Paper stock: `my-workspace/docs/reference/MEMRISTOR_PAPER_STOCK.md`
- Analog primitive bring-up: `synapse`, `lif_neuron` ✅ PASS
- Neuron composition and spike behavior verification: `neuron_tile` ✅ PASS
- Small neuromorphic tile integration: `neuro_tile4` ✅ PASS
- Coupled propagation demo: `neuro_tile4_coupled` ✅ PASS
- First computation demo (temporal AND coincidence detector) ✅ PASS
- Second computation demo (spike-domain XOR) ✅ PASS
- Research/vision docs credibility hardening (claim-scope + caveats) ✅ COMPLETE
- Computation-demo expansion (ticket 0014) ✅ COMPLETE
  - Ticket: `my-workspace/tickets/0014-computation-demo-coincidence-and-xor.md`
- Founder-evidence rigor hardening (ticket 0013) ✅ COMPLETE
  - Ticket: `my-workspace/tickets/0013-evidence-rigor-hardening.md`
- Build/test audit hardening (fail-closed + manifests) ✅ COMPLETE
- LIF corner-conditioned ODE/energy evidence (9 corners) ✅ COMPLETE
- One-terminal transistor->GDSII demo path: planning + bring-up 🔄
- Founder-thesis evidence track (clockless continuous-time compute): activated 🔄
- Analog robustness expansion (`synapse`, `lif_neuron`, `neuron_tile`) ✅ COMPLETE
  - Bundle summary: `competition/sweeps/robustness_summary.md`
- Workspace rendezvous scale-ramp planning (ticket 0015) ✅ COMPLETE
  - Follow-on target ticket:
    `my-workspace/tickets/0018-neuro-tile16-hierarchical-integration.md`
- Binary 2x2 architecture comparison demo (ticket 0016) 🔄
  - Neuro path proof v0 PASS: `results/matmul2x2_binary_neuro_test.txt`
  - Two-substrate comparison run published:
    `competition/analysis/matmul2x2_binary_comparison.md`
  - Matrix-size scaling sweep added (model-based):
    `competition/analysis/matmul_binary_scaling_summary.md`
  - 4x4 transistor checkpoint run published:
    `competition/analysis/matmul4x4_binary_comparison.md`
  - 4x4 sparse crossover sweep (measured) published:
    `competition/analysis/matmul4x4_crossover_summary.md`
- Temporal gradient learning loop (ticket 0017) 🔄
  - Hardened finite-difference benchmark runs published (train+holdout):
    `competition/analysis/temporal_gradient_learning_summary.md`
- Next-scale hierarchical integration target (ticket 0018) 🔄
  - Planned block: `neuro_tile16_hier`
  - Planned verifier: `ocean/test_neuro_tile16_hier.ocn`
- Analog vs digital nonlinearity benchmark (ticket 0019) 🔄
  - Protocol: `my-workspace/docs/reference/NONLINEARITY_COMPARISON_PLAN.md`
  - Vector set: `competition/data/nonlinearity/softmax_vectors_n4.csv`
  - Harness: `scripts/run_nonlinearity_vector_benchmark.py`
  - Toy softmax netlists: `netlists/softmax4_analog_toy.scs`, `netlists/softmax4_digital_toy.scs`
  - Runner: `scripts/run_softmax4_nonlinearity_benchmark.sh`
  - GPDK180 netlists: `netlists/softmax4_analog_gpdk180.scs`, `netlists/softmax4_digital_gpdk180.scs`

## Workspace Rendezvous (2026-02-03)

- Operating contract added: `my-workspace/docs/RANDEZVOUS.md`
- Rendezvous ticket completed:
  `my-workspace/tickets/0015-workspace-rendezvous-and-scale-ramp.md`
- Next-scale integration ticket opened:
  `my-workspace/tickets/0018-neuro-tile16-hierarchical-integration.md`
- Workspace hygiene tightened for local probe/scratch artifacts in `.gitignore`
- Full-flow scripts now auto-seed Synopsys/Siemens license env defaults:
  `scripts/setup_fullflow_licenses.sh`
- License investigation reference:
  `my-workspace/logs/2026-02-03-license-unblock-investigation.md`
  - DC and Calibre license failures are config-fixable in this environment
  - DC `DB-1` blocker resolved via LC-compiled minimal Liberty DB path
    (`implementation/fullflow_demo/work/dc/libcache/alu4_min_cells.db`)

## Milestone: Founder Thesis Activated (2026-02-02)

Reframe is now explicit: project value is original compute behavior, not only
tool operation.

- Thesis doc: `competition/founder-thesis.md`
- Core claim: computation encoded in membrane dynamics + spike timing
- Immediate proof targets:
  1. ODE-fit error metrics ✅
  2. Temporal sensitivity (`dt_spike/dparameter`) ✅
  3. Energy-per-event estimates ✅
  4. Mixed-signal coupling experiment ✅
  5. Explicit spike-domain computation demos ✅ (coincidence detector + XOR)

Founder-evidence artifacts:
- `competition/analysis/lif_ode_fit_summary.md`
- `competition/analysis/temporal_sensitivity_summary.md`
- `competition/analysis/lif_energy_summary.md`
- `competition/analysis/lif_corners/20260202_224254/lif_corner_summary.md`
- `results/coincidence_detector_test.txt`
- `results/xor_spike2_test.txt`

Founder-evidence snapshot:
- LIF decay-window ODE fit (12ns-19ns): `R^2 = 0.931`
- LIF global baseline ODE fit (full window): `R^2 = 0.029`
- LIF phase-aware piecewise ODE fit (full window): `R^2 = 0.312`
- Coupled-tile temporal sensitivity (63-point refined sweep):
  - `dt_spike0/dr_fb ≈ -0.599 ns/kOhm` (mean, `R^2≈0.9997`)
  - `dt_spike1/dr_fb ≈ -0.751 ns/kOhm` (mean, `R^2≈0.9997`)
  - `dt_spike2/dr_fb ≈ -0.481 ns/kOhm` (mean, `R^2≈0.9999`)
  - `dt_spike3/dr_fb ≈ -0.170 ns/kOhm` (mean, `R^2≈0.9821`)
  - uncertainty and quantization diagnostics now reported in
    `competition/analysis/temporal_sensitivity_summary.md`
- LIF energy per spike (total/spike): `~3.271 pJ/spike` (0-200ns window)
- LIF energy bootstrap 95% CI: `[3.155, 3.424] pJ`
- 9-corner LIF evidence sweep (rleak={8M,10M,12M}, iin={400u,500u,600u}):
  - energy/spike range: `3.112 - 3.409 pJ`
  - piecewise ODE R^2 range: `0.250 - 0.290`
  - global ODE R^2 remains low: `~0.032 - 0.034`
- Mixed-signal gating: downstream spikes `0` pre-enable -> `7` post-enable
- Coincidence detector (temporal AND) result:
  - A-only spikes: `0`
  - B-only spikes: `0`
  - A+B coincident spikes: `1`
  - A+B offset spikes: `0`
  - first coincident spike: `12.229 ns`
- XOR spike-domain result:
  - 00 spikes: `0`
  - 10 spikes: `1`
  - 01 spikes: `1`
  - 11 spikes: `0`
  - first output spikes (10/01): `~12.1 ns`

Audit hardening snapshot:
- `build.sh` now runs with `set -euo pipefail`
- stale `*_test.txt` + `.raw` artifacts are deleted before each component run
- fresh raw/result timestamps are required (fail-closed checks)
- result parsing is strict:
  - exactly one terminal `=== PASS|FAIL:` verdict is required
  - any `FAIL:` / `[FAIL]` / `ERROR:` marker fails the component
- OCEAN runtime script errors are fail-closed:
  - any `*Error*` in `results/<component>/ocean.log` fails verification
- Spectre warning policy is now strict and fail-closed:
  - any unallowlisted `WARNING (SPECTRE-xxxxx)` in `spectre.log` fails simulation
  - allowlist is explicit in `config/spectre_warning_allowlist.txt`
  - warning-count drift is also fail-closed per component/code using
    `config/spectre_warning_baseline.csv` (must not exceed prior green baseline)
- OCEAN verification scripts are now path-portable:
  - removed hardcoded `/home/v71349/analog-gradients/...` paths in favor of `results/...`
- top-level digital verification now checks full array outputs (not PE0-only):
  - `ocean/test_pe4.ocn`
  - `ocean/test_gpu_core.ocn`
- prior analog warning-only conditions are now fail conditions in:
  - `ocean/test_synapse.ocn`
  - `ocean/test_lif_neuron.ocn`
  - `ocean/test_coincidence_detector.ocn`
  - `ocean/test_xor_spike2.ocn`
- timestamped build run logs/manifests:
  - latest full-run: `results/_runlogs/build_all_20260203_152948.{log,manifest.txt}`

## Competition Edge: Full Semiconductor Flow Demo (In Progress)

| Stage | Toolchain | Status | Target Artifact |
|-------|-----------|--------|-----------------|
| Flow strategy and script plan | docs + bash/tcl planning | ✅ | `competition/full-flow-demo-plan.md` |
| Synthesis smoke test | Synopsys Design Compiler | ✅ | mapped netlist + timing reports |
| Place and route smoke test | Cadence Innovus | ✅ | DEF + routed netlist + GDS + reports |
| Physical verification smoke test | Siemens Calibre | ✅ with license env configured | DRC smoke summary + logs |
| Single-command demo orchestration | repo scripts | ✅ | `scripts/run_fullflow_smoke.sh` |

Full-flow smoke evidence:
`competition/full-flow-smoke-evidence.md`

## Video Demo Capture Readiness

- Scripted shot plan: `competition/video-shot-script.md`
- Waveform capture checklist: `competition/waveform-capture-checklist.md`
- Recording pack builder: `scripts/build_recording_pack.sh`
- Guided recording runner: `scripts/demo_narrator.sh`
- Timed narration script: `competition/voiceover-script.md`
- Available coupled-tile plot assets:
  - `competition/plots/neuro_tile4_coupled_spikes.svg`
  - `competition/plots/neuro_tile4_coupled_mems.svg`

## Paper Workthrough Readiness

- LaTeX source: `competition/paper/neurocore_workthrough.tex`
- Paper build helper: `scripts/build_paper.sh`
- Parsed paper data prep: `scripts/prepare_paper_data.py`
- Raw-point sweep + spike summary data:
  - `competition/paper/data/neuro_tile4_coupled_sweep_parsed.csv`
  - `competition/paper/data/first_spike_summary.csv`
- Build caveat: no local LaTeX engine currently available in this environment.

## Competition Path: Analog Primitive Bring-Up

| Component | Netlist | Simulation | Verification | Notes |
|-----------|---------|------------|--------------|-------|
| Synapse | ✅ | ✅ | ✅ PASS | EPSP integrate/decay + 6 output pulses in 120ns |
| LIF Neuron | ✅ | ✅ | ✅ PASS | 10 spikes in 200ns, max Vmem=1.651V |

## Competition Path: Analog Composition

| Component | Netlist | Simulation | Verification | Notes |
|-----------|---------|------------|--------------|-------|
| Neuron Tile | ✅ | ✅ | ✅ PASS | synapse->membrane->spike path with 11 detected spike pulses |
| Neuro Tile4 | ✅ | ✅ | ✅ PASS | 4-neuron tile with staggered first spikes: 47.5/49.5/51.5/53.5ns |
| Neuro Tile4 Coupled | ✅ | ✅ | ✅ PASS | feed-forward coupling: downstream channels spike from channel-0 drive |
| Neuro Tile4 Mixed-Signal | ✅ | ✅ | ✅ PASS | digital `en` gates analog propagation in one Spectre run |
| Coincidence Detector | ✅ | ✅ | ✅ PASS | spike-domain temporal AND: only coincident A+B input produces spike |
| XOR Spike2 | ✅ | ✅ | ✅ PASS | spike-domain XOR: output spikes for 10/01, suppressed for 00/11 |
| Matmul2x2 Binary Neuro | ✅ | ✅ | ✅ PASS | binary 2x2 proof point decodes expected `[[1 1] [1 2]]` |
| Matmul2x2 Binary Digital | ✅ | ✅ | ✅ PASS | binary 2x2 digital baseline decodes expected `[[1 1] [1 2]]` |
| Matmul4x4 Binary Neuro | ✅ | ✅ | ✅ PASS | 4x4 checkpoint decodes expected `[[2 2 2 3] [1 1 2 1] [1 3 2 2] [1 2 1 2]]` |
| Matmul4x4 Binary Digital | ✅ | ✅ | ✅ PASS | 4x4 digital checkpoint decodes expected `[[2 2 2 3] [1 1 2 1] [1 3 2 2] [1 2 1 2]]` |

## Competition Path: Robustness Snapshot

| Block | Sweep | Result | Artifact |
|-------|-------|--------|----------|
| Synapse | cpost={150f,200f,250f}, rdecay={60k,80k,100k} | 9/9 PASS (band) | `competition/sweeps/synapse_sweep_summary.md` |
| LIF Neuron | rleak={8M,10M,12M}, iin={400u,500u,600u} | 9/9 PASS (band) | `competition/sweeps/lif_neuron_sweep_summary.md` |
| Neuron Tile | r_couple={6k,8k,10k}, rleak={6M,8M,10M} | 9/9 PASS (band) | `competition/sweeps/neuron_tile_sweep_summary.md` |
| Neuro Tile4 Coupled | r_fb={600..1500}, rleak={5M..12M} | 63/63 PASS | `competition/sweeps/neuro_tile4_coupled_sweep_summary.md` |
| Bundle Rollup | all above | 90/90 PASS | `competition/sweeps/robustness_summary.md` |

## Architecture Scaling Sweep (Ticket 0016)

- Added scaling harness for binary matmul architecture discussion:
  - `scripts/run_matmul_binary_scaling_sweep.sh`
  - `scripts/analyze_matmul_binary_scaling.py`
- Added transistor checkpoint harness for `N=4`:
  - `scripts/generate_matmul4x4_checkpoint_assets.py`
  - `scripts/run_matmul4x4_binary_comparison.sh`
- Added sparse measured crossover harness (`N=4`):
  - `scripts/run_matmul4x4_crossover_sweep.sh`
- Added neuro `iin_amp` tuning harness (sparse fixed point):
  - `scripts/sweep_matmul4x4_neuro_iin.sh`
- Added sparse temporal benchmark harness (quality-gated, trace-driven):
  - `scripts/run_sparse_temporal_benchmark.sh`
  - `scripts/analyze_sparse_temporal_benchmark.py`
- Updated 4x4 neuro source model to binary-product-gated injection in generator:
  - `scripts/generate_matmul4x4_checkpoint_assets.py`
- Latest sweep artifacts:
  - `competition/sweeps/matmul_binary_scaling_sweep.csv`
  - `competition/analysis/matmul_binary_scaling_summary.md`
  - `competition/analysis/matmul_binary_scaling_energy.svg`
  - `competition/analysis/matmul_binary_scaling_pressure.svg`
- Latest `N=4` measured comparison:
  - `competition/analysis/matmul4x4_binary_comparison.md`
  - `competition/analysis/matmul4x4_binary_comparison.csv`
- Latest `N=4` sparse measured sweep:
  - `competition/sweeps/matmul4x4_crossover/matmul4x4_crossover.csv`
  - `competition/analysis/matmul4x4_crossover_summary.md`
  - `competition/analysis/matmul4x4_crossover_regime_summary.md`
- Latest sparse-point neuro tuning sweep:
  - `competition/analysis/matmul4x4_neuro_iin_sweep.csv`
  - `competition/analysis/matmul4x4_neuro_iin_sweep_summary.md`
- Latest sparse temporal benchmark artifacts:
  - `competition/analysis/sparse_temporal_benchmark_summary.md`
  - `competition/analysis/sparse_temporal_benchmark.csv`
  - `competition/analysis/sparse_temporal_benchmark_ratio.svg`
  - `competition/analysis/sparse_temporal_benchmark_eptp.svg`
- Scope caveat:
  - sweep curves are still model-extrapolated for larger `N`; measured transistor
    checkpoints currently cover `N=2` and `N=4`, with `N=8` pending.
  - measured sparse `N=4` sweep currently shows no active-point crossover;
    this reveals substantial neuro static/event overhead not captured by simple
    spike-count-only model extrapolation.
  - sparse fixed-point `iin_amp` reduction lowers neuro energy but also collapses
    spike activity/decoder correctness before approaching digital-energy parity.
  - product-gated source update reduced dense 4x4 neuro energy (about 30% drop
    vs prior checkpoint), but active-point sparse crossover is still not observed.
  - sparse temporal benchmark currently predicts crossover at extreme idle duty
    cycle (`~0.0085%` active windows), consistent with measured regime split;
    this is a calibrated trace model, not yet a transistor detector-vs-detector
    matched pair.

## Temporal Gradient Learning (Ticket 0017)

- Added finite-difference trainer:
  - `scripts/train_temporal_gradient_loop.py`
- Added benchmark runner:
  - `scripts/run_temporal_gradient_benchmark.sh`
- Objective/optimizer hardening after review:
  - `target_mode=absolute` promoted to default for headline runs
  - `target_mode=measured_anchor_shift` retained for dev/debug only
  - holdout leakage reduced: anchor probing now defaults to train-only delays
  - count mismatch loss (`abs(actual_count-expected_count)`)
  - magnitude-sensitive ordering loss (`violation^2`)
  - finite-difference denominator uses actual perturbation span at bounds
  - normalized-gradient update rule (less clip-dominated behavior)
  - normalized energy weighting (`energy_weight * energy/energy_ref`) with optional schedule
  - per-term loss contribution percentages now logged per iteration
- Latest artifacts:
  - `competition/analysis/temporal_gradient_learning.csv`
  - `competition/analysis/temporal_gradient_trace.csv`
  - `competition/analysis/temporal_gradient_learning_summary.md`
  - `competition/analysis/temporal_gradient_learning_loss.svg`
- Latest run archive:
  - `competition/sweeps/temporal_gradient_learning/20260204_183829/`
- Current method-demo result (`ITERS=4`, `target_mode=absolute`, `energy_weight=0.03`):
  - train loss `0.098085 -> 0.095554`, holdout loss `0.096863 -> 0.095044`
  - final loss composition: timing `~68.6%`, energy `~31.4%`, count/order `0%`
  - final penalties remained zero for this sampled delay family.
- Penalty activation checks:
  - count mismatch stress archive:
    `competition/sweeps/temporal_gradient_learning/20260204_185340_count_stress3/`
  - order-margin stress archive:
    `competition/sweeps/temporal_gradient_learning/20260204_185702_order_stress/`
- Scope caveat:
  - this is currently a **method demo** on `neuro_tile4_coupled`, not yet an
    externally valid benchmark.
  - **externally valid benchmark pending:** train/val/test over pattern families,
    plus matched digital temporal-detector baseline under identical scoring.

## Level 5: CMOS Primitives ✅

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| Inverter  | ✅ | ✅ | ✅ PASS |
| NAND2     | ✅ | ✅ | ✅ PASS |
| NOR2      | ✅ | ✅ | ✅ PASS |

### Verification Results

**Inverter:**
- Vin=HIGH → Vout=0.007V (LOW) ✓
- Vin=LOW → Vout=1.783V (HIGH) ✓

**NAND2:** `OUT = ~(A & B)`
- A=0, B=0 → 1.792V (HIGH) ✓
- A=1, B=0 → 1.769V (HIGH) ✓
- A=0, B=1 → 1.772V (HIGH) ✓
- A=1, B=1 → 0.015V (LOW) ✓

**NOR2:** `OUT = ~(A | B)`
- A=0, B=0 → 1.766V (HIGH) ✓
- A=1, B=0 → 0.014V (LOW) ✓
- A=0, B=1 → 0.012V (LOW) ✓
- A=1, B=1 → 0.004V (LOW) ✓

## Level 4: Logic Gates

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| AND2      | ✅ | ✅ | ✅ PASS |
| OR2       | ✅ | ✅ | ✅ PASS |
| XOR2      | ✅ | ✅ | ✅ PASS |
| XNOR2     | ✅ | ✅ | ✅ PASS |

## Level 3: Building Blocks

| Component  | Netlist | Simulation | Verification |
|------------|---------|------------|--------------|
| MUX2       | ✅ | ✅ | ✅ PASS |
| Half Adder | ✅ | ✅ | ✅ PASS |
| Full Adder | ✅ | ✅ | ✅ PASS |

## Level 2: RTL Components

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| ALU1      | ✅ | ✅ | ✅ PASS |
| ALU4      | ✅ | ✅ | ✅ PASS |

## Level 1: Functional Blocks

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| PE1       | ✅ | ✅ | ✅ PASS |
| PE4       | ✅ | ✅ | ✅ PASS |

## Level 0: System

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| GPU Core  | ✅ | ✅ | ✅ PASS |

## Tooling

- Headless-friendly Virtuoso runner: `scripts/virtuoso_replay.sh`

## Quick Commands

```bash
# Build and test all components
./build.sh all

# Build specific component
./build.sh inverter
./build.sh nand2
./build.sh nor2
./build.sh synapse
./build.sh lif_neuron
./build.sh neuron_tile
./build.sh neuro_tile4
./build.sh neuro_tile4_coupled
./build.sh coincidence_detector
./build.sh xor_spike2

# Source Cadence environment
source setup_cadence.sh
```

## Repository Structure

```
analog-gradients/
├── AGENTS.md             # Agent workflow rules
├── setup_cadence.sh      # Bash env setup for Cadence
├── build.sh              # Master build/test script
├── netlists/             # Spectre netlists (.scs)
├── ocean/                # OCEAN verification scripts (.ocn)
├── skill/                # Virtuoso SKILL scripts (.il)
├── results/              # Simulation outputs + *_test.txt reports
├── competition/          # ICTGC strategy + source docs
└── my-workspace/         # Knowledgebase, tickets, and logs
```

## Toolchain Leverage (Armory Assessment)

This project has access to a full semiconductor EDA stack on CMC Cloud:

| Domain | Tools | Status |
|--------|-------|--------|
| Analog simulation | Cadence Spectre, Synopsys HSPICE | ✅ Working |
| Digital simulation | VCS, Xcelium, Questa | ✅ Working |
| Synthesis | Synopsys Design Compiler | ✅ (license-dependent) |
| Place & route | Cadence Innovus | ✅ Working |
| Physical verification | Siemens Calibre | ✅ (license-dependent) |
| FPGA | Xilinx Vivado, Intel Quartus | ✅ Working |

**What this means:** Traditional chip design requires separate specialized teams
(analog, digital, physical design, verification, FPGA). This project demonstrates
that one person + AI agents can orchestrate the full flow.

**Path to silicon:**
1. Design + simulate: ✅ complete
2. Layout: available via Virtuoso GUI (manual)
3. Tape-out: purchasable service (MOSIS $5-50K, Efabless free MPW, commercial $50K+)

## Energy Positioning (Literature Context)

| Platform | Energy Metric | Value |
|----------|---------------|-------|
| **NeuroCore LIF** | per spike | **3.27 pJ** |
| Intel Loihi | per synaptic op | 23.6 pJ |
| IBM TrueNorth | per synaptic event | ~26 pJ |
| Analog CMOS (28nm) | per spike | 1.61 fJ (aggressive) |
| SOI LIF (2017) | per spike | ~35 pJ |

NeuroCore is competitive in the analog CMOS band and 7-8× better than digital
neuromorphic chips per event.

## Open Tickets

See `my-workspace/tickets/` for work items.
