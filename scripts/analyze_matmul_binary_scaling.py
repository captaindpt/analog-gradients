#!/usr/bin/env python3
"""Run a model-based binary matmul scaling sweep and emit plots/reports.

This script calibrates simple architecture models from the verified 2x2
transistor runs, then evaluates larger NxN binary workloads algorithmically.
"""

import argparse
import csv
import math
import random
import re
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, List, Sequence, Tuple


class Calibration:
    def __init__(
        self,
        digital_eop_j: float,
        digital_latency_ns: float,
        neuro_latency_ns: float,
        neuro_energy_j: float,
        neuro_partial_spikes: int,
        neuro_spike_model_j: float,
    ) -> None:
        self.digital_eop_j = digital_eop_j
        self.digital_latency_ns = digital_latency_ns
        self.neuro_latency_ns = neuro_latency_ns
        self.neuro_energy_j = neuro_energy_j
        self.neuro_partial_spikes = neuro_partial_spikes
        self.neuro_spike_model_j = neuro_spike_model_j

    @property
    def neuro_e_per_spike_j(self) -> float:
        if self.neuro_partial_spikes <= 0:
            raise ValueError("Neuro calibration has zero partial spikes.")
        return self.neuro_energy_j / float(self.neuro_partial_spikes)


def req_float(pattern: str, text: str, label: str) -> float:
    m = re.search(pattern, text)
    if not m:
        raise SystemExit(f"Missing {label}.")
    return float(m.group(1))


def req_int(pattern: str, text: str, label: str) -> int:
    m = re.search(pattern, text)
    if not m:
        raise SystemExit(f"Missing {label}.")
    return int(m.group(1))


def parse_calibration(digital_report: Path, neuro_report: Path) -> Calibration:
    dig = digital_report.read_text(encoding="utf-8")
    neu = neuro_report.read_text(encoding="utf-8")

    return Calibration(
        digital_eop_j=req_float(
            r"Energy per operation \(12 ops\):\s*([0-9.+-eE]+)\s*J/op",
            dig,
            "digital energy/op",
        ),
        digital_latency_ns=req_float(
            r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns",
            dig,
            "digital latency",
        ),
        neuro_latency_ns=req_float(
            r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns",
            neu,
            "neuro latency",
        ),
        neuro_energy_j=req_float(
            r"Total energy \(0-90ns\):\s*([0-9.+-eE]+)\s*J",
            neu,
            "neuro total energy",
        ),
        neuro_partial_spikes=req_int(
            r"Total partial spikes:\s*([0-9]+)",
            neu,
            "neuro partial spikes",
        ),
        neuro_spike_model_j=req_float(
            r"Spike-model energy estimate \(3\.27 pJ/spike\):\s*([0-9.+-eE]+)\s*J",
            neu,
            "neuro spike-model estimate",
        ),
    )


def parse_int_list(raw: str) -> List[int]:
    out: List[int] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        out.append(int(tok))
    if not out:
        raise SystemExit("No matrix sizes provided.")
    return out


def parse_float_list(raw: str) -> List[float]:
    out: List[float] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        val = float(tok)
        if val < 0.0 or val > 1.0:
            raise SystemExit(f"Density must be in [0,1], got {val}.")
        out.append(val)
    if not out:
        raise SystemExit("No densities provided.")
    return out


def parse_seed_list(raw: str) -> List[int]:
    out: List[int] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        out.append(int(tok))
    if not out:
        raise SystemExit("No seeds provided.")
    return out


def build_matrix(n: int, density: float, rng: random.Random) -> List[List[int]]:
    return [
        [1 if rng.random() < density else 0 for _ in range(n)]
        for _ in range(n)
    ]


def matmul_binary_counts(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> List[List[int]]:
    n = len(a)
    y: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s += a[i][k] * b[k][j]
            y[i][j] = s
    return y


def svg_text(x: float, y: float, txt: str, size: int = 14, weight: str = "normal", fill: str = "#102033") -> str:
    esc = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc}</text>'
    )


