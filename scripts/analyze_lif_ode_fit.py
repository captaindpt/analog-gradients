#!/usr/bin/env python3
"""Fit a first-order LIF-like ODE to measured lif_neuron waveform data."""

import csv
import math
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
IN_CSV = REPO_DIR / "competition" / "data" / "lif_neuron_waveform.csv"
OUT_DIR = REPO_DIR / "competition" / "analysis"
OUT_TRACE = OUT_DIR / "lif_ode_fit_trace.csv"
OUT_SUMMARY = OUT_DIR / "lif_ode_fit_summary.md"


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


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(IN_CSV.open("r", encoding="utf-8")))
    if len(rows) < 3:
        raise SystemExit("Not enough waveform points.")

    t_ns = [float(r["time_ns"]) for r in rows]
    mem = [float(r["mem"]) for r in rows]
    out = [float(r["out"]) for r in rows]
    spike = [float(r["spike"]) for r in rows]

    dt_s = (t_ns[1] - t_ns[0]) * 1e-9
    if dt_s <= 0:
        raise SystemExit("Invalid timestep.")

    # Build derivative samples (forward difference).
    dmem_dt = [(mem[i + 1] - mem[i]) / dt_s for i in range(len(mem) - 1)]

    # Model:
    # dV/dt = a*V + b*U_out + c*U_spike + d
    # Use points where signals are finite (all points are finite here).
    feats = []
    ys = []
    for i in range(len(dmem_dt)):
        feats.append([mem[i], out[i], spike[i], 1.0])
        ys.append(dmem_dt[i])

    # Least squares normal equations.
    p = 4
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for f, y in zip(feats, ys):
        for r in range(p):
            xty[r] += f[r] * y
            for c in range(p):
                xtx[r][c] += f[r] * f[c]

    a, b, c, d = solve_linear(xtx, xty)

    dfit = []
    for i in range(len(dmem_dt)):
        v = mem[i]
        uo = out[i]
        us = spike[i]
        dfit.append(a * v + b * uo + c * us + d)

    # Derivative fit metrics.
    mse = sum((m - p_) ** 2 for m, p_ in zip(dmem_dt, dfit)) / len(dmem_dt)
    rmse = math.sqrt(mse)
    y_mean = sum(dmem_dt) / len(dmem_dt)
    ss_tot = sum((m - y_mean) ** 2 for m in dmem_dt)
    ss_res = sum((m - p_) ** 2 for m, p_ in zip(dmem_dt, dfit))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    # Forward simulation from measured V(0).
    mem_model = [mem[0]]
    for i in range(len(mem) - 1):
        v = mem_model[-1]
        uo = out[i]
        us = spike[i]
        dv = (a * v + b * uo + c * us + d) * dt_s
        mem_model.append(v + dv)

    trace_mse = sum((m - p_) ** 2 for m, p_ in zip(mem, mem_model)) / len(mem)
    trace_rmse = math.sqrt(trace_mse)

    with OUT_TRACE.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "time_ns",
                "mem_meas_v",
                "mem_model_v",
                "out_v",
                "spike_v",
                "dmem_dt_meas_v_per_s",
                "dmem_dt_fit_v_per_s",
            ]
        )
        for i in range(len(mem)):
            d_meas = dmem_dt[i] if i < len(dmem_dt) else ""
            d_fit = dfit[i] if i < len(dfit) else ""
            w.writerow(
                [
                    f"{t_ns[i]:.3f}",
                    f"{mem[i]:.9f}",
                    f"{mem_model[i]:.9f}",
                    f"{out[i]:.9f}",
                    f"{spike[i]:.9f}",
                    d_meas if d_meas == "" else f"{d_meas:.6e}",
                    d_fit if d_fit == "" else f"{d_fit:.6e}",
                ]
            )

    tau_ns = ""
    if a < 0:
        tau_ns = f"{(-1.0 / a) * 1e9:.3f}"

    lines = []
    lines.append("# LIF ODE Fit Summary")
    lines.append("")
    lines.append("Input waveform:")
    lines.append(f"- `{IN_CSV}`")
    lines.append("")
    lines.append("Fitted model:")
    lines.append("")
    lines.append("`dV/dt = a*V + b*out + c*spike + d`")
    lines.append("")
    lines.append(f"- a = {a:.6e} 1/s")
    lines.append(f"- b = {b:.6e} 1/s")
    lines.append(f"- c = {c:.6e} 1/s")
    lines.append(f"- d = {d:.6e} V/s")
    if tau_ns:
        lines.append(f"- implied tau (from a) = {tau_ns} ns")
    lines.append("")
    lines.append("Fit quality:")
    lines.append(f"- derivative RMSE = {rmse:.6e} V/s")
    lines.append(f"- derivative R^2 = {r2:.6f}")
    lines.append(f"- trajectory RMSE = {trace_rmse:.6e} V")
    lines.append("")
    lines.append("Quiet-phase fit (spike < 0.2V):")

    quiet_idx = [i for i in range(len(dmem_dt)) if spike[i] < 0.2]
    q_feats = [[mem[i], out[i], 1.0] for i in quiet_idx]
    q_ys = [dmem_dt[i] for i in quiet_idx]

    if len(q_feats) >= 4:
        q_p = 3
        q_xtx = [[0.0] * q_p for _ in range(q_p)]
        q_xty = [0.0] * q_p
        for f, y in zip(q_feats, q_ys):
            for r in range(q_p):
                q_xty[r] += f[r] * y
                for c_ in range(q_p):
                    q_xtx[r][c_] += f[r] * f[c_]
        aq, bq, dq = solve_linear(q_xtx, q_xty)
        q_pred = [aq * f[0] + bq * f[1] + dq for f in q_feats]
        q_mse = sum((m - p_) ** 2 for m, p_ in zip(q_ys, q_pred)) / len(q_ys)
        q_rmse = math.sqrt(q_mse)
        q_mean = sum(q_ys) / len(q_ys)
        q_ss_tot = sum((m - q_mean) ** 2 for m in q_ys)
        q_ss_res = sum((m - p_) ** 2 for m, p_ in zip(q_ys, q_pred))
        q_r2 = 1.0 - (q_ss_res / q_ss_tot if q_ss_tot > 0 else 0.0)
        lines.append(f"- quiet samples = {len(q_feats)} / {len(dmem_dt)}")
        lines.append(f"- quiet model: dV/dt = aq*V + bq*out + dq")
        lines.append(f"- aq = {aq:.6e} 1/s")
        lines.append(f"- bq = {bq:.6e} 1/s")
        lines.append(f"- dq = {dq:.6e} V/s")
        if aq < 0:
            lines.append(f"- implied quiet tau = {(-1.0 / aq) * 1e9:.3f} ns")
        lines.append(f"- quiet derivative RMSE = {q_rmse:.6e} V/s")
        lines.append(f"- quiet derivative R^2 = {q_r2:.6f}")
    else:
        lines.append("- quiet-phase fit unavailable (insufficient samples)")

    lines.append("")
    lines.append("Decay-window fit (12ns to 19ns):")
    decay_idx = [
        i for i in range(len(dmem_dt))
        if t_ns[i] >= 12.0 and t_ns[i] <= 19.0
    ]
    if len(decay_idx) >= 4:
        dx = [mem[i] for i in decay_idx]
        dy = [dmem_dt[i] for i in decay_idx]
        xm = sum(dx) / len(dx)
        ym = sum(dy) / len(dy)
        num = sum((x - xm) * (y - ym) for x, y in zip(dx, dy))
        den = sum((x - xm) ** 2 for x in dx)
        m = num / den if den > 0 else 0.0
        q = ym - m * xm
        pred = [m * x + q for x in dx]
        dmse = sum((a_ - b_) ** 2 for a_, b_ in zip(dy, pred)) / len(dy)
        drmse = math.sqrt(dmse)
        dss_tot = sum((v - ym) ** 2 for v in dy)
        dss_res = sum((a_ - b_) ** 2 for a_, b_ in zip(dy, pred))
        dr2 = 1.0 - (dss_res / dss_tot if dss_tot > 0 else 0.0)
        lines.append(f"- decay samples = {len(decay_idx)}")
        lines.append(f"- decay model: dV/dt = m*V + q")
        lines.append(f"- m = {m:.6e} 1/s")
        lines.append(f"- q = {q:.6e} V/s")
        if m < 0:
            lines.append(f"- implied decay tau = {(-1.0 / m) * 1e9:.3f} ns")
        lines.append(f"- decay derivative RMSE = {drmse:.6e} V/s")
        lines.append(f"- decay derivative R^2 = {dr2:.6f}")
    else:
        lines.append("- decay-window fit unavailable (insufficient samples)")

    lines.append("")
    lines.append("Artifacts:")
    lines.append(f"- `{OUT_TRACE}`")
    OUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_TRACE}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
