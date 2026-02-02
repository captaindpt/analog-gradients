# GPU Building Blocks - Status

**Last Updated:** 2026-02-02

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

- Analog primitive bring-up: `synapse`, `lif_neuron` ✅ PASS
- Neuron composition and spike behavior verification: `neuron_tile` ✅ PASS
- Small neuromorphic tile integration: `neuro_tile4` ✅ PASS
- Coupled propagation demo: `neuro_tile4_coupled` ✅ PASS
- One-terminal transistor->GDSII demo path: planning + bring-up 🔄

## Competition Edge: Full Semiconductor Flow Demo (In Progress)

| Stage | Toolchain | Status | Target Artifact |
|-------|-----------|--------|-----------------|
| Flow strategy and script plan | docs + bash/tcl planning | ✅ | `competition/full-flow-demo-plan.md` |
| Synthesis smoke test | Synopsys Design Compiler | ⚠️ executable OK, license blocked (`DCSH-1`) | fallback gate-level netlist + logs |
| Place and route smoke test | Cadence Innovus | ✅ | DEF + routed netlist + GDS + reports |
| Physical verification smoke test | Siemens Calibre | ⚠️ executable OK, DRC license blocked | blocked DRC summary + logs |
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
| LIF Neuron | ✅ | ✅ | ✅ PASS | 10 spikes in 200ns, max Vmem=1.573V |

## Competition Path: Analog Composition

| Component | Netlist | Simulation | Verification | Notes |
|-----------|---------|------------|--------------|-------|
| Neuron Tile | ✅ | ✅ | ✅ PASS | synapse->membrane->spike path with 12 detected spike pulses |
| Neuro Tile4 | ✅ | ✅ | ✅ PASS | 4-neuron tile with staggered first spikes: 27.5/29.5/31.5/33.5ns |
| Neuro Tile4 Coupled | ✅ | ✅ | ✅ PASS | feed-forward coupling: downstream channels spike from channel-0 drive |

## Competition Path: Robustness Snapshot

| Block | Sweep | Result | Artifact |
|-------|-------|--------|----------|
| Neuro Tile4 Coupled | r_fb={700,1k,1500}, rleak={6M,8M,10M} | 9/9 PASS | `competition/sweeps/neuro_tile4_coupled_sweep_summary.md` |

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
| PE4       | ✅ | ✅ | ✅ PASS* |

## Level 0: System

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| GPU Core  | ✅ | ✅ | ✅ PASS* |

*Spot-check verification for PE4 and GPU Core uses PE0 outputs only.*

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

## Open Tickets

See `my-workspace/tickets/` for work items.