def polyline(points: Iterable[Tuple[float, float]], color: str, width: float = 2.5) -> str:
    ptxt = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{ptxt}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def draw_energy_svg(
    out_path: Path,
    n_vals: List[int],
    densities: List[float],
    agg: Dict[Tuple[int, float], Dict[str, float]],
) -> None:
    w, h = 1280, 760
    left, top, pw, ph = 100, 90, 1080, 520
    bg = ['<rect x="0" y="0" width="100%" height="100%" fill="#f7fafc"/>']
    bg.append(svg_text(28, 46, "Binary Matmul Scaling: Energy Estimate vs Matrix Size", 30, "bold"))
    bg.append(
        f'<rect x="{left}" y="{top}" width="{pw}" height="{ph}" fill="#ffffff" stroke="#d1d9e6" stroke-width="2"/>'
    )

    ymax = 0.0
    for n in n_vals:
        for p in densities:
            row = agg[(n, p)]
            ymax = max(ymax, row["digital_energy_pj_mean"], row["neuro_energy_pj_mean"])
    ymax = max(ymax * 1.15, 1.0)

    xmin = min(n_vals)
    xmax = max(n_vals)
    xspan = max(xmax - xmin, 1)
    yspan = ymax

    for i in range(6):
        y = top + ph * i / 5.0
        val = ymax * (1.0 - i / 5.0)
        bg.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left + pw}" y2="{y:.2f}" stroke="#e6ecf2" stroke-width="1"/>')
        bg.append(svg_text(20, y + 4, f"{val:.1f}", 12, fill="#4a5d73"))
    bg.append(svg_text(20, top - 10, "pJ", 12, "bold", "#2c3e50"))

    for n in n_vals:
        x = left + (n - xmin) * pw / xspan
        bg.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + ph}" stroke="#eef2f7" stroke-width="1"/>')
        bg.append(svg_text(x - 10, top + ph + 24, str(n), 12, fill="#4a5d73"))
    bg.append(svg_text(left + pw + 14, top + ph + 24, "N", 12, "bold", "#2c3e50"))

    digital_points = []
    for n in n_vals:
        v = mean(agg[(n, p)]["digital_energy_pj_mean"] for p in densities)
        x = left + (n - xmin) * pw / xspan
        y = top + ph - (v / yspan) * ph
        digital_points.append((x, y))
    bg.append(polyline(digital_points, "#1f77b4", 3.0))

    colors = ["#d62728", "#2ca02c", "#ff7f0e", "#9467bd", "#17becf"]
    for idx, p in enumerate(densities):
        pts = []
        for n in n_vals:
            v = agg[(n, p)]["neuro_energy_pj_mean"]
            x = left + (n - xmin) * pw / xspan
            y = top + ph - (v / yspan) * ph
            pts.append((x, y))
        bg.append(polyline(pts, colors[idx % len(colors)], 2.2))

    lx, ly = left + 20, top + ph + 58
    bg.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+34}" y2="{ly}" stroke="#1f77b4" stroke-width="3"/>')
    bg.append(svg_text(lx + 44, ly + 5, "digital model", 15))
    for idx, p in enumerate(densities):
        yy = ly + 28 * (idx + 1)
        c = colors[idx % len(colors)]
        bg.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+34}" y2="{yy}" stroke="{c}" stroke-width="3"/>')
        bg.append(svg_text(lx + 44, yy + 5, f"neuro model (density={p:.2f})", 15))

    out_path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        + "\n".join(bg)
        + "\n</svg>\n",
        encoding="utf-8",
    )


