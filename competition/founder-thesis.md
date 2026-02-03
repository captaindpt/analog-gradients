# NeuroCore Founder Thesis

## Core Reframe

This project is not "I can use EDA tools."  
This project is "I am building a compute primitive that clocked digital flows do not natively represent."

## Original Idea

**Clockless continuous-time compute using analog spike dynamics.**

Computation is encoded in:
1. membrane trajectory \(V_{mem}(t)\),
2. spike timing \(t_{spike}\),
3. event propagation latency across coupled channels,
instead of synchronous logic state transitions.

## Why This Is Founder-Level (Not Job-Applicant-Level)

Existing digital-centric flows optimize boolean + clock behavior.
NeuroCore demonstrates:
- asynchronous event-driven propagation in transistor circuits,
- timing-coded computation (latency as signal),
- sensitivity of timing to physical parameters (temporal gradients).

## Evidence Already in Repo

| Claim | Current Evidence |
|------|------------------|
| Analog neurons compute via continuous-time dynamics | `results/synapse_test.txt`, `results/lif_neuron_test.txt` |
| Multi-channel timing encodes information | `results/neuro_tile4_test.txt` (27.5/29.5/31.5/33.5 ns first spikes) |
| Feed-forward event propagation | `results/neuro_tile4_coupled_test.txt` |
| Explicit spike-domain computation (temporal AND) | `results/coincidence_detector_test.txt` |
| Explicit spike-domain computation (XOR) | `results/xor_spike2_test.txt` |
| Parameter robustness | `competition/sweeps/neuro_tile4_coupled_sweep_summary.md` (63/63 PASS) |
| Implementation credibility | `competition/full-flow-smoke-evidence.md` |

## Current Evidence Status (Math-Heavy)

1. **ODE-fit validation** ✅
   - Artifact: `competition/analysis/lif_ode_fit_summary.md`
   - Current readout:
     - decay-window fit (12ns-19ns): \(R^2 = 0.931\)
     - baseline full-window model remains weak: \(R^2 = 0.029\)
     - phase-aware piecewise fit improves global derivative fit:
       \(R^2 = 0.312\)
2. **Temporal sensitivity extraction** ✅
   - Artifact: `competition/analysis/temporal_sensitivity_summary.md`
   - Refined 63-point sweep readout:
     - \(dt_{spike0}/dr_{fb} \approx -0.599 \,\text{ns}/\text{k}\Omega\)
     - \(dt_{spike1}/dr_{fb} \approx -0.751 \,\text{ns}/\text{k}\Omega\)
     - \(dt_{spike2}/dr_{fb} \approx -0.481 \,\text{ns}/\text{k}\Omega\)
     - \(dt_{spike3}/dr_{fb} \approx -0.170 \,\text{ns}/\text{k}\Omega\)
   - The report now includes \(R^2\), 95% CI, and timing-step diagnostics.
3. **Energy-per-event estimate** ✅
   - Artifact: `competition/analysis/lif_energy_summary.md`
   - Current readout:
     - energy/spike (total/spike): \(\approx 3.271\,\text{pJ}\)
     - bootstrap 95% CI: \([3.155, 3.424]\,\text{pJ}\)
   - Uncertainty artifacts:
     - `competition/analysis/lif_energy_trace.csv`
     - `competition/analysis/lif_energy_bootstrap.csv`
4. **Mixed-signal coupling demo** ✅
   - Artifact: `competition/mixed-signal-smoke-evidence.md`
   - Highlight: downstream spikes are suppressed before digital `en` and activate after `en` rises.
5. **Computation demo (coincidence detector)** ✅
   - Artifact: `results/coincidence_detector_test.txt`
   - Readout:
     - A-only: 0 spikes
     - B-only: 0 spikes
     - A+B coincident: 1 spike
     - A+B offset: 0 spikes
6. **Computation demo (XOR)** ✅
   - Artifact: `results/xor_spike2_test.txt`
   - Readout:
     - 00: 0 spikes
     - 10: 1 spike
     - 01: 1 spike
     - 11: 0 spikes

## Next Rigor Targets

