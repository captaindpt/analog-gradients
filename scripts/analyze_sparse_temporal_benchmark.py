#!/usr/bin/env python3
"""Analyze sparse temporal event benchmark with measured transistor calibrations."""

import argparse
import csv
import math
import re
from pathlib import Path
from statistics import mean
from typing import Dict, List, Match, Optional, Sequence


def parse_float_list(raw: str) -> List[float]:
    vals: List[float] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        v = float(tok)
        if v <= 0.0 or v >= 1.0:
            raise SystemExit(f"Active fractions must be in (0,1), got {v}.")
        vals.append(v)
    if not vals:
        raise SystemExit("No active fractions provided.")
    return sorted(set(vals))


def req_match(pattern: str, text: str, label: str) -> Match[str]:
    m = re.search(pattern, text)
    if not m:
        raise SystemExit(f"Missing {label} in report.")
    return m


def parse_coincidence_report(path: Path) -> Dict[str, float]:
    txt = path.read_text(encoding="utf-8")

    counts = req_match(
        r"Spike counts:\s*"
        r"\n\s*A-only:\s*([0-9]+)\s*"
        r"\n\s*B-only:\s*([0-9]+)\s*"
        r"\n\s*Coincident:\s*([0-9]+)\s*"
        r"\n\s*Offset:\s*([0-9]+)",
        txt,
        "spike-count block",
    )

    a_cnt = int(counts.group(1))
    b_cnt = int(counts.group(2))
    c_cnt = int(counts.group(3))
    o_cnt = int(counts.group(4))

    lat_match = re.search(r"First coincident spike:\s*([0-9.+-eE]+)\s*ns", txt)
    latency_ns = float(lat_match.group(1)) if lat_match else float("nan")

    positives = 1.0
    negatives = 3.0
    tp = 1.0 if c_cnt >= 1 else 0.0
    fp_cases = float(int(a_cnt > 0) + int(b_cnt > 0) + int(o_cnt > 0))

    return {
        "neuro_tpr": tp / positives,
        "neuro_fpr": fp_cases / negatives,
        "neuro_latency_ns": latency_ns,
        "a_only_spikes": float(a_cnt),
        "b_only_spikes": float(b_cnt),
        "coincident_spikes": float(c_cnt),
        "offset_spikes": float(o_cnt),
    }


def parse_crossover_csv(path: Path) -> Dict[str, float]:
    rows = list(csv.DictReader(path.open("r", encoding="utf-8")))
    if not rows:
        raise SystemExit(f"No rows in {path}")

    active = [r for r in rows if float(r["active_products"]) > 0.0 and r["digital_pass"] == "PASS" and r["neuro_pass"] == "PASS"]
    idle = [r for r in rows if float(r["active_products"]) == 0.0 and r["digital_pass"] == "PASS" and r["neuro_pass"] == "PASS"]

    if not active:
        raise SystemExit("No active rows found in crossover CSV.")
    if not idle:
        raise SystemExit("No idle rows found in crossover CSV.")

    return {
        "digital_active_pj": mean(float(r["digital_energy_pj"]) for r in active),
        "digital_idle_pj": mean(float(r["digital_energy_pj"]) for r in idle),
        "neuro_active_pj": mean(float(r["neuro_energy_pj"]) for r in active),
        "neuro_idle_pj": mean(float(r["neuro_energy_pj"]) for r in idle),
        "digital_active_latency_ns": mean(float(r["digital_latency_ns"]) for r in active),
        "neuro_active_latency_ns": mean(float(r["neuro_latency_ns"]) for r in active),
    }


def safe_div(numer: float, denom: float) -> float:
    if denom == 0.0:
        return float("inf")
    return numer / denom


def fmt(v: float, digits: int = 6) -> str:
    if math.isnan(v):
        return "nan"
    if math.isinf(v):
        return "inf"
    return f"{v:.{digits}f}"


