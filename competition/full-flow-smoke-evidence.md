# Full-Flow Smoke Evidence (DC -> Innovus -> Calibre)

**Date:** 2026-02-02  
**Target:** `alu4_flow_demo`  
**Replay command:** `scripts/run_fullflow_smoke.sh`

## Run Outcome Summary

| Stage | Script | Result | Notes |
|------|--------|--------|-------|
| Synthesis | `scripts/run_dc_smoke.sh` | BLOCKED (license) | `dc_shell` runs, then reports `DCSH-1`; fallback mapped netlist is injected |
| Place/Route | `scripts/run_innovus_smoke.sh` | PASS | Innovus completes and emits DEF, routed netlist, reports, and GDS |
| Physical Verification | `scripts/run_calibre_smoke.sh` | BLOCKED (license) | Calibre runs and parses rule file; DRC license checkout fails |

## Key Artifacts

### DC

- `implementation/fullflow_demo/work/dc/dc_shell.log`
- `implementation/fullflow_demo/work/dc/out/alu4_flow_demo_mapped.v`
- `implementation/fullflow_demo/work/dc/reports/alu4_flow_demo_dc_fallback.warn`

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
- `implementation/fullflow_demo/work/calibre/alu4_flow_demo_calibre_license.warn`

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
- Current environment licenses block full DC synthesis and Calibre DRC signoff.
- Innovus stage proves physical-design execution and GDS emission path.
- Use `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh` when a hard fail is
  preferred for blocked stages.
- Strict-mode behavior verified on 2026-02-02 (`exit 20` with current licenses).
