# 0014: Computation Demo (Coincidence -> XOR)

**Status:** Completed
**Priority:** High
**Created:** 2026-02-03

## Description

Move from "neurons spike" to "network computes" with explicit spike-domain
input/output behavior that maps to recognizable logic tasks.

## Tasks

- [x] Implement first computation block: coincidence detector (temporal AND)
- [x] Add deterministic OCEAN PASS/FAIL verification for A-only/B-only/coincident/offset cases
- [x] Integrate block into `build.sh` and full regression path
- [x] Implement second computation block: XOR using spike-domain encoding
- [x] Add competition evidence language that compares coincidence vs XOR behavior

## Latest Progress (2026-02-03)

- Added netlist: `netlists/coincidence_detector.scs`
- Added verifier: `ocean/test_coincidence_detector.ocn`
- Added build target: `./build.sh coincidence_detector`
- Added full-regression integration in `build.sh all`
- Verification result (`results/coincidence_detector_test.txt`):
  - A-only: `0` spikes
  - B-only: `0` spikes
  - A+B coincident: `1` spike
  - A+B offset: `0` spikes
  - first coincident spike: `12.229 ns`
- Added netlist: `netlists/xor_spike2.scs`
- Added verifier: `ocean/test_xor_spike2.ocn`
- Added build target: `./build.sh xor_spike2`
- Verification result (`results/xor_spike2_test.txt`):
  - 00: `0` spikes
  - 10: `1` spike
  - 01: `1` spike
  - 11: `0` spikes
  - first output spikes (10/01): `~12.1 ns`
- Full regression: `./build.sh all` PASS
  - `results/_runlogs/build_all_20260203_111853.manifest.txt`

## Acceptance Criteria

1. At least one non-trivial spike-domain computation block is reproducibly PASS.
2. Behavior is encoded as explicit input/output cases, not only qualitative waveform inspection.
3. Full-stack `./build.sh all` remains PASS after compute-block addition.
