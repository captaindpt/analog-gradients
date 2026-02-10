# Memristor Primitive Master Notes and Spec (Physics-First)

Date: 2026-02-09
Status: Planning baseline, execution scaffold active
Track: new physical primitive first, compact model second, CMOS fallback third

This is the single master notes file for the memristor primitive workstream.
All planning, equations, acceptance criteria, and phase gates should stay here.

## 1) Mission and Minimum Success

Build a new memristive primitive for this repo and prove it in two stages:

1. Physics-only proof: show real memristive behavior in physical simulation.
2. Circuit-level proof: export/fitted compact model that passes Spectre/OCEAN checks.

Minimum success definition for this project:

1. The primitive shows paper-consistent memristive behavior.
2. Energy per event is reported and is acceptable for proof-of-concept even if
   it is up to 2x-3x worse than reference points.
3. The model is reusable in repo flows (`build.sh`, OCEAN PASS/FAIL artifacts).

## 2) Scope, Non-Goals, and Decision Rules

In scope:

1. Oxide-based bipolar VCM ReRAM class.
2. Headless, scriptable physics simulation.
3. Quantitative mapping from physics outputs to compact model parameters.
4. Deterministic verification gates in this repo.

Out of scope (for this phase):

1. Layout/device fabrication signoff.
2. Full process co-optimization across many materials.
3. Immediate large-scale AIMC training benchmarks.

Decision rules:

1. Prefer physically interpretable models over pure black-box fits.
2. Prefer robust, convergent simulation setup over maximal complexity.
3. Freeze acceptance bands early and tighten only after first passing proof.

## 3) Canonical Theory and Equation Set

These equations define what we mean by a compliant memristive primitive.

### 3.1 Chua 1971 (Foundational Element)

Source: `papers/12_chua_1971_memristor_missing_circuit_element.pdf`

Canonical relation:
- `dphi = M(q) dq`

Operational implications:

1. The element has memory through state dependence.
2. Under periodic excitation, i-v behavior shows pinched hysteresis in valid
   operating regimes.

### 3.2 Chua-Kang 1975 (General Memristive Systems)

Source: `papers/09_chua_kang_memristive_devices_1975.pdf`

General one-port memristive system form:

- `v(t) = R(w, i, t) * i(t)`
- `dw/dt = f(w, i, t)`

Operational implications:

1. Internal state `w` must be explicit and bounded.
2. Port behavior and state dynamics are coupled, not independent.

### 3.3 Strukov 2008 Drift-Coupled Physical Model

Source: `papers/13b_nature06932_missing_memristor_found.pdf`

Common simplified form from the paper:

- `v(t) = [Ron * w/D + Roff * (1 - w/D)] * i(t)`
- `dw/dt = mu_v * Ron/D * i(t)`

Interpretation for this project:

1. `w` is an effective conductive-region coordinate.
2. Ionic motion under field is the dominant mechanism in phase-A baseline.
3. Model must enforce bounds on `w` to avoid non-physical drift.

### 3.4 TEAM/VTEAM Compact Dynamics

Sources:
- `papers/02_TEAM_CCIT_804.pdf`
- `papers/10_vteam_improved_numerical_performance.pdf`

VTEAM state equation structure (piecewise voltage-threshold form):

- OFF branch: `dw/dt = koff * (v/voff - 1)^aoff * foff(w)` for `v > voff > 0`
- Sub-threshold: `dw/dt = 0` for `von < v < voff`
- ON branch: `dw/dt = kon * (v/von - 1)^aon * fon(w)` for `v < von < 0`

Modeling rules from these papers used in this repo:

1. Thresholded dynamics are preferred for stability and realism.
2. Windowing and state bounds are mandatory.
3. Numerically robust implementations are required to avoid stick and
   convergence artifacts.

### 3.5 Data-Driven Switching Surface Models

Sources:
- `papers/03_compact_VerilogA_ReRAM_switching.pdf`
- `papers/04_data_driven_VerilogA_ReRAM.pdf`

Takeaways adopted here:

1. Fit switching-rate surfaces `dR/dt` or `dR/dN` from measured/physics data.
2. Include state and bias dependence, not voltage-only curves.
3. Keep equations continuous/differentiable enough for simulator robustness.

