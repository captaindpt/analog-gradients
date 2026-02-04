# Binary 2x2 Matmul Proof Plan (Reference)

## Purpose

Define a fair, reproducible head-to-head compute demo:

- same task,
- two architectures,
- shared measurement method.

Task is constrained to **binary 2x2 matrix multiply** for first proof.

## Task Definition

Given:

```
[a b]   [e f]   [ae+bg  af+bh]
[c d] x [g h] = [ce+dg  cf+dh]
```

For binary inputs (`0/1`), each multiply is an AND and each output is an
integer in `{0,1,2}`.

## Architecture Comparison

### A) Digital Baseline

- Existing clocked digital path (GPU-core-linked baseline).
- Compute same binary 2x2 matmul workload.
- Report:
  - cycles,
  - latency (`cycles * clock_period`),
  - transient energy (`integral(VDD * I(VDD) dt)`).

### B) Neuro Path

- Product terms via spike coincidence behavior.
- Two-term accumulation via membrane integration.
- Output decode represents `{0,1,2}` for each matrix entry.
- Report:
  - partial-product spike counts,
  - output value decode,
  - latency (first valid output event),
  - transient energy (`integral(VDD * I(VDD) dt)`),
  - spike-model estimate (`3.27 pJ/spike * spikes`) as secondary sanity check.

## Honesty Constraints

1. Call this explicitly **binary matmul proof** (not full-precision matmul).
2. Use same input workload across both architectures.
3. Publish both favorable and unfavorable metrics.
4. Keep artifact paths reproducible in repo scripts/results.
5. Separate measured energy from model-estimated energy.

## Implementation Phases

1. **Phase 1 (now):** neuro binary matmul wiring using existing coincidence +
   integration primitives.
2. **Phase 2:** digital binary matmul baseline harness + energy extraction.
3. **Phase 3:** one-page comparison report and demo script.
4. **Phase 4 (stretch):** move from binary to rate/time-coded multiply primitive.

## Expected Artifacts

- `netlists/matmul2x2_binary_neuro.scs`
- `ocean/test_matmul2x2_binary_neuro.ocn`
- `netlists/matmul2x2_binary_digital.scs` (or equivalent GPU harness)
- `ocean/test_matmul2x2_binary_digital.ocn`
- `competition/analysis/matmul2x2_binary_comparison.md`