def find_crossing(alphas: Sequence[float], ratios: Sequence[float]) -> Optional[float]:
    for i in range(len(alphas) - 1):
        a1, a2 = alphas[i], alphas[i + 1]
        r1, r2 = ratios[i], ratios[i + 1]
        if math.isnan(r1) or math.isnan(r2):
            continue
        if (r1 - 1.0) * (r2 - 1.0) <= 0.0 and r1 != r2:
            return a1 + (1.0 - r1) * (a2 - a1) / (r2 - r1)
    return None


def svg_text(x: float, y: float, txt: str, size: int = 14, weight: str = "normal", fill: str = "#102033") -> str:
    esc = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc}</text>'
    )


def draw_ratio_svg(out_path: Path, rows: List[Dict[str, float]], crossover_alpha: Optional[float]) -> None:
    w, h = 1240, 720
    left, top, pw, ph = 110, 90, 1020, 500

    min_a = min(r["active_fraction"] for r in rows)
    max_a = max(r["active_fraction"] for r in rows)
    log_min = math.log10(min_a)
    log_max = math.log10(max_a)

    max_ratio = max(r["ratio_neuro_over_digital"] for r in rows)
    y_max = max(2.0, max_ratio * 1.1)

    def x_of(alpha: float) -> float:
        return left + (math.log10(alpha) - log_min) * pw / (log_max - log_min)

    def y_of(val: float) -> float:
        return top + ph - (val / y_max) * ph

    body = ['<rect x="0" y="0" width="100%" height="100%" fill="#f7fafc"/>']
    body.append(svg_text(24, 44, "Sparse Temporal Benchmark: Neuro/Digital Energy Ratio", 30, "bold"))
    body.append(f'<rect x="{left}" y="{top}" width="{pw}" height="{ph}" fill="#ffffff" stroke="#d1d9e6" stroke-width="2"/>')

    for i in range(6):
        yv = y_max * i / 5.0
        y = y_of(yv)
        body.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left + pw}" y2="{y:.2f}" stroke="#e6ecf2" stroke-width="1"/>')
        body.append(svg_text(26, y + 4, f"{yv:.1f}", 12, fill="#4a5d73"))

    for a in sorted(set(r["active_fraction"] for r in rows)):
        x = x_of(a)
        body.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + ph}" stroke="#eef2f7" stroke-width="1"/>')
        body.append(svg_text(x - 18, top + ph + 24, f"{a*100:.3f}%", 12, fill="#4a5d73"))

    one_y = y_of(1.0)
    body.append(f'<line x1="{left}" y1="{one_y:.2f}" x2="{left + pw}" y2="{one_y:.2f}" stroke="#111827" stroke-width="2" stroke-dasharray="8,6"/>')
    body.append(svg_text(left + pw - 120, one_y - 10, "ratio=1", 12, "bold", "#111827"))

    pts = " ".join(f"{x_of(r['active_fraction']):.2f},{y_of(r['ratio_neuro_over_digital']):.2f}" for r in rows)
    body.append(f'<polyline points="{pts}" fill="none" stroke="#d62728" stroke-width="3"/>')

    if crossover_alpha is not None:
        cx = x_of(crossover_alpha)
        body.append(f'<line x1="{cx:.2f}" y1="{top}" x2="{cx:.2f}" y2="{top + ph}" stroke="#0f766e" stroke-width="2" stroke-dasharray="5,5"/>')
        body.append(svg_text(cx + 8, top + 20, f"crossover ~ {crossover_alpha*100:.4f}%", 12, "bold", "#0f766e"))

    body.append(svg_text(24, top + ph + 18, "Neuro/Digital", 12, "bold", "#2c3e50"))
    body.append(svg_text(left + pw + 10, top + ph + 24, "active fraction", 12, "bold", "#2c3e50"))

    out_path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        + "\n".join(body)
        + "\n</svg>\n",
        encoding="utf-8",
    )


