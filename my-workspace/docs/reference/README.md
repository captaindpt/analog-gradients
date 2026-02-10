# Reference Docs

This folder contains supporting reference notes.

## How to Use

- Treat these as **context**, not primary execution truth.
- Primary truth order is still:
  1. `my-workspace/docs/vision.md`
  2. `my-workspace/docs/DEVELOPMENT.md`
  3. `my-workspace/docs/STATUS.md`

## Cadence Subfolder

- `Cadence/SETUP_GUIDE.md`: environment setup background.
- `Cadence/LICENSE_SETUP.md`: license troubleshooting.
- `Cadence/VIRTUOSO_AUTOMATION.md`: automation patterns and helper usage.
- `Cadence/CHECKPOINT_CLI_PROGRESS.md`: historical checkpoint notes (archival).
- `Cadence/CHINA_INFRASTRUCTURE_INSIGHTS.md`: motivation/thesis context (archival).
- `BINARY_MATMUL_PROOF_PLAN.md`: binary 2x2 matmul proof architecture
  and comparison method (digital vs neuro).
- `NONLINEARITY_COMPARISON_PLAN.md`: analog vs digital nonlinearity benchmark
  protocol (softmax/exp/sum/div).

## Memristor Track References

- `MEMRISTOR_PAPER_STOCK.md`: durable index of local memristor papers under
  `papers/`, grouped by theory/physics/modeling/training relevance.
- `MEMRISTOR_PRIMITIVE_SPEC.md`: master notes/spec for the memristor primitive
  workstream (equations, acceptance criteria, phase gates, execution sequence).

## Manufacturing-Readiness Goals

Reference goals for "manufacturable pre-silicon package ready":

1. Fix DC library flow correctness (resolve `.lib` vs `.db` target library usage).
2. Lock Synopsys/Calibre license environment in scripted runs.
3. Move from smoke checks to real signoff gates (full STA + DRC + LVS; add PEX where applicable).
4. Define and pass corners/mismatch/yield criteria, then freeze a tapeout-candidate revision.

If a reference note conflicts with the core docs, follow the core docs.
