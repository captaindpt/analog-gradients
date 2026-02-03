#!/usr/bin/env python3
"""Compute LIF energy-per-spike statistics and bootstrap CI from trace CSV."""

import argparse
import csv
import math
import random
from pathlib import Path


def crossing_times(v, t, vth=0.9):
    times = []
    for i in range(1, len(v)):
        v0, v1 = v[i - 1], v[i]
        if v0 < vth and v1 > vth:
            frac = (vth - v0) / (v1 - v0) if (v1 - v0) != 0 else 0.0
            frac = min(1.0, max(0.0, frac))
            tc = t[i - 1] + frac * (t[i] - t[i - 1])
            times.append(tc)
    return times


def integrate_between(t, y, ta, tb):
    if tb <= ta:
        return 0.0
    e = 0.0
    for i in range(1, len(t)):
        t0, t1 = t[i - 1], t[i]
        if t1 <= ta or t0 >= tb:
            continue
        lo = max(t0, ta)
        hi = min(t1, tb)
        if hi <= lo:
            continue
        dt_seg = t1 - t0
        if dt_seg <= 0:
            continue
        y0, y1 = y[i - 1], y[i]
        y_lo = y0 + (y1 - y0) * ((lo - t0) / dt_seg)
        y_hi = y0 + (y1 - y0) * ((hi - t0) / dt_seg)
        e += 0.5 * (y_lo + y_hi) * (hi - lo)
    return e


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--trace-csv", required=True)
    p.add_argument("--summary-txt", required=True)
    p.add_argument("--summary-md", required=True)
    p.add_argument("--bootstrap-csv", required=True)
    p.add_argument("--bootstrap-n", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--title", default="LIF Energy Summary")
    return p.parse_args()


def main():
    args = parse_args()
    trace_csv = Path(args.trace_csv).resolve()
    summary_txt = Path(args.summary_txt).resolve()
    summary_md = Path(args.summary_md).resolve()
    boot_csv = Path(args.bootstrap_csv).resolve()
    summary_txt.parent.mkdir(parents=True, exist_ok=True)
    summary_md.parent.mkdir(parents=True, exist_ok=True)
    boot_csv.parent.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(trace_csv.open("r", encoding="utf-8")))
    if len(rows) < 3:
        raise SystemExit("Trace CSV has insufficient rows.")

    t_ns = [float(r["time_ns"]) for r in rows]
    pwr = [float(r["power_w"]) for r in rows]
    spk = [float(r["spike_v"]) for r in rows]
    t_s = [x * 1e-9 for x in t_ns]
    dt = t_s[1] - t_s[0]
    if dt <= 0:
        raise SystemExit("Invalid time step in trace CSV.")

    spike_t = crossing_times(spk, t_s, 0.9)
    if not spike_t:
        raise SystemExit("No spikes found in trace.")

    t0 = t_s[0]
    t1 = t_s[-1]
    bounds = [t0]
    for i in range(len(spike_t) - 1):
        bounds.append(0.5 * (spike_t[i] + spike_t[i + 1]))
    bounds.append(t1)

    event_e = [integrate_between(t_s, pwr, bounds[i], bounds[i + 1]) for i in range(len(spike_t))]
    total_e = integrate_between(t_s, pwr, t0, t1)
    n_spk = len(spike_t)
    eps = total_e / n_spk if n_spk > 0 else float("nan")

    mean_event = sum(event_e) / len(event_e)
    var_event = sum((x - mean_event) ** 2 for x in event_e) / max(len(event_e) - 1, 1)
    std_event = math.sqrt(var_event)
    cv_event = std_event / mean_event if mean_event != 0 else float("nan")

    rng = random.Random(args.seed)
    boot_means = []
    for _ in range(args.bootstrap_n):
        sample = [event_e[rng.randrange(len(event_e))] for _ in range(len(event_e))]
        boot_means.append(sum(sample) / len(sample))
    boot_means.sort()
    lo = boot_means[int(0.025 * args.bootstrap_n)]
    hi = boot_means[int(0.975 * args.bootstrap_n)]
    boot_mean = sum(boot_means) / len(boot_means)

    with boot_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["event_index", "spike_time_ns", "event_energy_j", "event_energy_pj"])
        for i, (ts, e) in enumerate(zip(spike_t, event_e), 1):
            w.writerow([i, f"{ts * 1e9:.6f}", f"{e:.9e}", f"{e * 1e12:.6f}"])
        w.writerow([])
        w.writerow(["bootstrap_mean_energy_per_spike_j", "bootstrap_mean_energy_per_spike_pj"])
        for b in boot_means:
            w.writerow([f"{b:.9e}", f"{b * 1e12:.6f}"])

    txt_lines = [
        f"=== {args.title} ===",
        "",
        f"Total energy (window): {total_e:.6e} J",
        f"Detected spikes: {n_spk}",
        f"Energy per spike (total/spike): {eps:.6e} J",
        f"Energy per spike (total/spike): {eps * 1e12:.6f} pJ",
        "",
        f"Per-spike event energies (count): {len(event_e)}",
        f"Per-spike mean (event windows): {mean_event:.6e} J",
        f"Per-spike std (event windows): {std_event:.6e} J",
        f"Per-spike CV (event windows): {cv_event:.6f}",
        f"Bootstrap mean energy/spike (N={args.bootstrap_n}, seed={args.seed}): {boot_mean:.6e} J",
        f"Bootstrap 95% CI: [{lo:.6e}, {hi:.6e}] J",
        f"Bootstrap artifact: {boot_csv}",
        f"Trace CSV: {trace_csv}",
    ]
    summary_txt.write_text("\n".join(txt_lines) + "\n", encoding="utf-8")

    md_lines = [
        f"# {args.title}",
        "",
        f"Source trace: `{trace_csv}`",
        "",
        f"- Total energy (window): `{total_e:.6e}` J",
        f"- Detected spikes: `{n_spk}`",
        f"- Energy per spike (total/spike): `{eps:.6e}` J (`{eps * 1e12:.6f}` pJ)",
        f"- Event-window mean per spike: `{mean_event:.6e}` J (`{mean_event * 1e12:.6f}` pJ)",
        f"- Event-window std: `{std_event:.6e}` J (`{std_event * 1e12:.6f}` pJ)",
        f"- Event-window CV: `{cv_event:.6f}`",
        f"- Bootstrap mean (N={args.bootstrap_n}, seed={args.seed}): `{boot_mean:.6e}` J",
        f"- Bootstrap 95% CI: `[{lo:.6e}, {hi:.6e}]` J",
        "",
        "Method:",
        "- Integrate `P(t) = VDD * (-I(V_VDD))` from exported trace.",
        "- Detect spike crossings at 0.9V with linear interpolation.",
        "- Partition per-spike windows by midpoints between adjacent spike times.",
        "- Bootstrap the mean per-spike event energy from window energies.",
        "",
        "Artifacts:",
        f"- Summary TXT: `{summary_txt}`",
        f"- Bootstrap CSV: `{boot_csv}`",
    ]
    summary_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"Wrote {summary_txt}")
    print(f"Wrote {summary_md}")
    print(f"Wrote {boot_csv}")


if __name__ == "__main__":
    main()
