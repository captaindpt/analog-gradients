# 0007: NeuroCore Competition Kickoff

**Status:** Completed
**Priority:** High
**Created:** 2026-02-02

## Description

Kick off ICTGC execution by validating the first analog primitive and wiring it
into the reproducible build flow.

## Tasks

- [x] Review vision and competition strategy docs
- [x] Integrate `lif_neuron` into `build.sh`
- [x] Fix `ocean/test_lif_neuron.ocn` verification issues
- [x] Run `./build.sh lif_neuron` and capture PASS artifact
- [x] Define next analog block (`synapse`) and implement verification
- [x] Run `./build.sh synapse` and capture PASS artifact
- [x] Draft competition concept paper v1 in `competition/concept-paper-v1.md`
- [x] Define first composition block (`neuron_tile`) and test plan
- [x] Run `./build.sh neuron_tile` and capture PASS artifact

## Acceptance Criteria

1. `./build.sh lif_neuron` passes
2. `results/lif_neuron_test.txt` includes PASS verdict
3. `./build.sh synapse` passes
4. `results/synapse_test.txt` includes PASS verdict
5. `./build.sh neuron_tile` passes
6. `results/neuron_tile_test.txt` includes PASS verdict
7. `my-workspace/docs/STATUS.md` reflects analog primitive/composition status
