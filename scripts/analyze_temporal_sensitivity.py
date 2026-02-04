#!/usr/bin/env python3
"""Extract temporal sensitivity metrics with fit quality and uncertainty."""

import csv
import math
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
SWEEP_CSV = REPO_DIR / "competition" / "sweeps" / "neuro_tile4_coupled_sweep.csv"
OUT_DIR = REPO_DIR / "competition" / "analysis"
OUT_SLOPE_CSV = OUT_DIR / "temporal_sensitivity_slopes.csv"
OUT_MD = OUT_DIR / "temporal_sensitivity_summary.md"


def parse_float(value):
    if value.endswith("k"):
        return float(value[:-1]) * 1e3
    if value.endswith("M"):
        return float(value[:-1]) * 1e6
    return float(value)


def parse_times(field):
    return [float(x.strip()) for x in field.split(",")]


def linear_fit(xs, ys):
    n = len(xs)
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    sxx = sum((x - x_mean) ** 2 for x in xs)
    sxy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    slope = sxy / sxx if sxx > 0 else 0.0
    intercept = y_mean - slope * x_mean

    pred = [slope * x + intercept for x in xs]
    sse = sum((y - yp) ** 2 for y, yp in zip(ys, pred))
    sst = sum((y - y_mean) ** 2 for y in ys)
    r2 = 1.0 - (sse / sst if sst > 0 else 0.0)

    if n > 2 and sxx > 0:
        sigma2 = sse / (n - 2)
        slope_stderr = math.sqrt(max(sigma2 / sxx, 0.0))
    else:
        slope_stderr = float("nan")

    return slope, intercept, r2, slope_stderr


def min_nonzero_step(vals):
    uniq = sorted(set(vals))
    if len(uniq) < 2:
        return 0.0
    deltas = [b - a for a, b in zip(uniq, uniq[1:]) if b - a > 0]
    if not deltas:
        return 0.0
    return min(deltas)


def format_num(v, digits):
    if isinstance(v, float) and math.isnan(v):
        return "nan"
    return f"{v:.{digits}f}"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(SWEEP_CSV.open("r", encoding="utf-8")))
    pass_rows = [r for r in rows if r.get("pass") == "PASS"]
    if not pass_rows:
        raise SystemExit("Sweep CSV has no PASS rows.")

    grouped = {}
    for r in pass_rows:
        key = parse_float(r["rleak"])
        grouped.setdefault(key, []).append(r)

    slope_rows = []
    for rleak_ohm, group in sorted(grouped.items()):
        group_sorted = sorted(group, key=lambda g: parse_float(g["r_fb"]))
        xs = [parse_float(g["r_fb"]) for g in group_sorted]

        for ch in range(4):
            ys = [parse_times(g["first_spike_times_ns"])[ch] for g in group_sorted]
            slope, intercept, r2, slope_stderr = linear_fit(xs, ys)
            ci95 = 1.96 * slope_stderr if not math.isnan(slope_stderr) else float("nan")
            slope_rows.append(
                {
                    "rleak_ohm": f"{rleak_ohm:.0f}",
                    "channel": f"spike{ch}",
                    "n_points": str(len(xs)),
                    "dt_dr_fb_ns_per_ohm": f"{slope:.10f}",
                    "dt_dr_fb_ns_per_kohm": f"{slope * 1000:.7f}",
                    "intercept_ns": f"{intercept:.6f}",
                    "r2": f"{r2:.6f}",
                    "slope_stderr_ns_per_kohm": (
                        f"{slope_stderr * 1000:.7f}" if not math.isnan(slope_stderr) else "nan"
                    ),
                    "slope_ci95_low_ns_per_kohm": (
                        f"{(slope - ci95) * 1000:.7f}" if not math.isnan(ci95) else "nan"
                    ),
                    "slope_ci95_high_ns_per_kohm": (
                        f"{(slope + ci95) * 1000:.7f}" if not math.isnan(ci95) else "nan"
                    ),
                    "first_spike_min_ns": f"{min(ys):.6f}",
                    "first_spike_max_ns": f"{max(ys):.6f}",
                    "min_nonzero_step_ns": f"{min_nonzero_step(ys):.6f}",
                }
            )

    with OUT_SLOPE_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "rleak_ohm",
                "channel",
                "n_points",
                "dt_dr_fb_ns_per_ohm",
                "dt_dr_fb_ns_per_kohm",
                "intercept_ns",
                "r2",
                "slope_stderr_ns_per_kohm",
                "slope_ci95_low_ns_per_kohm",
                "slope_ci95_high_ns_per_kohm",
                "first_spike_min_ns",
                "first_spike_max_ns",
                "min_nonzero_step_ns",
            ],
        )
        w.writeheader()
        w.writerows(slope_rows)

    by_channel = {}
    for r in slope_rows:
        by_channel.setdefault(r["channel"], []).append(r)

    lines = []
    lines.append("# Temporal Sensitivity Summary")
    lines.append("")
    lines.append("Source sweep:")
    lines.append(f"- `{SWEEP_CSV}`")
    lines.append("")
    lines.append("Per-rleak fit outputs (`dt_spike/dr_fb`) are in:")
    lines.append(f"- `{OUT_SLOPE_CSV}`")
    lines.append("")
    lines.append("PASS rows used from sweep CSV:")
    lines.append(f"- `{len(pass_rows)}` / `{len(rows)}`")
    lines.append("")
    lines.append("## Channel-Aggregated Sensitivity (`ns/kOhm`)")
    lines.append("")
    lines.append("| Channel | Min Slope | Max Slope | Mean Slope | Mean R2 | Mean CI95 Half-Width |")
    lines.append("|---------|-----------|-----------|------------|---------|----------------------|")
    for ch in sorted(by_channel.keys()):
        vals = [float(r["dt_dr_fb_ns_per_kohm"]) for r in by_channel[ch]]
        r2s = [float(r["r2"]) for r in by_channel[ch]]
        cis = []
        for r in by_channel[ch]:
            lo = r["slope_ci95_low_ns_per_kohm"]
            hi = r["slope_ci95_high_ns_per_kohm"]
            if lo == "nan" or hi == "nan":
                continue
            cis.append((float(hi) - float(lo)) / 2.0)
        mean = sum(vals) / len(vals)
        mean_r2 = sum(r2s) / len(r2s)
        mean_ci = (sum(cis) / len(cis)) if cis else float("nan")
        lines.append(
            f"| {ch} | {min(vals):.6f} | {max(vals):.6f} | {mean:.6f} | {mean_r2:.5f} | {format_num(mean_ci, 6)} |"
        )

    lines.append("")
    lines.append("## Per-Rleak Fit Detail")
    lines.append("")
    lines.append("| rleak (Ohm) | Channel | N | Slope (ns/kOhm) | R2 | CI95 Low | CI95 High | Min Step (ns) |")
    lines.append("|-------------|---------|---|------------------|----|----------|-----------|---------------|")
    for r in slope_rows:
        lines.append(
            f"| {r['rleak_ohm']} | {r['channel']} | {r['n_points']} | {r['dt_dr_fb_ns_per_kohm']} | {r['r2']} | {r['slope_ci95_low_ns_per_kohm']} | {r['slope_ci95_high_ns_per_kohm']} | {r['min_nonzero_step_ns']} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "This report now includes fit quality (R2), slope uncertainty (95% CI), "
        "and first-spike quantization diagnostics to distinguish physical trends "
        "from measurement-resolution artifacts."
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_SLOPE_CSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