## 4) Chosen Device Class and Anchor Paper

Primary target class:
- Oxide-based bipolar VCM ReRAM two-terminal primitive.

Anchor for phase-A calibration:
- `papers/13b_nature06932_missing_memristor_found.pdf`

Mechanism taxonomy companion:
- `papers/14_waser_aono_2007_nanoionics_resistive_switching.pdf`

Why this class:

1. Mainstream and well-cited.
2. Clear bridge from physics to compact model.
3. Compatible with existing Spectre/OCEAN verification path.

## 5) Tooling Strategy (Pragmatic)

Primary physics tool:
- Synopsys Sentaurus TCAD (headless).

Compact/circuit verification:
- Cadence Spectre + OCEAN.

Fallback physics options:
- COMSOL only if required coupling is impractical in Sentaurus.

Fallback primitive path if physical primitive stalls:
- CMOS emulator path using
  `papers/08_cmos_memristor_emulator_circuits.pdf`.

## 6) Physics Tool Readiness Checkpoint

Headless Sentaurus smoke run has been validated in this environment.

Validated commands/tool availability (from tcsh environment):

1. `sde`
2. `snmesh`
3. `sdevice`

Current smoke evidence (minimal semiconductor chain):

1. Script/log inputs:
   - `/tmp/mem_sde.scm`
   - `/tmp/mem_device.cmd`
   - `/tmp/mem_sde.log`
   - `/tmp/mem_sdevice.log`
2. Output artifacts:
   - `/tmp/memdev_bnd.tdr`
   - `/tmp/memdev_msh.tdr`
   - `/tmp/memdev_des.tdr`
   - `/tmp/memdev_des.plt`

Interpretation:

1. Toolchain and license path are working headlessly.
2. This checkpoint proves infrastructure only; it is not yet a memristive
   device-physics proof.

## 7) Primitive Compliance Criteria

### 7.1 Behavioral Must-Haves

1. Pinched hysteresis in i-v under bipolar periodic drive.
2. Clear SET and RESET transitions under pulse programming.
3. Stable ON and OFF states under low-disturb read windows.
4. Frequency dependence trend consistent with literature.
5. No unstable runaway/divergence in repeated cycles.

### 7.2 Quantitative Fit Bands (Initial)

For selected anchor operating region:

1. SET threshold error <= 20%.
2. RESET threshold error <= 20%.
3. ON/OFF ratio within 0.5x to 2x of target reference.
4. State-update monotonicity and saturation trend match qualitatively.

### 7.3 Energy Criteria (POC)

Switching-event energy definition:
- `E_sw = integral(V(t) * I(t) dt)` over pulse window.

Acceptance:

1. Report both `E_set` and `E_reset`.
2. Up to 2x-3x reference energy is acceptable for initial proof.
3. Larger gap requires explicit root-cause note and justification.

## 8) Experiment Matrix and Sweep Contracts

### 8.1 Phase A0: Environment and Baseline Setup

Outputs:

1. Reproducible run directory.
2. Simulation command manifest.
3. One convergent baseline deck.

### 8.2 Phase A1: Quasi-Static I-V and Hysteresis

Sweep set:

1. Bipolar triangular waveform amplitudes: `0.5, 1.0, 1.5 V`.
2. Sweep rates/frequencies: low, medium, high bands.
3. Both polarities with identical absolute drive.

Extracted metrics:

1. Hysteresis area.
2. Pinch-point current near zero bias.
3. Effective ON/OFF resistance at read bias.

### 8.3 Phase A2: Pulse SET/RESET Characterization

Pulse matrix:

1. SET pulse amplitude-width grid.
2. RESET pulse amplitude-width grid.
3. Fixed read-disturb check between programming pulses.

Extracted metrics:

1. Threshold voltage and width contours.
2. `dR/dN` and switching-rate trends.
3. Event energy per successful transition.

### 8.4 Phase A3: Retention and Endurance

Retention:

1. Read at low bias over delayed checkpoints.
2. Report drift slope and state-separation decay.

Endurance:

1. Program/erase cycling with periodic readback.
2. Report threshold drift and ON/OFF collapse trends.

### 8.5 Phase A4: Variability and Sensitivity (Optional in First Pass)