1. Expand compute tasks beyond Boolean primitives (pattern discrimination /
   temporal sequence classification).
2. Expand corner-conditioned ODE/energy sweep beyond current 9-point grid
   (`competition/analysis/lif_corners/20260202_224254/`).
3. Add repeated-run reproducibility stats across environments/sessions.
4. Keep confidence/limitation language synchronized in competition evidence docs.

## Literature Context and Positioning

### Energy Benchmarks (Context Only, Non-Normalized)

| Platform | Metric | Value | Notes |
|----------|--------|-------|-------|
| **NeuroCore LIF** | energy/spike | **3.27 pJ** | This work (bootstrap 95% CI: 3.16-3.42 pJ) |
| Intel Loihi | energy/synaptic op | 23.6 pJ | Digital neuromorphic, includes routing |
| IBM TrueNorth | energy/synaptic event | ~26 pJ | Digital neuromorphic |
| SENECA (digital) | energy/synaptic op | ~2.8 pJ | Digital SNN accelerator |
| Analog CMOS LIF (28nm) | energy/spike | 1.61 fJ | Aggressive claim, definition-dependent |
| SOI LIF (2017) | energy/spike | ~35 pJ | Older analog reference |

**Interpretation guardrail:** These values are not directly comparable without
normalizing task, event definition, node/process, routing overhead, and
measurement boundaries. Use this table for qualitative positioning only.

**Caveat:** Energy metrics differ (pJ/spike vs pJ/synaptic-op vs µJ/inference).
We define energy-per-spike as total energy drawn from VDD during one
integrate-fire-reset cycle, including membrane charging, threshold detection,
and reset discharge.

### Novelty Claim

Prior art exists for coincidence detection in hardware:
- Clocked CMOS coincidence detectors (different approach - synchronous)
- Resonate-and-fire analog neurons (different neuron model)
- System-level delay-line modules (higher abstraction)

**NeuroCore's differentiator (current stage):** A clean CMOS LIF-based
temporal-AND compute primitive with:
- Quantified energy (3.27 pJ/spike with uncertainty bounds)
- Measured timing sensitivity (∂t_spike/∂r with R² > 0.98)
- Corner-sweep verification (63/63 coupled-tile, 9-corner LIF)
- Explicit computation demo (coincidence detector PASS)

### Timing Gradients as Training Signals

The measured temporal sensitivities:
- \(dt_{spike}/dr_{fb} \approx -0.17\) to \(-0.75\) ns/kΩ

...are empirical local gradients of the same form computed analytically by **EventProp** (Wunderlich et al., Nature Scientific Reports 2021), which derives exact gradients for continuous-time SNNs by backpropagating at spike times.

**Implication:** The circuit exhibits smooth, measurable timing gradients, a
prerequisite for gradient-based optimization of spike timing. This is
evidence of trainability potential, not yet a full on-chip learning result.

Key citations:
- EventProp: event-based backpropagation for continuous-time SNNs
- SparseProp (NeurIPS 2023): efficient event-based training
- BrainScaleS-2: mixed-signal substrate with in-the-loop training (PNAS 2022)

### Toolchain Leverage

This project uses a full semiconductor EDA stack:
- **Analog simulation:** Cadence Spectre, Synopsys HSPICE
- **Digital simulation:** VCS, Xcelium, Questa
- **Synthesis:** Synopsys Design Compiler
- **Place & route:** Cadence Innovus
- **Physical verification:** Siemens Calibre
- **FPGA:** Xilinx Vivado, Intel Quartus

Traditional chip design typically requires separate specialized teams for each
domain. This project shows that one person + AI agents can orchestrate a
reproducible **smoke** flow from transistor netlists to GDSII-ready artifacts.

The gap between "I can design a chip" and "I designed a chip" is:
1. Layout (available via Virtuoso GUI)
2. Tape-out (a service you purchase: MOSIS, Efabless, commercial MPW)

Most infrastructure for a full demonstration is in place; remaining work is
closing the loop on layout-level polish and tape-out logistics.

## Competition Pitch Line

> Conventional chips compute in clocked logic states.
> NeuroCore computes in continuous-time physics, where voltage trajectories and spike timing are the program.
