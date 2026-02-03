# Architecture Dissection Log
**Date:** 2026-02-02  
**Purpose:** complete bottom-up architecture breakdown for paper writing

---

## Scope and method

Read source-of-truth implementation artifacts in this order:

1. analog netlists:
   - `netlists/synapse.scs`
   - `netlists/lif_neuron.scs`
   - `netlists/neuron_tile.scs`
   - `netlists/neuro_tile4.scs`
   - `netlists/neuro_tile4_coupled.scs`
   - `netlists/neuro_tile4_mixed_signal.scs`
2. verification scripts:
   - `ocean/test_*.ocn` for each analog block above
3. latest result artifacts:
   - `results/*_test.txt`
4. thesis framing:
   - `competition/founder-thesis.md`
   - `competition/analysis/*.md`

Each layer is documented with: behavior, structural mechanism, parameter role, and paper hooks.

---

## Layer 1: synapse primitive

**Netlist:** `netlists/synapse.scs`  
**Verification:** `ocean/test_synapse.ocn`, `results/synapse_test.txt`

### What it does

Transforms presynaptic pulse train `pre` into an analog postsynaptic waveform `post` with charge integration and exponential decay, then buffers to digital-like `out`.

### How it does it (circuit)

- `MN_DRV (post pre vdd 0)` acts as controlled charge-transfer path from `vdd` into `post`.
- `C_POST` stores charge at `post`.
- `R_DECAY` leaks charge to ground, setting decay slope.
- Two CMOS inverters (`MP1/MN1`, `MP2/MN2`) buffer `post` into rail-to-rail output.

### Key parameters and roles

- `cpost=200fF`: integration bucket.
- `rdecay=80k`: decay path.
- implied synaptic time constant:
  - `tau_syn = rdecay * cpost = 80k * 200fF = 16ns`.

### Evidence snapshot

- output pulse count: 6
- measured `Vpost(max) = 1.418V`
- clear integrate -> decay -> re-charge behavior over repeated pulses

### Compact model

`dVpost/dt = Iinj/Cpost - Vpost/(Rdecay*Cpost)`

---

## Layer 2: single LIF neuron

**Netlist:** `netlists/lif_neuron.scs`  
**Verification:** `ocean/test_lif_neuron.ocn`, `results/lif_neuron_test.txt`

### What it does

Implements a leaky integrate-and-fire loop:

1. input current charges membrane node `mem`,
2. threshold detector generates `spike`,
3. feedback reset transistor discharges membrane.

### How it does it (circuit)

- input drive: pulse current source `I_in (vdd mem)`.
- membrane dynamics: `Cmem` + `Rleak`.
- threshold path: two inverters (`MP1/MN1`, `MP2/MN2`) using `mem` as analog input.
- reset loop: `MN_reset (mem spike 0 0)` discharges `mem` when `spike` is high.
- output buffer: `MP3/MN3`.

### Key parameters and roles

- `cmem=1pF`, `rleak=10M`, `iin_amp=500uA`.
- nominal leak time constant:
  - `tau_mem = rleak * cmem = 10us`.
- effective observed dynamics are faster due to active threshold/reset events.

### Evidence snapshot

- total spikes: 10 in 200ns window
- first spikes around 7ns, then periodic firing
- `Vmem(max)=1.651V`
- PASS with expected charge/spike behavior

### Compact hybrid model

- subthreshold: `Cmem * dVmem/dt = Iin - Vmem/Rleak`
- event condition: if `Vmem >= Vth`, emit spike
- reset phase: additional discharge current through `MN_reset`

---

## Layer 3: neuron tile (synapse + membrane + spike)

**Netlist:** `netlists/neuron_tile.scs`  
**Verification:** `ocean/test_neuron_tile.ocn`, `results/neuron_tile_test.txt`

### What it does

Composes synaptic filtering and LIF spiking into one end-to-end channel.

### How it does it

- front-end synapse (`MN_SYN`, `C_SYN`, `R_SYN`) creates filtered node `syn_post`.
- `R_COUPLE` injects synaptic voltage into membrane `mem`.
- membrane + threshold + reset as in LIF block.

### Why this layer matters

This is the first complete analog compute path:
`pre spike -> analog state variable -> thresholded event output`.

### Evidence snapshot

- `Vsyn@8ns > Vsyn@16ns` confirms decay
- `Vmem(max)=0.818V`
- spike count: 11
- PASS confirms composed behavior, not just isolated primitives

