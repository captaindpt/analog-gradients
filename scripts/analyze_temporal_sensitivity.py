#!/usr/bin/env python3
"""Extract temporal sensitivity metrics from coupled-tile sweep artifacts."""

import csv
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


def linear_slope(xs, ys):
    n = len(xs)
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    den = sum((x - x_mean) ** 2 for x in xs)
    if den == 0:
        return 0.0
    return num / den


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(SWEEP_CSV.open("r", encoding="utf-8")))
    if not rows:
        raise SystemExit("Sweep CSV is empty.")

    grouped = {}
    for r in rows:
        key = parse_float(r["rleak"])
        grouped.setdefault(key, []).append(r)

    slope_rows = []
    for rleak_ohm, group in sorted(grouped.items()):
        group_sorted = sorted(group, key=lambda g: parse_float(g["r_fb"]))
        xs = [parse_float(g["r_fb"]) for g in group_sorted]

        for ch in range(4):
            ys = [parse_times(g["first_spike_times_ns"])[ch] for g in group_sorted]
            slope = linear_slope(xs, ys)
            slope_rows.append(
                {
                    "rleak_ohm": f"{rleak_ohm:.0f}",
                    "channel": f"spike{ch}",
                    "dt_dr_fb_ns_per_ohm": f"{slope:.8f}",
                    "dt_dr_fb_ns_per_kohm": f"{slope * 1000:.5f}",
                    "first_spike_min_ns": f"{min(ys):.3f}",
                    "first_spike_max_ns": f"{max(ys):.3f}",
                }
            )

    with OUT_SLOPE_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "rleak_ohm",
                "channel",
                "dt_dr_fb_ns_per_ohm",
                "dt_dr_fb_ns_per_kohm",
                "first_spike_min_ns",
                "first_spike_max_ns",
            ],
        )
        w.writeheader()
        w.writerows(slope_rows)

    by_channel = {}
    for r in slope_rows:
        by_channel.setdefault(r["channel"], []).append(float(r["dt_dr_fb_ns_per_kohm"]))

    lines = []
    lines.append("# Temporal Sensitivity Summary")
    lines.append("")
    lines.append("Source sweep:")
    lines.append(f"- `{SWEEP_CSV}`")
    lines.append("")
    lines.append("Per-rleak slopes (`dt_spike/dr_fb`) are in:")
    lines.append(f"- `{OUT_SLOPE_CSV}`")
    lines.append("")
    lines.append("## Channel-Aggregated Sensitivity (`ns/kOhm`)")
    lines.append("")
    lines.append("| Channel | Min | Max | Mean |")
    lines.append("|---------|-----|-----|------|")
    for ch in sorted(by_channel.keys()):
        vals = by_channel[ch]
        mean = sum(vals) / len(vals)
        lines.append(f"| {ch} | {min(vals):.5f} | {max(vals):.5f} | {mean:.5f} |")

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "These derivatives quantify how spike timing shifts as physical coupling "
        "resistance (`r_fb`) changes, providing a direct temporal-gradient metric."
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_SLOPE_CSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
