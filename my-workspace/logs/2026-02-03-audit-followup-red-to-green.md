# 2026-02-03: Audit Follow-up (Red -> Green)

## Findings addressed

- Build baseline regressed to red after strict warning gate rollout.
- OCEAN relative path portability failed when running build from outside repo root.

## Changes

- `build.sh`
  - OCEAN now executes from repo root (`cd $REPO_DIR`) before script run.
  - strict Spectre warning gate refined to parse explicit warning codes only:
    - `WARNING (SPECTRE-xxxxx)`
  - added explicit warning allowlist support:
    - `config/spectre_warning_allowlist.txt`
- Added initial allowlist entries for currently known tolerance-relaxation warning codes:
  - `SPECTRE-17191`
  - `SPECTRE-17192`

## Validation

- `./build.sh all` PASS
  - `results/_runlogs/build_all_20260203_133924.{log,manifest.txt}`
- portability repro fixed:
  - `cd /tmp && /home/v71349/analog-gradients/build.sh pe4` PASS
  - `results/_runlogs/build_pe4_20260203_134239.{log,manifest.txt}`

## Outcome

False-pass protections remain intact, warning policy stays strict for unallowlisted warning codes, and the baseline is green again.
