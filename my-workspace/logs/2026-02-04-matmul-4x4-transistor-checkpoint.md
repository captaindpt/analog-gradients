# 2026-02-04 - Binary Matmul 4x4 Transistor Checkpoint

## Objective

Advance ticket 0016 with a measured `N=4` transistor checkpoint for both
architectures (digital baseline and neuro path), beyond the 2x2 proof.

## Work Completed

- Added generated 4x4 checkpoint assets:
  - `netlists/matmul4x4_binary_digital.scs`
  - `netlists/matmul4x4_binary_neuro.scs`
  - `ocean/test_matmul4x4_binary_digital.ocn`
  - `ocean/test_matmul4x4_binary_neuro.ocn`
  - `scripts/generate_matmul4x4_checkpoint_assets.py`
- Added reproducible comparison runner:
  - `scripts/run_matmul4x4_binary_comparison.sh`
- Added build target wiring:
  - `build.sh` now accepts `matmul4x4_binary_digital` and
    `matmul4x4_binary_neuro` (and includes them in `all`).

## Measured Checkpoint Results

From `scripts/run_matmul4x4_binary_comparison.sh`:

- Digital (`results/matmul4x4_binary_digital_test.txt`)
  - latency: `0.190 ns`
  - energy (0-120ns): `5.459367e-13 J` (`0.546 pJ`)
  - energy/op (`112 ops`): `4.874435e-15 J/op` (`0.00487 pJ/op`)
- Neuro (`results/matmul4x4_binary_neuro_test.txt`)
  - latency: `2.239 ns`
  - energy (0-120ns): `7.666180e-11 J` (`76.662 pJ`)
  - energy/op (`112 ops`): `6.844804e-13 J/op` (`0.684 pJ/op`)
  - total partial spikes: `28`

Both decoders match expected:
`[[2 2 2 3] [1 1 2 1] [1 3 2 2] [1 2 1 2]]`.

## Artifacts

- `competition/analysis/matmul4x4_binary_comparison.md`
- `competition/analysis/matmul4x4_binary_comparison.csv`
