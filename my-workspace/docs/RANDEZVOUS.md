# Workspace Rendezvous

**Date:** 2026-02-03  
**Purpose:** Keep execution clean, aligned, and ready to scale to bigger NeuroCore blocks.

## What "Clean Workspace" Means

1. Work only from source-of-truth docs (`vision.md`, `DEVELOPMENT.md`, `STATUS.md`).
2. Keep generated noise out of commits (raw waveforms, probe logs, scratch DB/work dirs).
3. Record every meaningful run in a dated log under `my-workspace/logs/`.
4. Keep tickets current: one ticket per meaningful objective shift.

## Current Rendezvous Objectives

1. **Full-flow reliability**  
   - Move DC + Calibre from "license-blocked narrative" to "configured + reproducible". ✅  
   - Close remaining DC blocker (`DB-1` library format path). ✅
2. **Analog robustness expansion**  
   - Extend sweeps beyond `neuro_tile4_coupled` to `synapse`, `lif_neuron`, `neuron_tile`. ✅
   - Define explicit PASS bands (not only nominal PASS). ✅
3. **Scale path ("bigger and bigger things")**  
   - Preserve fail-closed verification guarantees while increasing network size/complexity.
   - Keep every new block script-reproducible and mapped to evidence artifacts.

## Operational Loop (Per Session)

```bash
source setup_cadence.sh
./build.sh all
```

For full-flow stages requiring Synopsys/Siemens licenses:

```bash
export SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca
export MGLS_LICENSE_FILE=6056@licaccess.cmc.ca
export SALT_LICENSE_SERVER=$MGLS_LICENSE_FILE
scripts/run_fullflow_smoke.sh
```

## Active Tickets for This Rendezvous

- `my-workspace/tickets/0009-neurocore-robustness-sweeps.md`
- `my-workspace/tickets/0010-transistor-to-gds-demo-bringup.md`
- `my-workspace/tickets/0011-competition-paper-workthrough.md`
- `my-workspace/tickets/0015-workspace-rendezvous-and-scale-ramp.md`
- `my-workspace/tickets/0016-binary-matmul-architecture-comparison.md`
- `my-workspace/tickets/0017-temporal-gradient-learning-loop.md`