def draw_eptp_svg(out_path: Path, rows: List[Dict[str, float]]) -> None:
    w, h = 1240, 720
    left, top, pw, ph = 110, 90, 1020, 500

    min_a = min(r["active_fraction"] for r in rows)
    max_a = max(r["active_fraction"] for r in rows)
    log_min_x = math.log10(min_a)
    log_max_x = math.log10(max_a)

    y_vals = [
        r["digital_energy_per_tp_pj"] for r in rows if r["digital_energy_per_tp_pj"] > 0.0
    ] + [
        r["neuro_energy_per_tp_pj"] for r in rows if r["neuro_energy_per_tp_pj"] > 0.0
    ]
    log_min_y = math.log10(min(y_vals))
    log_max_y = math.log10(max(y_vals))

    def x_of(alpha: float) -> float:
        return left + (math.log10(alpha) - log_min_x) * pw / (log_max_x - log_min_x)

    def y_of(val: float) -> float:
        return top + ph - (math.log10(val) - log_min_y) * ph / (log_max_y - log_min_y)

    body = ['<rect x="0" y="0" width="100%" height="100%" fill="#f7fafc"/>']
    body.append(svg_text(24, 44, "Sparse Temporal Benchmark: Energy per Correct Event", 30, "bold"))
    body.append(f'<rect x="{left}" y="{top}" width="{pw}" height="{ph}" fill="#ffffff" stroke="#d1d9e6" stroke-width="2"/>')

    for i in range(6):
        lv = log_min_y + (log_max_y - log_min_y) * i / 5.0
        val = 10 ** lv
        y = y_of(val)
        body.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left + pw}" y2="{y:.2f}" stroke="#e6ecf2" stroke-width="1"/>')
        body.append(svg_text(16, y + 4, f"{val:.3f}", 12, fill="#4a5d73"))

    for a in sorted(set(r["active_fraction"] for r in rows)):
        x = x_of(a)
        body.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + ph}" stroke="#eef2f7" stroke-width="1"/>')
        body.append(svg_text(x - 18, top + ph + 24, f"{a*100:.3f}%", 12, fill="#4a5d73"))

    d_pts = " ".join(
        f"{x_of(r['active_fraction']):.2f},{y_of(r['digital_energy_per_tp_pj']):.2f}" for r in rows
    )
    n_pts = " ".join(
        f"{x_of(r['active_fraction']):.2f},{y_of(r['neuro_energy_per_tp_pj']):.2f}" for r in rows
    )
    body.append(f'<polyline points="{d_pts}" fill="none" stroke="#1f77b4" stroke-width="3"/>')
    body.append(f'<polyline points="{n_pts}" fill="none" stroke="#d62728" stroke-width="3"/>')

    lx, ly = left + 20, top + ph + 56
    body.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+32}" y2="{ly}" stroke="#1f77b4" stroke-width="3"/>')
    body.append(svg_text(lx + 42, ly + 5, "digital", 14))
    body.append(f'<line x1="{lx}" y1="{ly+28}" x2="{lx+32}" y2="{ly+28}" stroke="#d62728" stroke-width="3"/>')
    body.append(svg_text(lx + 42, ly + 33, "neuro", 14))

    body.append(svg_text(8, top + ph + 18, "pJ per true positive (log scale)", 12, "bold", "#2c3e50"))
    body.append(svg_text(left + pw + 10, top + ph + 24, "active fraction", 12, "bold", "#2c3e50"))

    out_path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        + "\n".join(body)
        + "\n</svg>\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Sparse temporal benchmark analyzer.")
    parser.add_argument("--crossover-csv", required=True, type=Path)
    parser.add_argument("--coincidence-report", required=True, type=Path)
    parser.add_argument("--active-fractions", required=True)
    parser.add_argument("--windows", type=int, default=1_000_000)
    parser.add_argument("--digital-tpr", type=float, default=1.0)
    parser.add_argument("--digital-fpr", type=float, default=0.0)
    parser.add_argument("--digital-latency-ns", type=float, default=None)
    parser.add_argument("--max-latency-ns", type=float, default=15.0)
    parser.add_argument("--max-fpr", type=float, default=0.01)
    parser.add_argument("--min-tpr", type=float, default=0.99)
    parser.add_argument("--out-csv", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--out-ratio-svg", required=True, type=Path)
    parser.add_argument("--out-eptp-svg", required=True, type=Path)
    args = parser.parse_args()

    alphas = parse_float_list(args.active_fractions)
    cal = parse_crossover_csv(args.crossover_csv)
    coin = parse_coincidence_report(args.coincidence_report)

    digital_latency_ns = (
        args.digital_latency_ns
        if args.digital_latency_ns is not None
        else cal["digital_active_latency_ns"]
    )

    rows: List[Dict[str, float]] = []
    for alpha in alphas:
        windows = float(args.windows)
        event_windows = windows * alpha
        idle_windows = windows - event_windows

        digital_energy_pj = (
            event_windows * cal["digital_active_pj"]
            + idle_windows * cal["digital_idle_pj"]
        )
        neuro_energy_pj = (
            event_windows * cal["neuro_active_pj"]
            + idle_windows * cal["neuro_idle_pj"]
        )

        digital_tp = event_windows * args.digital_tpr
        neuro_tp = event_windows * coin["neuro_tpr"]
        digital_fp = idle_windows * args.digital_fpr
        neuro_fp = idle_windows * coin["neuro_fpr"]

        digital_precision = safe_div(digital_tp, digital_tp + digital_fp)
        neuro_precision = safe_div(neuro_tp, neuro_tp + neuro_fp)

        row = {
            "active_fraction": alpha,
            "windows": windows,
            "event_windows": event_windows,
            "idle_windows": idle_windows,
            "digital_energy_pj": digital_energy_pj,
            "neuro_energy_pj": neuro_energy_pj,
            "ratio_neuro_over_digital": safe_div(neuro_energy_pj, digital_energy_pj),
            "digital_tp": digital_tp,
            "neuro_tp": neuro_tp,
            "digital_fp": digital_fp,
            "neuro_fp": neuro_fp,
            "digital_recall": args.digital_tpr,
            "neuro_recall": coin["neuro_tpr"],
            "digital_fpr": args.digital_fpr,
            "neuro_fpr": coin["neuro_fpr"],
            "digital_precision": digital_precision,
            "neuro_precision": neuro_precision,
            "digital_latency_ns": digital_latency_ns,
            "neuro_latency_ns": coin["neuro_latency_ns"],
            "digital_energy_per_tp_pj": safe_div(digital_energy_pj, digital_tp),
            "neuro_energy_per_tp_pj": safe_div(neuro_energy_pj, neuro_tp),
            "digital_pass_quality": 1.0
            if args.digital_tpr >= args.min_tpr
            and args.digital_fpr <= args.max_fpr
            and digital_latency_ns <= args.max_latency_ns
            else 0.0,
            "neuro_pass_quality": 1.0
            if coin["neuro_tpr"] >= args.min_tpr
            and coin["neuro_fpr"] <= args.max_fpr
            and coin["neuro_latency_ns"] <= args.max_latency_ns
            else 0.0,
        }
        rows.append(row)

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "active_fraction",
            "windows",
            "event_windows",
            "idle_windows",
            "digital_energy_pj",
            "neuro_energy_pj",
            "ratio_neuro_over_digital",
            "digital_tp",
            "neuro_tp",
            "digital_fp",
            "neuro_fp",
            "digital_recall",
            "neuro_recall",
            "digital_fpr",
            "neuro_fpr",
            "digital_precision",
            "neuro_precision",
            "digital_latency_ns",
            "neuro_latency_ns",
            "digital_energy_per_tp_pj",
            "neuro_energy_per_tp_pj",
            "digital_pass_quality",
            "neuro_pass_quality",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: fmt(v, 9) for k, v in r.items()})

    ratio_cross = find_crossing(
        [r["active_fraction"] for r in rows],
        [r["ratio_neuro_over_digital"] for r in rows],
    )

    args.out_ratio_svg.parent.mkdir(parents=True, exist_ok=True)
    args.out_eptp_svg.parent.mkdir(parents=True, exist_ok=True)
    draw_ratio_svg(args.out_ratio_svg, rows, ratio_cross)
    draw_eptp_svg(args.out_eptp_svg, rows)

    md: List[str] = []
    md.append("# Sparse Temporal Event Benchmark (Trace-Driven, Calibrated)")
    md.append("")
    md.append("Goal: compare digital vs neuro on **energy per correct event** under fixed quality gates.")
    md.append("")
    md.append("Calibration sources:")
    md.append(f"- Energy windows (active/idle): `{args.crossover_csv}`")
    md.append(f"- Neuro temporal detection quality: `{args.coincidence_report}`")
    md.append("")
    md.append("Window-energy calibration (measured):")
    md.append("")
    md.append("| Regime | Digital (pJ/window) | Neuro (pJ/window) | Neuro/Digital |")
    md.append("|--------|----------------------|-------------------|---------------|")
    md.append(
        f"| Active | {cal['digital_active_pj']:.6f} | {cal['neuro_active_pj']:.6f} | {safe_div(cal['neuro_active_pj'], cal['digital_active_pj']):.3f}x |"
    )
    md.append(
        f"| Idle | {cal['digital_idle_pj']:.6f} | {cal['neuro_idle_pj']:.6f} | {safe_div(cal['neuro_idle_pj'], cal['digital_idle_pj']):.3f}x |"
    )
    md.append("")
    md.append("Quality-gate setup:")
    md.append(f"- min recall: `{args.min_tpr:.3f}`")
    md.append(f"- max false-positive rate: `{args.max_fpr:.4f}`")
    md.append(f"- max latency: `{args.max_latency_ns:.3f} ns`")
    md.append(f"- digital quality model: recall=`{args.digital_tpr:.3f}`, FPR=`{args.digital_fpr:.4f}`, latency=`{digital_latency_ns:.3f} ns`")
    md.append(
        f"- neuro quality from coincidence test: recall=`{coin['neuro_tpr']:.3f}`, FPR=`{coin['neuro_fpr']:.4f}`, latency=`{coin['neuro_latency_ns']:.3f} ns`"
    )
    md.append("")
    md.append("| Active fraction | Digital energy (pJ) | Neuro energy (pJ) | Ratio (N/D) | Digital pJ/TP | Neuro pJ/TP | Quality pass (D/N) |")
    md.append("|-----------------|---------------------|-------------------|-------------|---------------|-------------|--------------------|")
    for r in rows:
        md.append(
            f"| {r['active_fraction']*100:.4f}% | {r['digital_energy_pj']:.3f} | {r['neuro_energy_pj']:.3f} | "
            f"{r['ratio_neuro_over_digital']:.3f}x | {r['digital_energy_per_tp_pj']:.3f} | {r['neuro_energy_per_tp_pj']:.3f} | "
            f"{int(r['digital_pass_quality'])}/{int(r['neuro_pass_quality'])} |"
        )

    md.append("")
    if ratio_cross is None:
        md.append("Crossover result:")
        md.append("- No ratio crossing found in sampled active-fraction range.")
    else:
        md.append("Crossover result:")
        md.append(
            f"- Estimated `ratio=1` active-fraction crossover: `{ratio_cross:.8f}` "
            f"(`{ratio_cross*100:.4f}%` active windows, `{(1.0-ratio_cross)*100:.4f}%` idle windows)."
        )

    md.append("")
    md.append("Interpretation:")
    md.append("- Neuro wins only when traces are extremely idle; digital wins once active windows are frequent.")
    md.append("- This benchmark is trace-driven and calibrated from measured transistor data, not a direct transistor detector-vs-detector netlist pair.")
    md.append("")
    md.append("Artifacts:")
    md.append(f"- CSV: `{args.out_csv}`")
    md.append(f"- Ratio plot: `{args.out_ratio_svg}`")
    md.append(f"- Energy/TP plot: `{args.out_eptp_svg}`")

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