def draw_pressure_svg(
    out_path: Path,
    n_vals: List[int],
    densities: List[float],
    agg: Dict[Tuple[int, float], Dict[str, float]],
) -> None:
    w, h = 1280, 760
    left, top, pw, ph = 100, 90, 1080, 520
    body = ['<rect x="0" y="0" width="100%" height="100%" fill="#f7fafc"/>']
    body.append(svg_text(28, 46, "Compounding Pressure vs Matrix Size", 30, "bold"))
    body.append(
        f'<rect x="{left}" y="{top}" width="{pw}" height="{ph}" fill="#ffffff" stroke="#d1d9e6" stroke-width="2"/>'
    )

    xmin = min(n_vals)
    xmax = max(n_vals)
    xspan = max(xmax - xmin, 1)
    ymax = float(max(n_vals))
    yspan = max(ymax, 1.0)

    for i in range(6):
        y = top + ph * i / 5.0
        val = ymax * (1.0 - i / 5.0)
        body.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left + pw}" y2="{y:.2f}" stroke="#e6ecf2" stroke-width="1"/>')
        body.append(svg_text(20, y + 4, f"{val:.1f}", 12, fill="#4a5d73"))

    for n in n_vals:
        x = left + (n - xmin) * pw / xspan
        body.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + ph}" stroke="#eef2f7" stroke-width="1"/>')
        body.append(svg_text(x - 10, top + ph + 24, str(n), 12, fill="#4a5d73"))
    body.append(svg_text(left + pw + 14, top + ph + 24, "N", 12, "bold", "#2c3e50"))

    dig_depth = []
    dig_bitwidth = []
    neuro_fanin = []
    for n in n_vals:
        x = left + (n - xmin) * pw / xspan
        depth = float(math.ceil(math.log2(n)))
        bitw = float(math.ceil(math.log2(n + 1)))
        fanin = float(n)
        dig_depth.append((x, top + ph - (depth / yspan) * ph))
        dig_bitwidth.append((x, top + ph - (bitw / yspan) * ph))
        neuro_fanin.append((x, top + ph - (fanin / yspan) * ph))

    body.append(polyline(dig_depth, "#1f77b4", 2.8))
    body.append(polyline(dig_bitwidth, "#17becf", 2.8))
    body.append(polyline(neuro_fanin, "#d62728", 3.0))

    colors = ["#2ca02c", "#ff7f0e", "#9467bd", "#8c564b", "#e377c2"]
    for idx, p in enumerate(densities):
        pts = []
        for n in n_vals:
            val = agg[(n, p)]["y_max_mean"]
            x = left + (n - xmin) * pw / xspan
            y = top + ph - (val / yspan) * ph
            pts.append((x, y))
        body.append(polyline(pts, colors[idx % len(colors)], 2.2))

    lx, ly = left + 20, top + ph + 58
    legend = [
        ("#1f77b4", "digital adder depth (stages)"),
        ("#17becf", "digital output bitwidth"),
        ("#d62728", "neuro membrane fan-in (inputs/output)"),
    ]
    for idx, (color, label) in enumerate(legend):
        yy = ly + idx * 26
        body.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+34}" y2="{yy}" stroke="{color}" stroke-width="3"/>')
        body.append(svg_text(lx + 44, yy + 5, label, 14))
    base = ly + len(legend) * 26 + 8
    for idx, p in enumerate(densities):
        yy = base + idx * 24
        c = colors[idx % len(colors)]
        body.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+34}" y2="{yy}" stroke="{c}" stroke-width="3"/>')
        body.append(svg_text(lx + 44, yy + 5, f"neuro output peak mean (density={p:.2f})", 14))

    out_path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        + "\n".join(body)
        + "\n</svg>\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Binary matmul scaling sweep model.")
    parser.add_argument("--digital-report", required=True, type=Path)
    parser.add_argument("--neuro-report", required=True, type=Path)
    parser.add_argument("--n-list", required=True, help="Comma-separated sizes, e.g. 2,4,8")
    parser.add_argument("--density-list", required=True, help="Comma-separated probabilities in [0,1]")
    parser.add_argument("--seed-list", required=True, help="Comma-separated random seeds")
    parser.add_argument("--out-csv", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--out-energy-svg", required=True, type=Path)
    parser.add_argument("--out-pressure-svg", required=True, type=Path)
    args = parser.parse_args()

    n_vals = sorted(set(parse_int_list(args.n_list)))
    densities = sorted(set(parse_float_list(args.density_list)))
    seeds = sorted(set(parse_seed_list(args.seed_list)))

    cal = parse_calibration(args.digital_report, args.neuro_report)

    rows: List[Dict[str, str]] = []
    agg_map: Dict[Tuple[int, float], List[Dict[str, float]]] = {}

    for n in n_vals:
        for density in densities:
            for seed in seeds:
                rng = random.Random((n * 10_000_019) ^ (seed * 1_000_003) ^ int(density * 1000))
                a = build_matrix(n, density, rng)
                b = build_matrix(n, density, rng)
                y = matmul_binary_counts(a, b)

                a_ones = sum(sum(r) for r in a)
                b_ones = sum(sum(r) for r in b)
                y_sum = sum(sum(r) for r in y)
                y_max = max(max(r) for r in y)
                y_mean = y_sum / float(n * n)

                total_products = n ** 3
                active_products = y_sum
                add_ops = n * n * max(n - 1, 0)
                total_ops = total_products + add_ops

                digital_depth = int(math.ceil(math.log2(n)))
                digital_bitwidth = int(math.ceil(math.log2(n + 1)))

                digital_energy_j = cal.digital_eop_j * total_ops
                digital_latency_ns = cal.digital_latency_ns * max(1, digital_depth)

                neuro_energy_j = cal.neuro_e_per_spike_j * active_products
                neuro_spike_model_j = (cal.neuro_spike_model_j / float(cal.neuro_partial_spikes)) * active_products
                neuro_fanin = n
                neuro_latency_floor_ns = cal.neuro_latency_ns

                row = {
                    "n": str(n),
                    "density": f"{density:.3f}",
                    "seed": str(seed),
                    "a_ones": str(a_ones),
                    "b_ones": str(b_ones),
                    "total_products": str(total_products),
                    "active_products": str(active_products),
                    "y_mean": f"{y_mean:.6f}",
                    "y_max": str(y_max),
                    "digital_total_ops": str(total_ops),
                    "digital_adder_depth": str(digital_depth),
                    "digital_output_bitwidth": str(digital_bitwidth),
                    "digital_energy_pj_est": f"{digital_energy_j * 1e12:.6f}",
                    "digital_latency_ns_est": f"{digital_latency_ns:.6f}",
                    "neuro_membrane_fanin": str(neuro_fanin),
                    "neuro_energy_pj_est_measured_cal": f"{neuro_energy_j * 1e12:.6f}",
                    "neuro_energy_pj_est_spike_model": f"{neuro_spike_model_j * 1e12:.6f}",
                    "neuro_latency_ns_floor_est": f"{neuro_latency_floor_ns:.6f}",
                }
                rows.append(row)

                agg_map.setdefault((n, density), []).append(
                    {
                        "digital_energy_pj": digital_energy_j * 1e12,
                        "neuro_energy_pj": neuro_energy_j * 1e12,
                        "active_products": float(active_products),
                        "y_max": float(y_max),
                        "y_mean": y_mean,
                    }
                )

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    agg: Dict[Tuple[int, float], Dict[str, float]] = {}
    for key, vals in agg_map.items():
        agg[key] = {
            "digital_energy_pj_mean": mean(v["digital_energy_pj"] for v in vals),
            "neuro_energy_pj_mean": mean(v["neuro_energy_pj"] for v in vals),
            "active_products_mean": mean(v["active_products"] for v in vals),
            "y_max_mean": mean(v["y_max"] for v in vals),
            "y_mean_mean": mean(v["y_mean"] for v in vals),
        }

    args.out_energy_svg.parent.mkdir(parents=True, exist_ok=True)
    args.out_pressure_svg.parent.mkdir(parents=True, exist_ok=True)
    draw_energy_svg(args.out_energy_svg, n_vals, densities, agg)
    draw_pressure_svg(args.out_pressure_svg, n_vals, densities, agg)

    lines: List[str] = []
    lines.append("# Binary Matmul Scaling Sweep (Model-Based)")
    lines.append("")
    lines.append("This sweep uses calibrated 2x2 transistor measurements and extrapolates")
    lines.append("larger NxN binary workloads algorithmically.")
    lines.append("")
    lines.append("Calibration sources:")
    lines.append(f"- Digital: `{args.digital_report}`")
    lines.append(f"- Neuro: `{args.neuro_report}`")
    lines.append("")
    lines.append("Calibration values:")
    lines.append(f"- Digital energy/op: `{cal.digital_eop_j * 1e12:.6f} pJ/op`")
    lines.append(f"- Digital 2x2 latency: `{cal.digital_latency_ns:.3f} ns`")
    lines.append(f"- Neuro 2x2 total energy: `{cal.neuro_energy_j * 1e12:.3f} pJ`")
    lines.append(f"- Neuro 2x2 partial spikes: `{cal.neuro_partial_spikes}`")
    lines.append(f"- Neuro measured-calibrated energy/spike: `{cal.neuro_e_per_spike_j * 1e12:.3f} pJ/spike`")
    lines.append(f"- Neuro spike-model energy/spike: `{(cal.neuro_spike_model_j / cal.neuro_partial_spikes) * 1e12:.3f} pJ/spike`")
    lines.append("")
    lines.append("Sweep setup:")
    lines.append(f"- N list: `{','.join(str(x) for x in n_vals)}`")
    lines.append(f"- density list: `{','.join(f'{x:.2f}' for x in densities)}`")
    lines.append(f"- seeds: `{','.join(str(x) for x in seeds)}`")
    lines.append("")
    lines.append("| N | density | mean active products | mean y_max | digital energy est (pJ) | neuro energy est (pJ) | energy ratio (neuro/digital) |")
    lines.append("|---|---------|----------------------|------------|---------------------------|-----------------------|------------------------------|")
    for n in n_vals:
        for p in densities:
            a = agg[(n, p)]
            ratio = a["neuro_energy_pj_mean"] / a["digital_energy_pj_mean"] if a["digital_energy_pj_mean"] > 0 else float("inf")
            lines.append(
                f"| {n} | {p:.2f} | {a['active_products_mean']:.2f} | {a['y_max_mean']:.2f} | "
                f"{a['digital_energy_pj_mean']:.3f} | {a['neuro_energy_pj_mean']:.3f} | {ratio:.2f}x |"
            )
    lines.append("")
    lines.append("Interpretation notes:")
    lines.append("- Digital model scales with operation count `N^2(2N-1)` and logic-depth proxy `ceil(log2 N)`.")
    lines.append("- Neuro model scales with event count (`active_products`) and membrane fan-in (`N`).")
    lines.append("- This is an extrapolation aid for architecture discussion; it is not a full transistor NxN run.")
    lines.append("")
    lines.append("Artifacts:")
    lines.append(f"- CSV: `{args.out_csv}`")
    lines.append(f"- Energy plot: `{args.out_energy_svg}`")
    lines.append(f"- Pressure plot: `{args.out_pressure_svg}`")

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
