# Binary 2x2 Matmul: Digital vs Neuro Comparison

Generated: 2026-02-04 03:54:25 UTC

Scope: binary-only first proof (`A,B ∈ {0,1}`), fixed stimulus point:
- A = `[[1,0],[1,1]]`
- B = `[[1,1],[0,1]]`
- Expected Y = `[[1,1],[1,2]]`

| Metric | Digital Baseline | Neuro Path |
|--------|------------------|------------|
| Operations | 12 | 12 |
| Decoded output | `[[1 1] [1 2]]` | `[[1 1] [1 2]]` |
| Latency to full output-valid | 0.141 ns | 2.233 ns |
| Measured energy (0-90ns) | 0.060 pJ | 11.202 pJ |
| Energy / op (12 ops) | 0.005 pJ/op | 0.934 pJ/op |
| Neuro partial spikes | n/a | 5 |
| Neuro spike-model estimate | n/a | 16.350 pJ |

Derived deltas:
- Neuro measured energy vs digital: `+18692.78%` (negative means lower).
- Neuro/digital latency ratio: `15.837x`.
- Caveat: this digital baseline is a minimal combinational transistor netlist, not a clocked PE-array workload.

Reproduce:
- `./build.sh matmul2x2_binary_digital`
- `./build.sh matmul2x2_binary_neuro`
- `scripts/run_matmul2x2_binary_comparison.sh`

Sources:
- `/home/v71349/analog-gradients/results/matmul2x2_binary_digital_test.txt`
- `/home/v71349/analog-gradients/results/matmul2x2_binary_neuro_test.txt`
- `/home/v71349/analog-gradients/competition/analysis/matmul2x2_binary_comparison.csv`
