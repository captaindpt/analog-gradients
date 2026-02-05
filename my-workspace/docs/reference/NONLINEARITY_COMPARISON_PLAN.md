# Analog vs. Digital Nonlinearity Comparison Plan

## Objective

Demonstrate (or disprove) that analog circuits compute neural-network
nonlinearities more efficiently than digital implementations under matched
inputs and accuracy criteria.

Primary target: **softmax over N elements**.

## Scope

Comparison is **hybrid**:
- Linear ops (matmul) remain digital in both paths.
- Nonlinear ops (exp/sum/div/softmax) are digital in the baseline and analog in the hybrid.

## Metrics (Required)

1. **Energy**: pJ per operation (full softmax over N elements).
2. **Latency**: ns to settle within tolerance of expected output.
3. **Accuracy**: max error (L∞) and mean error (L2/RMSE).
4. **Transistor count**: area proxy (documented estimate).

## Input/Output Protocol

- Input: vector of logits in volts (analog path) and fixed-point words
  (digital path), derived from the same floating-point vector.
- Output: probability vector (sum=1), measured as voltages in analog path
  and fixed-point codes in digital path.
- Expected output: floating-point softmax reference with defined tolerance.

## Measurement Rules

### Energy

Compute energy by integrating instantaneous power:

`E = ∫ ( -I(VDD) * V(vdd) ) dt`

Requirements:
- Save `V_VDD:p` and `vdd` node waveform.
- Use identical integration windows for analog and digital.
- Declare whether IO conversion (DAC/ADC) is included or excluded.

### Latency

Define latency as the first time each output enters a tolerance band around
its expected value and stays within that band for a hold window.

Minimum:
- `|v_out(t) - v_ref| <= tol` for `t >= t_settle`.
- `hold_window_ns` documented.

### Accuracy

- `L∞` error per vector (max absolute error across outputs).
- RMSE per vector (optional).
- Pass/fail threshold explicitly defined (e.g., `L∞ <= 0.02`).

## Model-Fidelity Gate

Results are only **claimable** if the analog path uses a real CMOS PDK
(e.g., GPDK180 or better). Toy `mos1` models are **development-only** and
must be labeled as such in summaries.

## Required Artifacts

1. Vector set used (CSV + generator config).
2. Per-vector results (CSV).
3. Summary markdown with energy/latency/accuracy and clear scope.
4. Netlists and OCEAN tests for both analog and digital paths.

## Testbed Readiness Checklist

- [ ] Vector generator script exists and versioned.
- [ ] Benchmark runner exists and outputs per-vector CSV.
- [ ] Energy integration uses actual VDD waveform.
- [ ] Accuracy/latency definitions are explicit and enforced.
- [ ] PDK fidelity is recorded in summary (`toy` vs `PDK`).
- [ ] IO inclusion/exclusion is declared and consistent.

## Suggested File Paths

- Vector generator: `scripts/generate_softmax_vectors.py`
- Benchmark runner: `scripts/run_nonlinearity_vector_benchmark.py`
- Vectors: `competition/data/nonlinearity/softmax_vectors_n{N}.csv`
- Results: `competition/sweeps/nonlinearity/<run_id>/`
- Summary: `competition/analysis/nonlinearity_softmax_summary.md`
