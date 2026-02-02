# Mixed-Signal Smoke Evidence

**Date:** 2026-02-02  
**Target:** `neuro_tile4_mixed_signal`  
**Command:** `./build.sh neuro_tile4_mixed_signal`

## Objective

Demonstrate digital control over analog spike propagation in one transistor-level
Spectre run.

## Setup

- Analog path: 4-neuron feed-forward tile
- Digital control path: inverter-buffered `en` signal
- Control behavior: `en` rises near `140.5ns`, enabling coupling transistors

## Key Result

From `results/neuro_tile4_mixed_signal_test.txt`:

- Enable rising edge: `140.50 ns`
- Spike counts before enable (`20ns .. 135.5ns`):
  - `spike0=6 spike1=0 spike2=0 spike3=0`
- Spike counts after enable (`160.5ns .. 300ns`):
  - `spike0=7 spike1=7 spike2=7 spike3=7`

Interpretation:
- Before digital enable, downstream channels are quiescent.
- After digital enable, downstream analog channels activate and propagate.

## Artifacts

- Netlist: `netlists/neuro_tile4_mixed_signal.scs`
- Verification script: `ocean/test_neuro_tile4_mixed_signal.ocn`
- Report: `results/neuro_tile4_mixed_signal_test.txt`
