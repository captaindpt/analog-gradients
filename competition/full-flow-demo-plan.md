# NeuroCore Full-Flow Demo Plan

## Objective

Create a judge-visible "from transistors to GDS-ready artifacts" demo that proves
NeuroCore is not only simulated, but implementable through a real semiconductor flow.

## Current Reality (2026-02-03)

| Track | Status | Evidence |
|------|--------|----------|
| Analog path (`synapse` -> `neuro_tile4_coupled`) | PASS | `competition/verification-evidence.md` |
| Digital path (CMOS -> GPU core) | PASS | `results/gpu_core_test.txt` |
| Robustness snapshot (`neuro_tile4_coupled`) | 63/63 PASS | `competition/sweeps/neuro_tile4_coupled_sweep_summary.md` |
| Synopsys DC smoke | DEGRADED (`DB-1` target-library mismatch, fallback netlist) | `implementation/fullflow_demo/work/dc/reports/alu4_flow_demo_dc_target_lib.warn` |
| Cadence Innovus smoke | PASS | `implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.gds` |
| Siemens Calibre smoke | PASS | `implementation/fullflow_demo/work/calibre/alu4_flow_demo_drc.summary` |
| One-command orchestration | PASS | `scripts/run_fullflow_smoke.sh` |

## Why This Is the Edge

Most teams show one slice (simulation, RTL, or layout). This plan shows all of it:

1. Analog transistor-level proof (`synapse` -> `lif_neuron` -> tiles)
2. Digital implementation capability (synthesis + P&R)
3. Physical verification readiness (DRC/LVS path)
4. Scripted, reproducible terminal workflow

## Founder Reframe (Milestone Upgrade)

Full-flow evidence remains important, but it is now the support layer for the
original idea:

- **Primary claim:** clockless continuous-time compute via analog spike dynamics.
- **Support claim:** the stack is implementation-credible and reproducible.

Thesis reference: `competition/founder-thesis.md`

## Current Starting Point

### Analog (Spectre verified)

- `synapse`
- `lif_neuron`
- `neuron_tile`
- `neuro_tile4`
- `neuro_tile4_coupled`

### Digital (Spectre verified)

- CMOS primitives -> logic -> adders/mux -> ALU -> PE -> GPU core

### Tooling Inventory (Armory snapshot)

- Cadence: Virtuoso, Innovus, Xcelium, Pegasus
- Synopsys: DC, VCS, HSPICE
- Siemens: Questa, Calibre
- FPGA and other tools available, plus multiple PDK kits

## Recommended Demo Architecture

### Recommended execution mode: Option A with Analog Bookends

Use analog proof at the start/end, and run a practical digital full-flow in the
middle.

1. **Open with analog evidence**
   - `./build.sh neuro_tile4` (or `neuro_tile4_coupled`) PASS
2. **Synthesis**
   - Verilog target -> Synopsys DC -> gate-level netlist + timing report
3. **Place and route**
   - Gate-level netlist -> Cadence Innovus -> floorplan/placement/routing outputs
4. **Physical verification path**
   - Calibre DRC/LVS smoke verification artifacts
5. **Close with outcome**
   - GDSII-ready artifact path and Taiwan-fit ask

## 3-Minute Narrative Structure

1. **0:00-0:30** Analog proof (Spectre PASS + waveforms)
2. **0:30-1:30** Digital flow time-lapse (DC -> Innovus -> Calibre)
3. **1:30-2:15** Credibility pitch ("I can do simulation and implementation")
4. **2:15-2:45** Taiwan integration ask (TSMC + GUC + ecosystem)
5. **2:45-3:00** Closing claim ("From transistors to GDS-ready flow")

## Eye-Popping Version ("One Terminal. Transistors to Tape-Out. One Engineer.")

1. **Scene 1 (30s): The Stack**
   - Show `./build.sh all` PASS cascade.
   - Message: verified analog + digital stack, automated and reproducible.
2. **Scene 2 (45s): The Analog Brain**
   - Show `neuro_tile4_coupled` spike/membrane waveforms and staggered timing.
   - Message: feed-forward spiking propagation as real transistor-level behavior.
3. **Scene 3 (60s): The Flow**
   - Show `scripts/run_fullflow_smoke.sh`, highlight Innovus execution and GDS emit.
   - Message: this is a manufacturable implementation flow, not a slide deck.
4. **Scene 4 (30s): The Point**
   - Message: one engineer, real stack, ready for shuttle access.
5. **Scene 5 (15s): Close**
   - Message: NeuroCore, analog AI on standard CMOS, transistor-to-GDS evidence.

## Immediate Bring-Up Steps

1. Validate DC smoke flow on a small known block
2. Validate Innovus smoke flow on DC output
3. Validate Calibre invocation path on generated layout artifacts
4. Script all steps into one replayable command chain
5. Integrate outputs into `competition/` evidence files

## Bring-Up Status (2026-02-03)

- `scripts/run_fullflow_smoke.sh` now replays the 3 stages in one command.
- DC: license env is configured in-script; current blocker is `DB-1` target-library
  compatibility (`.lib` vs expected `.db`) and fallback netlist usage.
- Innovus: smoke P&R completed; DEF, reports, and GDS emitted.
- Calibre: smoke DRC run completes with results database + summary output.
- Artifact index: `competition/full-flow-smoke-evidence.md`.

## Success Criteria

- Each stage emits real artifacts (not screenshots only)
- The command sequence is reproducible on this repo environment
- The demo can be replayed in one terminal session for judges
