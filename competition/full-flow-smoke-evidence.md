# Full-Flow Smoke Evidence (DC -> Innovus -> Calibre)

**Date:** 2026-02-04  
**Target:** `alu4_flow_demo`  
**Replay command:** `scripts/run_fullflow_smoke.sh`

## Run Outcome Summary

| Stage | Script | Result | Notes |
|------|--------|--------|-------|
| Synthesis | `scripts/run_dc_smoke.sh` | PASS | DC uses LC-compiled DB library (`implementation/fullflow_demo/work/dc/libcache/alu4_min_cells.db`); no `DB-1`/`UIO-3` fallback |
| Place/Route | `scripts/run_innovus_smoke.sh` | PASS | Innovus completes and emits DEF, routed netlist, reports, and GDS |
| Physical Verification | `scripts/run_calibre_smoke.sh` | PASS | Calibre DRC smoke runs to completion with `0` DRC results in summary |

## Key Artifacts

### DC

- `implementation/fullflow_demo/work/dc/dc_shell.log`
- `implementation/fullflow_demo/work/dc/out/alu4_flow_demo_mapped.v`
- `implementation/fullflow_demo/work/dc/libcache/alu4_min_cells.db`

### Innovus

- `implementation/fullflow_demo/work/innovus/innovus.log`
- `implementation/fullflow_demo/work/innovus/mmmc.tcl`
- `implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.def`
- `implementation/fullflow_demo/work/innovus/out/alu4_flow_demo_postroute.v`
- `implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.gds`
- `implementation/fullflow_demo/work/innovus/reports/alu4_flow_demo_area.rpt`
- `implementation/fullflow_demo/work/innovus/reports/alu4_flow_demo_power.rpt`
- `implementation/fullflow_demo/work/innovus/reports/alu4_flow_demo_timing.rpt`

### Calibre

- `implementation/fullflow_demo/work/calibre/calibre_drc.log`
- `implementation/fullflow_demo/work/calibre/alu4_flow_demo_drc_smoke.svrf`
- `implementation/fullflow_demo/work/calibre/alu4_flow_demo_drc.summary`

### Stage Logs

- `implementation/fullflow_demo/work/logs/stage1_dc.log`
- `implementation/fullflow_demo/work/logs/stage2_innovus.log`
- `implementation/fullflow_demo/work/logs/stage3_calibre.log`

## Quantitative Snapshot

- Innovus area report: `10` instances, total area `20.520`
- Innovus power report total: `0.00069651 mW`
- Innovus outputs present:
  - DEF: `implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.def`
  - GDS: `implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.gds`

## Notes for Demo Narrative

- The implementation chain is reproducible and script-driven in one command.
- Calibre stage now runs with configured license defaults and produces a DRC summary.
- DC target-library compatibility issue (`DB-1`) is resolved in strict replay mode.
- Innovus stage continues to prove physical-design execution and GDS emission path.
- Use `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh` when a hard fail is
  preferred for degraded stages.
- Strict-mode behavior verified on 2026-02-04 (`exit 0` with all stages PASS).
