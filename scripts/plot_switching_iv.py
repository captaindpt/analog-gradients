#!/usr/bin/env python3
"""Plot SET/RESET I-V curves for a memristor run with publication-ready styling."""

import argparse
import csv
import os
from pathlib import Path
import shutil
import sys
from typing import Dict, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    py312 = shutil.which("python3.12")
    if py312 and Path(sys.executable).name != "python3.12":
        os.execv(py312, [py312, __file__] + sys.argv[1:])
    raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot memristor SET/RESET curves on log(|I|) scale."
    )
    parser.add_argument(
        "--run-dir",
        required=True,
        help="Run directory containing set_current.csv/reset_current.csv/manifest.txt",
    )
    parser.add_argument(
        "--out-dir",
        default="tcad/memristor/results",
        help="Output directory for PNG/SVG files",
    )
    return parser.parse_args()


def read_manifest(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text().splitlines():
        if "=" not in raw:
            continue
        k, v = raw.split("=", 1)
        values[k.strip()] = v.strip()
    return values


def read_iv(path: Path) -> Tuple[np.ndarray, np.ndarray]:
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(newline="") as f:
        head = f.readline().strip().lower()

    if head.startswith("time_s"):
        voltage = []
        current = []
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                voltage.append(float(row["voltage_v"]))
                current.append(float(row["current_a"]))
        return np.array(voltage), np.array(current)

    arr = np.loadtxt(path, delimiter=",")
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    return arr[:, 1], arr[:, 2]


def safe_float(text: str, default: float = float("nan")) -> float:
    try:
        return float(text)
    except Exception:
        return default


def main() -> None:
    args = parse_args()
    run_dir = Path(args.run_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    set_csv = run_dir / "set_current.csv"
    reset_csv = run_dir / "reset_current.csv"
    manifest = read_manifest(run_dir / "manifest.txt")

    set_v, set_i = read_iv(set_csv)
    reset_v, reset_i = read_iv(reset_csv)

    set_peak = float(np.max(np.abs(set_i)))
    reset_abs = np.abs(reset_i)
    reset_peak = float(np.max(reset_abs)) if reset_abs.size > 0 else float("nan")
    reset_min = float(np.min(reset_abs[reset_abs > 0])) if np.any(reset_abs > 0) else float("nan")

    ratio_peak_over_peak = float("nan")
    if np.isfinite(set_peak) and np.isfinite(reset_peak) and reset_peak > 0:
        ratio_peak_over_peak = set_peak / reset_peak
    elif "current_ratio_set_over_reset" in manifest:
        ratio_peak_over_peak = safe_float(manifest.get("current_ratio_set_over_reset", "nan"))

    # Primary switching ratio: compare SET peak against minimum RESET current
    # in a high-bias region to avoid near-zero-voltage trivial minima.
    ratio_on_off = float("nan")
    if reset_abs.size > 0 and np.any(np.abs(reset_v) > 0):
        vthr = 0.5 * float(np.max(np.abs(reset_v)))
        mask = np.abs(reset_v) >= vthr
        if np.any(mask):
            reset_window = reset_abs[mask]
            reset_window_min = float(np.min(reset_window[reset_window > 0])) if np.any(reset_window > 0) else float("nan")
            if np.isfinite(set_peak) and np.isfinite(reset_window_min) and reset_window_min > 0:
                ratio_on_off = set_peak / reset_window_min

    bg = "#05070d"
    panel = "#0b1220"
    fg = "#e8eef8"
    grid = "#3b4d67"
    set_color = "#5dd6ff"
    reset_color = "#ff8f6e"

    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(panel)

    eps = 1e-30
    ax.plot(set_v, np.clip(np.abs(set_i), eps, None), lw=2.0, color=set_color, label="SET")
    ax.plot(reset_v, np.clip(np.abs(reset_i), eps, None), lw=2.0, color=reset_color, label="RESET")
    ax.set_yscale("log")

    ax.set_title("ReRAM Memristor IV Characteristic — KMC Physical Simulation", color=fg, fontsize=14, pad=14)
    subtitle = (
        f"Run: {run_dir.name} | oxide={manifest.get('oxide_thickness_nm', 'NA')}nm | "
        f"lateral={manifest.get('lateral_nm', 'NA')}nm | compliance={manifest.get('compliance_a', 'NA')}A"
    )
    ax.text(0.5, 1.01, subtitle, transform=ax.transAxes, color=fg, fontsize=10, ha="center", va="bottom")

    ratio_text = "ON/OFF ratio (set_max/reset_min@|V|>=0.5Vmax): NA"
    if np.isfinite(ratio_on_off):
        ratio_text = f"ON/OFF ratio (set_max/reset_min@|V|>=0.5Vmax): {ratio_on_off:.3e}"
    ax.text(
        0.02,
        0.02,
        ratio_text,
        transform=ax.transAxes,
        color=fg,
        fontsize=10,
        bbox=dict(facecolor="#101a2d", edgecolor=grid, alpha=0.85),
    )

    ax.set_xlabel("Voltage (V)", color=fg, fontsize=12)
    ax.set_ylabel("|Current| (A)", color=fg, fontsize=12)
    ax.grid(True, which="both", color=grid, alpha=0.35, lw=0.8)
    ax.tick_params(colors=fg)
    for spine in ax.spines.values():
        spine.set_color(grid)

    legend = ax.legend(facecolor=panel, edgecolor=grid)
    for text in legend.get_texts():
        text.set_color(fg)

    png_out = out_dir / f"switching_iv_{run_dir.name}.png"
    svg_out = out_dir / f"switching_iv_{run_dir.name}.svg"
    fig.tight_layout()
    fig.savefig(png_out, dpi=300, facecolor=bg)
    fig.savefig(svg_out, facecolor=bg)

    print(f"Saved PNG: {png_out}")
    print(f"Saved SVG: {svg_out}")
    print(f"set_peak_a={set_peak:.6e}")
    if np.isfinite(reset_min):
        print(f"reset_min_abs_a={reset_min:.6e}")
    else:
        print("reset_min_abs_a=NA")
    if np.isfinite(ratio_peak_over_peak):
        print(f"ratio_set_over_reset_peak={ratio_peak_over_peak:.6e}")
    else:
        print("ratio_set_over_reset_peak=NA")
    if np.isfinite(ratio_on_off):
        print(f"ratio_set_over_reset_min_window={ratio_on_off:.6e}")
    else:
        print("ratio_set_over_reset_min_window=NA")


if __name__ == "__main__":
    main()
