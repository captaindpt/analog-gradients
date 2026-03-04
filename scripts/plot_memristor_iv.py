#!/usr/bin/env python3.12
"""Plot SET/RESET I-V curves for the row-32 memristor run."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


RUN_DIR = Path(
    "tcad/memristor/runs/20260212_000817_reram_row32_combined_aggressive"
)
SET_CSV = RUN_DIR / "set_current.csv"
RESET_CSV = RUN_DIR / "reset_current.csv"
OUT_PNG = Path("tcad/memristor/runs/memristor_iv_row32.png")


def read_iv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Return (voltage, current) from a 3-column CSV."""
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(newline="") as f:
        first = f.readline().strip()

    # Handle both header and no-header CSV formats.
    if first.lower().startswith("time_s"):
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            v = []
            i = []
            for row in reader:
                v.append(float(row["voltage_v"]))
                i.append(float(row["current_a"]))
        return np.array(v), np.array(i)

    data = np.loadtxt(path, delimiter=",")
    if data.ndim == 1:
        data = data.reshape(1, -1)
    return data[:, 1], data[:, 2]


def main() -> None:
    set_v, set_i = read_iv(SET_CSV)

    reset_v = None
    reset_i = None
    if RESET_CSV.exists():
        reset_v, reset_i = read_iv(RESET_CSV)

    bg = "#0d1117"
    fg = "#c9d1d9"
    grid = "#30363d"

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    ax.plot(set_v, set_i, lw=1.8, color="#58a6ff", label="SET")
    if reset_v is not None and reset_i is not None:
        ax.plot(reset_v, reset_i, lw=1.8, color="#f78166", label="RESET")

    ax.set_title(
        "HfO₂ ReRAM I-V Characteristic — Row 32 (3nm, aggressive KMC)",
        color=fg,
        fontsize=13,
    )
    ax.set_xlabel("Voltage (V)", color=fg)
    ax.set_ylabel("Current (A)", color=fg)
    ax.grid(True, color=grid, alpha=0.6, lw=0.8)
    ax.tick_params(colors=fg)
    for spine in ax.spines.values():
        spine.set_color(grid)

    leg = ax.legend(facecolor=bg, edgecolor=grid)
    for txt in leg.get_texts():
        txt.set_color(fg)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_PNG, facecolor=bg)
    print(f"Saved: {OUT_PNG}")


if __name__ == "__main__":
    main()
