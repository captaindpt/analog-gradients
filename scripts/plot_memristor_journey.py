#!/usr/bin/env python3.12
"""Generate a social-media-ready visualization of the memristor KMC ReRAM exploration journey."""

import csv
import glob
import os
import re
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# ===== COLOR PALETTE =====
BG = "#0d1117"
PANEL_BG = "#161b22"
GRID = "#21262d"
BORDER = "#30363d"
TEXT = "#c9d1d9"
TEXT_DIM = "#8b949e"
TEXT_BRIGHT = "#f0f6fc"
BLUE = "#58a6ff"
ORANGE = "#f0883e"
GREEN = "#3fb950"
RED = "#f85149"
PURPLE = "#bc8cff"

PHASE_COLORS = {
    "B": BLUE,
    "C": BLUE,
    "D": ORANGE,
    "E": GREEN,
    "F": PURPLE,
    "Z": PURPLE,
}

RESULTS_CSV = "tcad/memristor/runs/reram_results.csv"
RUNS_ROOT = "tcad/memristor/runs"
OUT_PNG = "tcad/memristor/runs/memristor_journey.png"


def parse_int(value):
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.upper() == "NA":
        return None
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None


def parse_float(value):
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.upper() == "NA":
        return None
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def read_manifest(path):
    out = {}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def parse_kmc_counts_from_log(log_path):
    gen_max = None
    diff_max = None
    if not os.path.exists(log_path):
        return gen_max, diff_max
    gen_re = re.compile(r"FrenkelPair1 Bulk Generation count\s+([0-9]+)")
    diff_re = re.compile(r"Vacancy diffusion count\s+([0-9]+)")
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            gm = gen_re.search(line)
            if gm:
                val = int(gm.group(1))
                gen_max = val if gen_max is None else max(gen_max, val)
            dm = diff_re.search(line)
            if dm:
                val = int(dm.group(1))
                diff_max = val if diff_max is None else max(diff_max, val)
    return gen_max, diff_max


def load_csv_rows(path):
    rows = {}
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            r = parse_int(row.get("sweep_row"))
            if r is None:
                continue
            rows[r] = {
                "row": r,
                "phase": (row.get("phase") or "").strip(),
                "group": (row.get("sweep_group") or "").strip(),
                "gen": parse_int(row.get("kmc_generation_count_max")) or 0,
                "diff": parse_int(row.get("kmc_vacancy_diffusion_count_max")) or 0,
                "set_i": parse_float(row.get("set_current_abs_max_a")),
                "outcome": (row.get("outcome") or "").strip(),
                "notes": (row.get("notes") or "").strip(),
                "run_id": (row.get("run_id") or "").strip(),
                "source": "csv",
            }
    return rows


def load_latest_manifest_rows(root):
    by_row = {}
    manifest_paths = glob.glob(os.path.join(root, "*_reram_row*_*/manifest.txt"))
    for path in manifest_paths:
        m = read_manifest(path)
        row = parse_int(m.get("sweep_row"))
        if row is None:
            continue
        run_id = (m.get("run_id") or "").strip()
        prev = by_row.get(row)
        if prev is not None and run_id <= prev["run_id"]:
            continue
        run_dir = os.path.dirname(path)
        gen = parse_int(m.get("kmc_generation_count_max"))
        diff = parse_int(m.get("kmc_vacancy_diffusion_count_max"))
        if gen is None or diff is None:
            log_gen, log_diff = parse_kmc_counts_from_log(os.path.join(run_dir, "sdevice_stdout.log"))
            if gen is None:
                gen = log_gen
            if diff is None:
                diff = log_diff
        by_row[row] = {
            "row": row,
            "phase": (m.get("phase") or "").strip(),
            "group": (m.get("sweep_group") or "").strip(),
            "gen": gen or 0,
            "diff": diff or 0,
            "set_i": parse_float(m.get("set_current_abs_max_a")),
            "outcome": (m.get("outcome") or "").strip(),
            "notes": (m.get("notes") or "").strip(),
            "run_id": run_id,
            "source": "manifest",
        }
    return by_row


