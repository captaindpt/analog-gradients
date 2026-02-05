# 2026-02-05 - Nonlinearity Benchmark Kickoff

## Objective

Kick off the analog vs digital nonlinearity comparison (softmax) and prepare
the repo as a proper testbed for energy/latency/accuracy comparisons.

## Work Completed

- Added benchmark protocol reference:
  - `my-workspace/docs/reference/NONLINEARITY_COMPARISON_PLAN.md`
- Opened new benchmark ticket:
  - `my-workspace/tickets/0019-analog-vs-digital-nonlinearity-comparison.md`
- Added benchmark scaffolding scripts:
  - `scripts/generate_softmax_vectors.py`
  - `scripts/run_nonlinearity_vector_benchmark.py`
- Added toy softmax netlists + runner:
  - `netlists/softmax4_analog_toy.scs`
  - `netlists/softmax4_digital_toy.scs`
  - `scripts/run_softmax4_nonlinearity_benchmark.sh`
- Added GPDK180-compatible softmax netlists:
  - `netlists/softmax4_analog_gpdk180.scs`
  - `netlists/softmax4_digital_gpdk180.scs`
- Benchmark harness now supports output scaling/inversion for PDK runs.
- Generated initial softmax vector set (N=4, 64 samples):
  - `competition/data/nonlinearity/softmax_vectors_n4.csv`
  - `competition/data/nonlinearity/softmax_vectors_n4.json`
- Updated core docs to reflect the new objective:
  - `my-workspace/docs/vision.md`
  - `my-workspace/docs/DEVELOPMENT.md`
  - `my-workspace/docs/STATUS.md`
  - `my-workspace/docs/RANDEZVOUS.md`

## Next Steps

1. Implement analog softmax blocks with PDK fidelity.
2. Implement matched digital baseline (LUT/polynomial) and verifiers.
3. Run benchmark and publish summary under `competition/analysis/`.
