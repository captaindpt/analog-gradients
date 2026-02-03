# 0013: Evidence Rigor Hardening

**Status:** In Progress
**Priority:** High
**Created:** 2026-02-02

## Description

Now that build/test auditability is fail-closed and reproducible, harden the
founder-evidence track so claims are quantitatively robust and not overfit to
coarse measurement windows.

## Tasks

- [ ] Expand coupled-tile sweep granularity (`r_fb`, `rleak`) and preserve full raw traces per sweep point
- [ ] Increase transient/time-resolution where needed to reduce 0.5ns quantization effects
- [ ] Rework ODE fitting into phase-aware model(s) and report both local and global fit quality
- [ ] Add uncertainty reporting (multi-run or bootstrap) for energy-per-spike estimates
- [ ] Update competition evidence docs with explicit confidence/limitation statements

## Acceptance Criteria

1. Temporal sensitivity trends vary meaningfully with parameters (or explicitly
   show and justify invariance with higher-fidelity data).
2. ODE-fit section reports a defensible global model or clearly bounded local
   models with rationale.
3. Energy metric includes uncertainty and method assumptions.
4. All claims in `competition/founder-thesis.md` map to reproducible artifacts
   and confidence statements.
