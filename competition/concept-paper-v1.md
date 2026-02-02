# NeuroCore Concept Paper (Draft v1)

**Project Name:** NeuroCore  
**Category:** AI Core Technologies and Chips  
**Applicant Type:** Individual (University-led founder)  
**Draft Date:** February 2, 2026  
**ICTGC Round 4 Deadline:** February 28, 2026 (grace period through March 20, 2026)

---

## 1) Problem Statement

Edge AI workloads are increasingly constrained by energy, not arithmetic throughput.
In conventional digital accelerators, memory movement and clocked switching dominate
system power for sparse, event-driven signals (audio triggers, biosignals, always-on
sensing). This creates a major gap for low-power edge systems that require continuous
inference under strict power budgets.

Neuromorphic analog computing is a strong fit for sparse edge signals, but many
approaches depend on exotic materials or custom fabrication options that are not
widely manufacturable. We target a different path: analog spiking compute in
**standard CMOS**, aligned with Taiwan's mature-node manufacturing strengths.

## 2) Proposed Technical Solution

NeuroCore is a transistor-up analog neuromorphic compute core built on a verified
digital foundation already developed in this repository.

### Core idea

- Use CMOS analog primitives to implement event-driven dynamics:
  - **Synapse primitive** (`netlists/synapse.scs`): integrate + decay response
  - **LIF neuron primitive** (`netlists/lif_neuron.scs`): threshold + spike behavior
- Compose primitives into small neuromorphic tiles for edge inference.
- Preserve compatibility with existing digital control/interconnect blocks from the
  verified GPU hierarchy in this repo.

### Why this is differentiated

1. **Transistor-up methodology**: validated from logic primitives to system wrapper.
2. **Standard CMOS target**: no dependence on memristor/RRAM process assumptions.
3. **Competition-ready verification flow**: reproducible Spectre + OCEAN PASS/FAIL.

## 3) Current Technical Progress (Evidence)

### 3.1 Verified digital foundation (already complete)

- Level 5 through Level 0 stack verified:
  - Inverter/NAND/NOR -> logic gates -> adders/mux -> ALU -> PE -> GPU core
- Build flow: `./build.sh all`
- Result artifacts: `results/*_test.txt`

### 3.2 Analog primitive bring-up (competition kickoff complete)

1. **Synapse primitive**
   - Netlist: `netlists/synapse.scs`
   - Test: `ocean/test_synapse.ocn`
   - Result: `results/synapse_test.txt` (PASS)
   - Observed behavior: integrate/decay dynamics + repeated output pulses

2. **LIF neuron primitive**
   - Netlist: `netlists/lif_neuron.scs`
   - Test: `ocean/test_lif_neuron.ocn`
   - Result: `results/lif_neuron_test.txt` (PASS)
   - Observed behavior: repeated spikes under pulsed input drive

### 3.3 Analog composition milestone

3. **Neuron tile composition**
   - Netlist: `netlists/neuron_tile.scs`
   - Test: `ocean/test_neuron_tile.ocn`
   - Result: `results/neuron_tile_test.txt` (PASS)
   - Observed behavior: synapse decay + membrane integration + spike emission

4. **4-neuron tile composition**
   - Netlist: `netlists/neuro_tile4.scs`
   - Test: `ocean/test_neuro_tile4.ocn`
   - Result: `results/neuro_tile4_test.txt` (PASS)
   - Observed behavior: four parallel spiking channels with staggered first-spike timing

5. **4-neuron coupled propagation tile**
   - Netlist: `netlists/neuro_tile4_coupled.scs`
   - Test: `ocean/test_neuro_tile4_coupled.ocn`
   - Result: `results/neuro_tile4_coupled_test.txt` (PASS)
   - Observed behavior: feed-forward coupling enables downstream activity from a single driven source channel

### 3.4 Reproducibility

- Environment setup: `source setup_cadence.sh`
- Simulation + verification: `./build.sh synapse`, `./build.sh lif_neuron`,
  `./build.sh all`
- Verification status is tracked in `my-workspace/docs/STATUS.md`.
- Robustness sweep entrypoint: `scripts/sweep_neuro_tile4_coupled.sh` (9-point initial sweep, all PASS).

## 4) Taiwan Collaboration Plan (40% Local Connections)

NeuroCore is structured to engage Taiwan's IC ecosystem from simulation to
silicon prototyping.

### Requested Taiwan resources

- **Foundry access:** TSMC mature-node analog/mixed-signal shuttle path
  (primary request: 180nm mixed-signal/BCD-friendly option).
- **Design support:** GUC/CMSC consultation for mixed-signal integration and
  tape-out readiness.
- **IP support:** M31/eMemory interface and configuration IP as needed.
- **Testing ecosystem:** Taiwan-based measurement and validation services for
  prototype characterization.

### Taiwan execution intent

- Participate in required Taiwan matchmaking residency (minimum 1 month).
- Align roadmap with Taiwan partners for pilot silicon and commercialization.

## 5) Value Creation (40%)

NeuroCore targets always-on edge AI use cases where sparse event processing is a
natural fit:

- low-power sensor fusion
- always-listening / trigger-based audio
- compact intelligent sensing endpoints

Commercial pathway: licenseable analog AI compute IP + reference tile designs for
integration with digital SoCs and edge modules.

## 6) Technological Innovation (20%)

Innovation comes from combining:

1. transistor-level analog primitive design,
2. reproducible automated verification,
3. integration path from analog neuromorphic primitives into a broader compute stack.

This bridges practical circuit implementation and scalable productization rather
than limiting novelty to isolated demos.

## 7) Roadmap

### Phase A: February-March 2026 (competition submission phase)

- finalize concept paper + 3-minute video
- continue analog primitive validation and documentation
- define tile-level architecture and testbench

### Phase B: Q2-Q3 2026

- implement and verify first neuromorphic tile netlist
- characterize behavior across operating corners
- establish Taiwan partner workflow for tape-out feasibility

### Phase C: Q4 2026-Q1 2027

- mixed-signal integration planning
- shuttle submission readiness package
- prototype path definition with Taiwan ecosystem partners

## 8) Team

Founder-led technical execution with demonstrated transistor-up implementation and
verification capability in Cadence Spectre/OCEAN flows. Current focus is to expand
from verified primitives to tile-level neuromorphic compute and complete the ICTGC
submission package.

---

## Appendix: Submission Asset Mapping

- Concept paper draft: `competition/concept-paper-v1.md`
- Strategy and judging fit: `competition/competition-plan.md`
- Program rules reference: `competition/ICTGC-Program-Guidelines.md`
- Evidence rollup: `competition/verification-evidence.md`,
  `competition/metrics-summary.md`
- Verification evidence: `results/synapse_test.txt`, `results/lif_neuron_test.txt`,
  `results/neuron_tile_test.txt`, `results/neuro_tile4_test.txt`,
  `results/neuro_tile4_coupled_test.txt`,
  `results/gpu_core_test.txt`