---

## Layer 4: neuro_tile4 (parallel channels)

**Netlist:** `netlists/neuro_tile4.scs`  
**Verification:** `ocean/test_neuro_tile4.ocn`, `results/neuro_tile4_test.txt`

### What it does

Instantiates four neuron-tile channels in parallel with staggered input delays.

### Structural pattern

- channels 0..3 are replicated blocks.
- only presynaptic delays differ (`5ns`, `7ns`, `9ns`, `11ns`).
- architecture intentionally converts input phase offsets into output spike-time offsets.

### Evidence snapshot

- all membranes integrate (`~0.818V` max each).
- all channels spike (`13` pulses each in report).
- first-spike ordering preserved: channel 0 < 1 < 2 < 3.

### Compute interpretation

Information is encoded in relative timing (phase/latency), not only logic level.

---

## Layer 5: neuro_tile4_coupled (feed-forward propagation)

**Netlist:** `netlists/neuro_tile4_coupled.scs`  
**Verification:** `ocean/test_neuro_tile4_coupled.ocn`, `results/neuro_tile4_coupled_test.txt`

### What it does

Demonstrates event propagation when only channel 0 gets external stimulation.
Downstream channels activate through coupling paths.

### How it does it

- external drive only on `pre0`; `pre1..pre3` are DC 0.
- coupling network:
  - resistive injection: `R_FB01`, `R_FB12`, `R_FB23`
  - active feed-forward transistors: `MN_FB01`, `MN_FB12`, `MN_FB23`
- inverter front-end sizing differs from uncoupled tile (`pch 800n`, `nch 3u`) to tune switching behavior.

### Evidence snapshot

- all channels show membrane integration (`0.642, 0.993, 1.216, 0.756V` maxima).
- spike counts in current artifact: `15` per channel.
- first-spike ordering preserved (`10.0, 12.5, 13.5, 14.0ns`).

### Paper significance

Shows asynchronous, clockless propagation across channels using transistor dynamics.

---

## Layer 6: neuro_tile4_mixed_signal (digital gate over analog propagation)

**Netlist:** `netlists/neuro_tile4_mixed_signal.scs`  
**Verification:** `ocean/test_neuro_tile4_mixed_signal.ocn`, `results/neuro_tile4_mixed_signal_test.txt`

### What it does

Adds digital enable `en` that gates analog feed-forward coupling.

### How it does it

- digital enable chain:
  - `V_EN_IN` pulse source
  - two-inverter buffer to clean `en`
- coupling transistors become gated switch elements:
  - `MN_FB01 (syn1 en spike0 0)` and similarly for downstream links.

### Evidence snapshot

- enable edge at `~140.5ns`.
- before enable: `spike0=6`, `spike1..3=0`.
- after enable: `spike0=7`, `spike1=7`, `spike2=7`, `spike3=7`.

### Thesis relevance

Digital control modulates analog temporal propagation in one run, bridging conventional control logic with continuous-time compute substrate.

---

## Parallel digital baseline track

Verified hierarchy remains intact from CMOS gates to GPU scaffold:

- Level 5 -> 0 stack remains PASS (`inverter` through `gpu_core`).
- this provides control/reference path while neuromorphic branch advances.

This dual-track structure is central to the paper: the project is not analog-only experimentation; it is analog expansion on top of a verified digital base.

---

## Big assembled architecture (paper framing)

From left to right:

1. **Input events** (presynaptic spikes, optional digital enables),
2. **Synaptic filtering** (`MN_DRV + C + R`),
3. **Membrane dynamics** (`Cmem + Rleak`),
4. **Event generation** (inverter comparator chain + reset transistor),
5. **Spatial propagation** (feed-forward coupling across channels),
6. **Control coupling** (digital enable gating),
7. **Verification envelope** (OCEAN PASS checks + sweep + ODE/sensitivity/energy analyses),
8. **Implementation credibility lane** (RTL target through Innovus/GDS smoke path).

This is the "small pieces -> assembled system" narrative to carry the paper.

---

## Immediate paper actions

- [x] complete component-level architecture dissection
- [ ] inject architecture breakdown section into LaTeX source
- [ ] add explicit equations for synapse/membrane/coupling
- [ ] add a dedicated architecture diagram artifact for reuse in paper/slides
- [ ] reconcile metric values between waveform CSV-derived summaries and latest OCEAN reports (threshold definition note)