1. Perturb mobility, defect baseline, or interface parameters.
2. Report spread in threshold and resistance states.

## 9) Physics-to-Compact Model Mapping Spec

### 9.1 Parameters to Extract

From physics outputs, derive:

1. `R_on`, `R_off` and state bounds.
2. `v_on`, `v_off` thresholds.
3. `k_on`, `k_off`, `a_on`, `a_off` rate parameters.
4. Window/saturation parameters for `f_on(w)`, `f_off(w)`.
5. Optional asymmetry terms for up/down switching differences.

### 9.2 Mapping Workflow

1. Build cleaned switching-surface data table from phase-A runs.
2. Fit compact equation family (VTEAM-first) inside target envelope.
3. Validate fit on holdout pulse conditions.
4. Export parameter set with explicit fit-error report.

### 9.3 Fit Quality Metrics

1. RMS error on threshold extraction.
2. Relative error on ON/OFF ratio.
3. Relative error on event energy.
4. Pass/fail against section 7 bands.

## 10) Spectre/OCEAN Integration Contract

Required repo assets:

1. Primitive netlist or Verilog-A wrapper under `netlists/`.
2. OCEAN verifier under `ocean/test_memristor_*.ocn`.
3. Deterministic PASS/FAIL artifact in `results/*_test.txt`.
4. `build.sh` integration for one-command verification.

Current checkpoint already present:

1. Netlist: `netlists/memristor_vteam.scs`
2. OCEAN test: `ocean/test_memristor_vteam.ocn`
3. PASS artifact: `results/memristor_vteam_test.txt`

## 11) Data, Artifacts, and Reproducibility Layout

Planned structure:

1. `tcad/memristor/config/` for anchor environment and constants.
2. `tcad/memristor/templates/` for extraction schemas.
3. `tcad/memristor/runs/<timestamp>/` for per-run manifests and outputs.
4. `results/memristor_*/` for compact-model verification artifacts.

Current helper scripts:

1. `scripts/init_memristor_phase_a.sh`
2. `scripts/analyze_memristor_waveform.py`

## 12) Claims Policy and Scientific Hygiene

Required claim discipline:

1. Do not claim physical fabrication; claim simulation evidence only.
2. Keep "memristor" terminology aligned with explicit equation compliance.
3. Document model envelope where behavior is validated.
4. Use critique source `papers/11_missing_memristor_has_not_been_found.pdf`
   to keep wording precise and avoid over-claiming.

## 13) Risks and Mitigations

1. Risk: physical deck converges but shows only resistor-like behavior.
   Mitigation: explicitly add ionic/state dynamics and verify hysteresis metrics.
2. Risk: numerical artifacts mistaken for memristive behavior.
   Mitigation: cross-check sweep rate dependence, reverse sweeps, and bounds.
3. Risk: compact model overfits one bias regime.
   Mitigation: holdout pulse conditions and envelope declaration.
4. Risk: timeline slip on physics path.
   Mitigation: parallel CMOS-emulator backup with preserved interfaces.

## 14) Phase Gates and Evidence Checklist

Gate A0: planning complete

1. Anchor class and citations frozen.
2. Acceptance metrics frozen.

Gate A1: physics environment ready

1. Headless deck converges.
2. Reproducible run manifest exists.

Gate A2: memristive behavior reproduced

1. Pinched hysteresis demonstrated.
2. SET/RESET transitions extracted.

Gate A3: quantitative fit acceptable

1. Threshold/ratio/energy within agreed bands or justified.

Gate A4: compact model validated

1. Spectre model reproduces selected envelope.
2. OCEAN verifier emits deterministic PASS/FAIL.

Gate A5: workstream integration complete

1. `build.sh` target stable.
2. Docs/ticket/status all updated.

## 15) Immediate Execution Sequence (Next Work Session)

1. Promote the `/tmp` Sentaurus smoke chain into repo under `tcad/memristor/`.
2. Add script `scripts/run_memristor_phase_a_sentaurus.sh` with run manifest.
3. Add CSV extraction bridge from `.plt`/`.tdr` to analysis script input.
4. Run first phase-A sweep and publish baseline summary in `competition/` or
   `my-workspace/logs/` with explicit caveats.
