# 0019: Analog vs Digital Nonlinearity Comparison (Softmax)

**Status:** In Progress  
**Priority:** High  
**Created:** 2026-02-05

## Description

Build a reproducible benchmark that compares analog vs digital computation of
nonlinear neural ops (exp/sum/div/softmax). Linear ops remain digital in both
paths. The goal is a defensible energy/latency/accuracy comparison on matched
inputs.

Reference plan:
`my-workspace/docs/reference/NONLINEARITY_COMPARISON_PLAN.md`

## Tasks

- [x] Publish benchmark plan + measurement rules
- [x] Add vector generator script for softmax test vectors
- [x] Add benchmark runner harness (per-vector energy/latency/accuracy)
- [x] Add toy analog/digital softmax netlists + runner for harness validation
- [x] Add GPDK180-compatible softmax netlists (analog + digital proxy)
- [ ] Implement analog exp/sum/div/softmax with real PDK models
- [ ] Implement digital baseline (LUT or polynomial) with matched accuracy spec
- [ ] Write OCEAN verifiers for analog + digital softmax blocks
- [ ] Run benchmark and publish summary under `competition/analysis/`

## Acceptance Criteria

1. Both analog and digital paths run on the same input vectors.
2. Energy is measured by VDD current integration with explicit IO scope.
3. Latency and accuracy are defined and pass/fail gated.
4. Summary reports real pJ/ns/error numbers with model fidelity declared.
