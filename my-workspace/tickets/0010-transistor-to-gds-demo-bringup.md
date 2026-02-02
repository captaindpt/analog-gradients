# 0010: Transistor-to-GDS Demo Bring-Up

**Status:** In Progress (tool-license constrained)
**Priority:** High
**Created:** 2026-02-02

## Description

Bring up a reproducible implementation flow demo for competition:
DC synthesis -> Innovus P&R -> Calibre verification, with analog NeuroCore
evidence as bookends.

## Tasks

- [x] Select first digital implementation target (`alu4_flow_demo`)
- [x] Create DC script and run synthesis smoke test
- [x] Create Innovus script and run place/route smoke test
- [x] Create Calibre invocation and capture DRC/LVS smoke output
- [x] Add one-command orchestrator for replay
- [x] Attach generated artifact references under `competition/`
- [x] Draft shot-by-shot video runbook with exact commands and cues
- [x] Create `competition/recording-pack/` scene-organized capture bundle
- [x] Add guided recording helper (`scripts/demo_narrator.sh`)
- [x] Add timed voiceover script (`competition/voiceover-script.md`)

## Acceptance Criteria

1. A terminal command sequence can replay the full flow end-to-end
2. Netlist/timing/P&R/DRC artifacts are saved and referenced in docs
3. Demo path is aligned with `competition/full-flow-demo-plan.md`

## Latest Run Snapshot (2026-02-02)

- Replay command: `scripts/run_fullflow_smoke.sh`
- DC stage: executable runs, synthesis blocked by `DCSH-1` license;
  fallback mapped netlist used (`implementation/fullflow_demo/work/dc/reports/alu4_flow_demo_dc_fallback.warn`)
- Innovus stage: PASS; DEF/post-route netlist/GDS generated
- Calibre stage: executable runs, DRC blocked by license;
  blocked summary emitted (`implementation/fullflow_demo/work/calibre/alu4_flow_demo_drc.summary`)
- Competition evidence doc added: `competition/full-flow-smoke-evidence.md`
- Recording runbook added: `competition/video-shot-script.md`
- Recording pack added: `competition/recording-pack/`
- Guided narrator script added: `scripts/demo_narrator.sh`
- Voiceover script added: `competition/voiceover-script.md`
