#!/usr/bin/env python3
"""
Analyze memristor waveform CSV and extract first-pass physics metrics.

Required columns (auto-detected):
- time_s (or time)
- voltage_v (or voltage, v)
- current_a (or current, i)
"""

import argparse
import csv
import json
from typing import Dict, List, Tuple


def _pick_column(fieldnames: List[str], candidates: List[str]) -> str:
    lowered = {name.lower(): name for name in fieldnames}
    for cand in candidates:
        if cand.lower() in lowered:
            return lowered[cand.lower()]
    raise ValueError("Missing required column. Tried: {}".format(", ".join(candidates)))


def _read_waveform(csv_path: str) -> Tuple[List[float], List[float], List[float]]:
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row: {}".format(csv_path))

        t_col = _pick_column(reader.fieldnames, ["time_s", "time", "t"])
        v_col = _pick_column(reader.fieldnames, ["voltage_v", "voltage", "v"])
        i_col = _pick_column(reader.fieldnames, ["current_a", "current", "i"])

        t_vals = []
        v_vals = []
        i_vals = []
        for row in reader:
            t_vals.append(float(row[t_col]))
            v_vals.append(float(row[v_col]))
            i_vals.append(float(row[i_col]))

    if len(t_vals) < 3:
        raise ValueError("Need at least 3 samples, got {}".format(len(t_vals)))
    return t_vals, v_vals, i_vals


def _estimate_thresholds(v: List[float], i: List[float], v_floor: float) -> Dict[str, float]:
    set_v = None
    set_slope = -1e99
    reset_v = None
    reset_slope = 1e99

    for k in range(len(v) - 1):
        dv = v[k + 1] - v[k]
        if abs(dv) < 1e-12:
            continue
        di = i[k + 1] - i[k]
        slope = di / dv
        vmid = 0.5 * (v[k + 1] + v[k])

        if vmid >= v_floor and slope > set_slope:
            set_slope = slope
            set_v = vmid
        if vmid <= -v_floor and slope < reset_slope:
            reset_slope = slope
            reset_v = vmid

    return {
        "set_threshold_v": set_v,
        "set_didv_peak": set_slope if set_v is not None else None,
        "reset_threshold_v": reset_v,
        "reset_didv_peak": reset_slope if reset_v is not None else None,
    }


def _integrate_energy(t: List[float], v: List[float], i: List[float]) -> float:
    e = 0.0
    for k in range(len(t) - 1):
        dt = t[k + 1] - t[k]
        p0 = v[k] * i[k]
        p1 = v[k + 1] * i[k + 1]
        e += 0.5 * (p0 + p1) * dt
    return e


def _integrate_hysteresis(v: List[float], i: List[float]) -> float:
    area = 0.0
    for k in range(len(v) - 1):
        dv = v[k + 1] - v[k]
        imid = 0.5 * (i[k + 1] + i[k])
        area += imid * dv
    return area


def _read_resistance_window(v: List[float], i: List[float], read_v: float, tol_v: float) -> Dict[str, float]:
    vals = []
    for vk, ik in zip(v, i):
        if abs(vk - read_v) <= tol_v and abs(ik) > 1e-15:
            vals.append(abs(vk / ik))
    if not vals:
        return {"read_res_min_ohm": None, "read_res_max_ohm": None}
    return {"read_res_min_ohm": min(vals), "read_res_max_ohm": max(vals)}


def _write_md(path: str, metrics: Dict[str, float], csv_path: str) -> None:
    lines = []
    lines.append("# Memristor Waveform Metrics")
    lines.append("")
    lines.append("- Source CSV: `{}`".format(csv_path))
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    for key in sorted(metrics.keys()):
        lines.append("| {} | {} |".format(key, metrics[key]))
    lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract first-pass memristor metrics from waveform CSV.")
    ap.add_argument("--csv", required=True, help="Input waveform CSV.")
    ap.add_argument("--out-json", required=True, help="Output JSON path.")
    ap.add_argument("--out-md", default="", help="Optional Markdown summary path.")
    ap.add_argument("--v-floor", type=float, default=0.2, help="Absolute voltage floor for threshold extraction.")
    ap.add_argument("--read-v", type=float, default=0.2, help="Read voltage for resistance window metrics.")
    ap.add_argument("--read-tol", type=float, default=0.02, help="Voltage tolerance around read voltage.")
    args = ap.parse_args()

    t, v, i = _read_waveform(args.csv)
    metrics = {}
    metrics["samples"] = len(t)
    metrics["time_start_s"] = t[0]
    metrics["time_stop_s"] = t[-1]
    metrics.update(_estimate_thresholds(v, i, args.v_floor))
    metrics["energy_total_j"] = _integrate_energy(t, v, i)
    metrics["hysteresis_area_av"] = _integrate_hysteresis(v, i)
    metrics.update(_read_resistance_window(v, i, args.read_v, args.read_tol))
    metrics["current_abs_max_a"] = max(abs(x) for x in i)
    metrics["voltage_abs_max_v"] = max(abs(x) for x in v)

    with open(args.out_json, "w") as f:
        json.dump(metrics, f, indent=2, sort_keys=True)

    if args.out_md:
        _write_md(args.out_md, metrics, args.csv)

    print("Wrote metrics JSON:", args.out_json)
    if args.out_md:
        print("Wrote metrics Markdown:", args.out_md)


if __name__ == "__main__":
    main()
