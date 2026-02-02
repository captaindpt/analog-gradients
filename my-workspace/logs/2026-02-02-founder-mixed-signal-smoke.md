# Session: 2026-02-02 - Founder Mixed-Signal Smoke

## Summary

Completed first mixed-signal founder-evidence artifact:
digital enable gating of analog feed-forward propagation in one Spectre run.

## Added

- `netlists/neuro_tile4_mixed_signal.scs`
- `ocean/test_neuro_tile4_mixed_signal.ocn`
- `competition/mixed-signal-smoke-evidence.md`

## Build Integration

- `build.sh` now supports:
  - `./build.sh neuro_tile4_mixed_signal`
  - Included in `./build.sh all`

## Verification Result

From `results/neuro_tile4_mixed_signal_test.txt`:

- Enable rising edge: `140.50ns`
- Downstream spikes before enable: `spike1=0 spike2=0 spike3=0`
- Downstream spikes after enable: `spike1=7 spike2=7 spike3=7`

## Founder Track Impact

This confirms mixed-signal control over timing propagation, completing the
phase-1 founder evidence pack (ODE fit + temporal sensitivity + energy/spike +
mixed-signal gating).
