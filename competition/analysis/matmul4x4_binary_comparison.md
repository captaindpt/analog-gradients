# Binary 4x4 Matmul: Digital vs Neuro Checkpoint

Generated: 2026-02-04 17:45:36 UTC

Scope: binary-only transistor checkpoint (`A,B ∈ {0,1}`), fixed stimulus point.
- A = `[[1,0,1,1],[0,1,1,0],[1,1,0,1],[1,0,0,1]]`
- B = `[[1,1,0,1],[0,1,1,0],[1,0,1,1],[0,1,1,1]]`
- Expected Y = `[[2,2,2,3],[1,1,2,1],[1,3,2,2],[1,2,1,2]]`

| Metric | Digital Baseline | Neuro Path |
|--------|------------------|------------|
| Operations | 112 | 112 |
| Decoded output match | `True` | `True` |
| Latency to full output-valid | 0.190 ns | 2.239 ns |
| Measured energy (0-120ns) | 0.546 pJ | 76.662 pJ |
| Energy / op (112 ops) | 0.005 pJ/op | 0.684 pJ/op |
| Neuro partial spikes | n/a | 28 |
| Neuro spike-model estimate | n/a | 91.560 pJ |

Derived deltas:
- Neuro measured energy vs digital: `+13942.25%`.
- Neuro/digital latency ratio: `11.784x`.

Reproduce:
- `./build.sh matmul4x4_binary_digital`
- `./build.sh matmul4x4_binary_neuro`
- `scripts/run_matmul4x4_binary_comparison.sh`

Sources:
- `/home/v71349/analog-gradients/results/matmul4x4_binary_digital_test.txt`
- `/home/v71349/analog-gradients/results/matmul4x4_binary_neuro_test.txt`
- `/home/v71349/analog-gradients/competition/analysis/matmul4x4_binary_comparison.csv`