def build_records():
    rows = load_csv_rows(RESULTS_CSV)
    manifest_rows = load_latest_manifest_rows(RUNS_ROOT)
    # Manifest values are newer/more complete for rows that were not appended to reram_results.csv.
    rows.update(manifest_rows)
    return rows


def build_x_axis(rows_sorted):
    labels = []
    row_to_x = {}
    gap_positions = []
    prev = None
    for r in rows_sorted:
        if prev is not None and r - prev > 1:
            labels.append("")
            gap_positions.append(len(labels) - 1)
        labels.append(str(r))
        row_to_x[r] = len(labels) - 1
        prev = r
    return labels, row_to_x, gap_positions


def phase_segments(rows_sorted, records):
    segs = []
    if not rows_sorted:
        return segs
    start = rows_sorted[0]
    prev = rows_sorted[0]
    phase = records[start]["phase"] or "?"
    for r in rows_sorted[1:]:
        p = records[r]["phase"] or "?"
        if p == phase and r == prev + 1:
            prev = r
            continue
        segs.append((start, prev, phase))
        start = r
        prev = r
        phase = p
    segs.append((start, prev, phase))
    return segs


def main():
    records = build_records()
    if not records:
        raise SystemExit("No run records found.")

    rows_sorted = sorted(records.keys())
    labels, row_to_x, gap_positions = build_x_axis(rows_sorted)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(16, 9), gridspec_kw={"height_ratios": [3, 1.2]}
    )
    fig.patch.set_facecolor(BG)

    for ax in (ax1, ax2):
        ax.set_facecolor(PANEL_BG)
        ax.tick_params(colors=TEXT, labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(BORDER)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.5)
        ax.set_axisbelow(True)

    # ---------- TOP PANEL: KMC event counts ----------
    bar_width = 0.35
    for r in rows_sorted:
        d = records[r]
        x = row_to_x[r]
        gen_val = max(d["gen"], 0.4)
        diff_val = max(d["diff"], 0.4)
        color = PHASE_COLORS.get(d["phase"], BLUE)
        ax1.bar(x - bar_width / 2, gen_val, bar_width, color=color, alpha=0.9, edgecolor="none", zorder=3)
        ax1.bar(x + bar_width / 2, diff_val, bar_width, color=color, alpha=0.35, edgecolor="none", zorder=3)
        if d["outcome"] != "CONVERGED":
            ax1.plot(x, gen_val * 1.8, "x", color=RED, markersize=9, markeredgewidth=2.5, zorder=5)

    ax1.set_yscale("log")
    ax1.set_ylim(0.2, 8e7)
    ax1.set_ylabel("KMC Event Count", color=TEXT, fontsize=12, fontweight="bold")
    ax1.set_xticks(list(range(len(labels))))
    ax1.set_xticklabels(labels, fontsize=8, color=TEXT)

    for gx in gap_positions:
        ax1.axvline(gx, color=TEXT_DIM, linestyle=":", linewidth=1, alpha=0.4)
        ax1.text(gx, 0.35, "...", ha="center", va="top", fontsize=12, color=TEXT_DIM, fontweight="bold")

    for r_start, r_end, phase in phase_segments(rows_sorted, records):
        color = PHASE_COLORS.get(phase, BLUE)
        x_start = row_to_x[r_start] - 0.5
        x_end = row_to_x[r_end] + 0.5
        ax1.axvspan(x_start, x_end, alpha=0.06, color=color, zorder=0)
        mid_x = (row_to_x[r_start] + row_to_x[r_end]) / 2
        ax1.text(
            mid_x,
            5e7,
            f"Phase {phase}",
            ha="center",
            va="center",
            fontsize=8.5,
            color=color,
            fontweight="bold",
            alpha=0.8,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=BG, edgecolor="none", alpha=0.7),
        )

    if 27 in records:
        row27_x = row_to_x[27]
        row27_gen = max(records[27]["gen"], 0.4)
        ax1.annotate(
            "FIRST FILAMENT\nGROWTH > 0",
            xy=(row27_x, row27_gen),
            xytext=(max(0, row27_x - 5), 1.5e7),
            fontsize=11,
            fontweight="bold",
            color=GREEN,
            arrowprops=dict(
                arrowstyle="->",
                color=GREEN,
                lw=2.5,
                connectionstyle="arc3,rad=-0.2",
            ),
            ha="center",
            va="center",
            bbox=dict(
                boxstyle="round,pad=0.5",
                facecolor="#3fb95018",
                edgecolor=GREEN,
                lw=2,
            ),
        )

    legend_gen = mpatches.Patch(facecolor=ORANGE, alpha=0.9, label="Vacancy generation")
    legend_diff = mpatches.Patch(facecolor=ORANGE, alpha=0.35, label="Vacancy diffusion")
    legend_fail = plt.Line2D(
        [0],
        [0],
        marker="x",
        color=RED,
        linestyle="None",
        markersize=8,
        markeredgewidth=2,
        label="Convergence failure/timeout",
    )
    ax1.legend(
        handles=[legend_gen, legend_diff, legend_fail],
        loc="upper left",
        fontsize=9,
        facecolor=PANEL_BG,
        edgecolor=BORDER,
        labelcolor=TEXT,
        framealpha=0.9,
    )

    # ---------- BOTTOM PANEL: SET current ----------
    set_rows = [r for r in rows_sorted if records[r]["set_i"] is not None]
    set_x = [row_to_x[r] for r in set_rows]
    set_y = [records[r]["set_i"] for r in set_rows]
    set_colors = [PHASE_COLORS.get(records[r]["phase"], BLUE) for r in set_rows]

    if set_rows:
        ax2.scatter(set_x, set_y, c=set_colors, s=55, zorder=5, edgecolors="white", linewidths=0.5)
        ax2.plot(set_x, set_y, color=TEXT_DIM, alpha=0.3, linewidth=1, zorder=3)

    y_floor = 3e-16
    y_top = 2e-14
    ax2.set_yscale("log")
    ax2.set_ylim(y_floor, y_top)
    ax2.set_ylabel("Peak SET Current (A)", color=TEXT, fontsize=11, fontweight="bold")
    ax2.set_xlabel("Sweep Row", color=TEXT, fontsize=12, fontweight="bold")
    ax2.set_xticks([i for i, lbl in enumerate(labels) if lbl])
    ax2.set_xticklabels([lbl for lbl in labels if lbl], fontsize=7.5, color=TEXT)

    fail_x = []
    fail_y = []
    for r in rows_sorted:
        d = records[r]
        if d["set_i"] is None and d["outcome"] != "CONVERGED":
            fail_x.append(row_to_x[r])
            fail_y.append(y_floor * 1.2)
    if fail_x:
        ax2.scatter(fail_x, fail_y, marker="x", c=RED, s=50, linewidths=1.8, zorder=6)

    ax2.axhline(y=2.975e-15, color=TEXT_DIM, linestyle="--", alpha=0.3, linewidth=1)
    ax2.text(0.5, 3.2e-15, "leakage floor (~3 fA)", fontsize=8, color=TEXT_DIM, alpha=0.6)

    for r_start, r_end, phase in phase_segments(rows_sorted, records):
        color = PHASE_COLORS.get(phase, BLUE)
        ax2.axvspan(row_to_x[r_start] - 0.5, row_to_x[r_end] + 0.5, alpha=0.05, color=color, zorder=0)

    ax2.annotate(
        "",
        xy=(max(1, len(labels) - 1), 1.5e-14),
        xytext=(max(1, len(labels) - 1), 6e-15),
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.5, alpha=0.4),
    )
    ax2.text(max(1, len(labels) - 0.5), 1.6e-14, "switching target", fontsize=7, color=RED, alpha=0.5, ha="right")

    # ---------- Title block ----------
    run_count = len(rows_sorted)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    fig.suptitle(
        "HfO$_2$ Memristor: KMC ReRAM Parameter Exploration",
        fontsize=19,
        fontweight="bold",
        color=TEXT_BRIGHT,
        y=0.98,
    )
    fig.text(
        0.5,
        0.945,
        f"{run_count} sweep rows with data  |  Kinetic Monte Carlo defect physics  |  Updated {now}",
        ha="center",
        fontsize=11,
        color=TEXT_DIM,
        style="italic",
    )

    plt.tight_layout(rect=[0, 0, 1, 0.925])
    plt.savefig(OUT_PNG, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Saved: {OUT_PNG}")


if __name__ == "__main__":
    main()
