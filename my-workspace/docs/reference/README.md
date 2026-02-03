# Reference Docs

This folder contains supporting reference notes.

## How to Use

- Treat these as **context**, not primary execution truth.
- Primary truth order is still:
  1. `my-workspace/docs/vision.md`
  2. `my-workspace/docs/DEVELOPMENT.md`
  3. `my-workspace/docs/STATUS.md`

## Cadence Subfolder

- `Cadence/SETUP_GUIDE.md`: environment setup background.
- `Cadence/LICENSE_SETUP.md`: license troubleshooting.
- `Cadence/VIRTUOSO_AUTOMATION.md`: automation patterns and helper usage.
- `Cadence/CHECKPOINT_CLI_PROGRESS.md`: historical checkpoint notes (archival).
- `Cadence/CHINA_INFRASTRUCTURE_INSIGHTS.md`: motivation/thesis context (archival).

## Manufacturing-Readiness Goals

Reference goals for "manufacturable pre-silicon package ready":

1. Fix DC library flow correctness (resolve `.lib` vs `.db` target library usage).
2. Lock Synopsys/Calibre license environment in scripted runs.
3. Move from smoke checks to real signoff gates (full STA + DRC + LVS; add PEX where applicable).
4. Define and pass corners/mismatch/yield criteria, then freeze a tapeout-candidate revision.

If a reference note conflicts with the core docs, follow the core docs.
