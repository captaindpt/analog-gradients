#!/usr/bin/env python3
"""Fit global and phase-aware ODE models to measured LIF waveform data."""

import argparse
import csv
import math
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_IN_CSV = REPO_DIR / "competition" / "data" / "lif_neuron_waveform.csv"
DEFAULT_OUT_TRACE = REPO_DIR / "competition" / "analysis" / "lif_ode_fit_trace.csv"
DEFAULT_OUT_SUMMARY = REPO_DIR / "competition" / "analysis" / "lif_ode_fit_summary.md"


def solve_linear(system, rhs):
    """Gaussian elimination for small dense systems."""
    n = len(rhs)
    a = [row[:] for row in system]
    b = rhs[:]

    for i in range(n):
        piv = i
        for r in range(i + 1, n):
            if abs(a[r][i]) > abs(a[piv][i]):
                piv = r
        a[i], a[piv] = a[piv], a[i]
        b[i], b[piv] = b[piv], b[i]

        if abs(a[i][i]) < 1e-20:
            raise RuntimeError("Singular system in fit.")

        inv = 1.0 / a[i][i]
        for c in range(i, n):
            a[i][c] *= inv
        b[i] *= inv

        for r in range(n):
            if r == i:
                continue
            fac = a[r][i]
            if fac == 0:
                continue
            for c in range(i, n):
                a[r][c] -= fac * a[i][c]
            b[r] -= fac * b[i]

    return b


def fit_linear(feats, ys, ridge=1e-18):
    p = len(feats[0])
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for f, y in zip(feats, ys):
        for r in range(p):
            xty[r] += f[r] * y
            for c in range(p):
                xtx[r][c] += f[r] * f[c]
    for i in range(p):
        xtx[i][i] += ridge
    return solve_linear(xtx, xty)


def score(y_true, y_pred):
    mse = sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)
    rmse = math.sqrt(mse)
    mean = sum(y_true) / len(y_true)
    sst = sum((x - mean) ** 2 for x in y_true)
    sse = sum((a - b) ** 2 for a, b in zip(y_true, y_pred))
    r2 = 1.0 - (sse / sst if sst > 0 else 0.0)
    return rmse, r2


def classify_phase(spike_v, out_v, dmem_dt):
    # Reset/refractory: high spike or low buffered output.
    if spike_v > 0.9 or out_v < 0.9:
        return "reset"
    # Outside reset, sign of derivative separates charging from passive decay.
    if dmem_dt >= 0:
        return "charge"
    return "decay"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", default=str(DEFAULT_IN_CSV))
    parser.add_argument("--trace-out", default=str(DEFAULT_OUT_TRACE))
    parser.add_argument("--summary-out", default=str(DEFAULT_OUT_SUMMARY))
    return parser.parse_args()


