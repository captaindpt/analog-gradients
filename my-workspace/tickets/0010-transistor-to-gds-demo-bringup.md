# 0010: Transistor-to-GDS Demo Bring-Up

**Status:** In Progress (strict replay unblocked)
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

## Latest Run Snapshot (2026-02-03)

- Replay command: `scripts/run_fullflow_smoke.sh`
- License defaults are now auto-seeded in flow scripts via:
  `scripts/setup_fullflow_licenses.sh`
- DC stage: license checkout succeeds; stage degrades due target-library format
  (`DB-1` / `UIO-3`) and falls back to mapped netlist
  (`implementation/fullflow_demo/work/dc/reports/alu4_flow_demo_dc_target_lib.warn`)
- Innovus stage: PASS; DEF/post-route netlist/GDS generated
- Calibre stage: PASS with licensed DRC run (`calibrehdrc` + `calibredrc`)
- Strict replay (`FULLFLOW_STRICT=1`) now fails closed on any degraded stage,
  including DC target-library fallback.

## Latest Run Snapshot (2026-02-04)

- Replay command: `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh`
- DC stage: PASS with DB-compatible compiled library
  (`implementation/fullflow_demo/work/dc/libcache/alu4_min_cells.db`);
  no `DB-1`/`UIO-3` fallback
- Innovus stage: PASS; DEF/post-route netlist/GDS generated
- Calibre stage: PASS; DRC smoke summary reports `TOTAL RESULTS GENERATED = 0`
- Strict replay now exits cleanly (`exit 0`)