def main():
    args = parse_args()
    in_csv = Path(args.input_csv).resolve()
    out_trace = Path(args.trace_out).resolve()
    out_summary = Path(args.summary_out).resolve()
    out_trace.parent.mkdir(parents=True, exist_ok=True)
    out_summary.parent.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(in_csv.open("r", encoding="utf-8")))
    if len(rows) < 3:
        raise SystemExit("Not enough waveform points.")

    t_ns = [float(r["time_ns"]) for r in rows]
    mem = [float(r["mem"]) for r in rows]
    out = [float(r["out"]) for r in rows]
    spike = [float(r["spike"]) for r in rows]

    dt_s = (t_ns[1] - t_ns[0]) * 1e-9
    if dt_s <= 0:
        raise SystemExit("Invalid timestep.")

    dmem_dt = [(mem[i + 1] - mem[i]) / dt_s for i in range(len(mem) - 1)]
    feats = [[mem[i], out[i], spike[i], 1.0] for i in range(len(dmem_dt))]

    # Baseline global model.
    global_params = fit_linear(feats, dmem_dt)
    gpred = [
        global_params[0] * f[0]
        + global_params[1] * f[1]
        + global_params[2] * f[2]
        + global_params[3]
        for f in feats
    ]
    g_rmse, g_r2 = score(dmem_dt, gpred)

    g_mem_step = [mem[0]]
    for i in range(len(mem) - 1):
        g_mem_step.append(mem[i] + gpred[i] * dt_s)
    g_trace_rmse = math.sqrt(
        sum((mem[i + 1] - g_mem_step[i + 1]) ** 2 for i in range(len(mem) - 1))
        / (len(mem) - 1)
    )

    # Phase-aware piecewise model.
    phases = [classify_phase(spike[i], out[i], dmem_dt[i]) for i in range(len(dmem_dt))]
    phase_names = ["charge", "reset", "decay"]
    phase_models = {}
    phase_preds = [0.0] * len(dmem_dt)
    phase_metrics = {}

    for ph in phase_names:
        idx = [i for i, p in enumerate(phases) if p == ph]
        if len(idx) < 4:
            # Fallback to global parameters if phase is undersampled.
            phase_models[ph] = global_params[:]
            phase_metrics[ph] = {"n": len(idx), "rmse": float("nan"), "r2": float("nan")}
            continue
        ph_feats = [feats[i] for i in idx]
        ph_ys = [dmem_dt[i] for i in idx]
        ph_params = fit_linear(ph_feats, ph_ys)
        phase_models[ph] = ph_params
        ph_pred = [
            ph_params[0] * f[0] + ph_params[1] * f[1] + ph_params[2] * f[2] + ph_params[3]
            for f in ph_feats
        ]
        ph_rmse, ph_r2 = score(ph_ys, ph_pred)
        phase_metrics[ph] = {"n": len(idx), "rmse": ph_rmse, "r2": ph_r2}
        for k, i in enumerate(idx):
            phase_preds[i] = ph_pred[k]

    pw_rmse, pw_r2 = score(dmem_dt, phase_preds)

    pw_mem_step = [mem[0]]
    for i in range(len(mem) - 1):
        pw_mem_step.append(mem[i] + phase_preds[i] * dt_s)
    pw_trace_rmse = math.sqrt(
        sum((mem[i + 1] - pw_mem_step[i + 1]) ** 2 for i in range(len(mem) - 1))
        / (len(mem) - 1)
    )

    with out_trace.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "time_ns",
                "phase",
                "mem_meas_v",
                "mem_model_global_step_v",
                "mem_model_piecewise_step_v",
                "out_v",
                "spike_v",
                "dmem_dt_meas_v_per_s",
                "dmem_dt_global_v_per_s",
                "dmem_dt_piecewise_v_per_s",
            ]
        )
        for i in range(len(mem)):
            phase_name = phases[i] if i < len(phases) else ""
            d_meas = dmem_dt[i] if i < len(dmem_dt) else ""
            d_g = gpred[i] if i < len(gpred) else ""
            d_p = phase_preds[i] if i < len(phase_preds) else ""
            w.writerow(
                [
                    f"{t_ns[i]:.3f}",
                    phase_name,
                    f"{mem[i]:.9f}",
                    f"{g_mem_step[i]:.9f}",
                    f"{pw_mem_step[i]:.9f}",
                    f"{out[i]:.9f}",
                    f"{spike[i]:.9f}",
                    d_meas if d_meas == "" else f"{d_meas:.6e}",
                    d_g if d_g == "" else f"{d_g:.6e}",
                    d_p if d_p == "" else f"{d_p:.6e}",
                ]
            )

    lines = []
    lines.append("# LIF ODE Fit Summary")
    lines.append("")
    lines.append("Input waveform:")
    lines.append(f"- `{in_csv}`")
    lines.append("")
    lines.append("## Global Linear Model (Baseline)")
    lines.append("")
    lines.append("`dV/dt = a*V + b*out + c*spike + d`")
    lines.append("")
    lines.append(f"- a = {global_params[0]:.6e} 1/s")
    lines.append(f"- b = {global_params[1]:.6e} 1/s")
    lines.append(f"- c = {global_params[2]:.6e} 1/s")
    lines.append(f"- d = {global_params[3]:.6e} V/s")
    if global_params[0] < 0:
        lines.append(f"- implied tau (from a) = {(-1.0 / global_params[0]) * 1e9:.3f} ns")
    lines.append(f"- derivative RMSE = {g_rmse:.6e} V/s")
    lines.append(f"- derivative R^2 = {g_r2:.6f}")
    lines.append(f"- one-step reconstruction RMSE = {g_trace_rmse:.6e} V")
    lines.append("")
    lines.append("## Phase-Aware Piecewise Model")
    lines.append("")
    lines.append(
        "Phase labels are derived from measured signals:\n"
        "- `reset`: `spike > 0.9V` or `out < 0.9V`\n"
        "- `charge`: outside reset and `dV/dt >= 0`\n"
        "- `decay`: outside reset and `dV/dt < 0`"
    )
    lines.append("")
    lines.append("Per-phase model form: `dV/dt = a*V + b*out + c*spike + d`")
    lines.append("")
    for ph in phase_names:
        p = phase_models[ph]
        m = phase_metrics[ph]
        lines.append(f"- {ph} samples = {m['n']}")
        lines.append(f"  - a = {p[0]:.6e} 1/s")
        lines.append(f"  - b = {p[1]:.6e} 1/s")
        lines.append(f"  - c = {p[2]:.6e} 1/s")
        lines.append(f"  - d = {p[3]:.6e} V/s")
        if not math.isnan(m["rmse"]):
            lines.append(f"  - phase derivative RMSE = {m['rmse']:.6e} V/s")
            lines.append(f"  - phase derivative R^2 = {m['r2']:.6f}")
    lines.append("")
    lines.append(f"- piecewise derivative RMSE = {pw_rmse:.6e} V/s")
    lines.append(f"- piecewise derivative R^2 = {pw_r2:.6f}")
    lines.append(f"- piecewise one-step reconstruction RMSE = {pw_trace_rmse:.6e} V")
    lines.append("")
    lines.append("## Comparison")
    lines.append("")
    lines.append(
        f"- derivative R^2 improvement: {g_r2:.6f} -> {pw_r2:.6f} "
        f"(delta = {pw_r2 - g_r2:+.6f})"
    )
    lines.append(
        f"- one-step RMSE improvement: {g_trace_rmse:.6e} -> {pw_trace_rmse:.6e} V"
    )
    lines.append("")
    lines.append("Artifacts:")
    lines.append(f"- `{out_trace}`")
    out_summary.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {out_trace}")
    print(f"Wrote {out_summary}")


if __name__ == "__main__":
    main()
