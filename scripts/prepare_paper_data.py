#!/usr/bin/env python3
"""Prepare parsed CSV artifacts for the LaTeX workthrough paper."""

import csv
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
SWEEP_IN = REPO_DIR / "competition" / "sweeps" / "neuro_tile4_coupled_sweep.csv"
NEURO_SPIKES_IN = REPO_DIR / "competition" / "data" / "neuro_tile4_spikes.csv"
COUPLED_SPIKES_IN = REPO_DIR / "competition" / "data" / "neuro_tile4_coupled_spikes.csv"
OUT_DIR = REPO_DIR / "competition" / "paper" / "data"


def parse_value(text):
    text = text.strip()
    if text.endswith("k"):
        return float(text[:-1]) * 1e3
    if text.endswith("M"):
        return float(text[:-1]) * 1e6
    return float(text)


def parse_spike_counts(text):
    out = {}
    for item in text.split():
        name, val = item.split("=")
        out[name] = int(val)
    return out


def parse_float_list(text):
    return [float(x.strip()) for x in text.split(",")]


def build_sweep_parsed():
    rows = []
    with SWEEP_IN.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mems = parse_float_list(row["membrane_maxima"])
            spikes = parse_spike_counts(row["spike_counts"])
            smax = parse_float_list(row["spike_maxima"])
            rows.append(
                {
                    "r_fb_ohm": f"{parse_value(row['r_fb']):.0f}",
                    "rleak_ohm": f"{parse_value(row['rleak']):.0f}",
                    "pass": row["pass"],
                    "mem0_max_v": f"{mems[0]:.3f}",
                    "mem1_max_v": f"{mems[1]:.3f}",
                    "mem2_max_v": f"{mems[2]:.3f}",
                    "mem3_max_v": f"{mems[3]:.3f}",
                    "spike0_count": str(spikes["spike0"]),
                    "spike1_count": str(spikes["spike1"]),
                    "spike2_count": str(spikes["spike2"]),
                    "spike3_count": str(spikes["spike3"]),
                    "spike0_max_v": f"{smax[0]:.3f}",
                    "spike1_max_v": f"{smax[1]:.3f}",
                    "spike2_max_v": f"{smax[2]:.3f}",
                    "spike3_max_v": f"{smax[3]:.3f}",
                }
            )

    out_path = OUT_DIR / "neuro_tile4_coupled_sweep_parsed.csv"
    keys = list(rows[0].keys())
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)

    grouped = {
        "6000000": [],
        "8000000": [],
        "10000000": [],
    }
    for row in rows:
        grouped[row["rleak_ohm"]].append(
            {
                "r_fb_ohm": row["r_fb_ohm"],
                "mem2_max_v": row["mem2_max_v"],
                "spike2_max_v": row["spike2_max_v"],
            }
        )

    for rleak_ohm, group_rows in grouped.items():
        out_group = OUT_DIR / f"sweep_mem2_rleak_{rleak_ohm}.csv"
        with out_group.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["r_fb_ohm", "mem2_max_v", "spike2_max_v"])
            w.writeheader()
            w.writerows(group_rows)
    return out_path


def first_spike_times(path, threshold=0.4):
    first = {"spike0": None, "spike1": None, "spike2": None, "spike3": None}
    with path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = float(row["time_ns"])
            for sig in list(first.keys()):
                if first[sig] is None and float(row[sig]) >= threshold:
                    first[sig] = t
    return first


def build_first_spike_summary():
    neuro = first_spike_times(NEURO_SPIKES_IN)
    coupled = first_spike_times(COUPLED_SPIKES_IN)

    out_path = OUT_DIR / "first_spike_summary.csv"
    rows = [
        {"dataset": "neuro_tile4", **{k: f"{v:.3f}" for k, v in neuro.items()}},
        {"dataset": "neuro_tile4_coupled", **{k: f"{v:.3f}" for k, v in coupled.items()}},
    ]
    keys = ["dataset", "spike0", "spike1", "spike2", "spike3"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    return out_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sweep_path = build_sweep_parsed()
    first_spike_path = build_first_spike_summary()
    print(f"Wrote {sweep_path}")
    print(f"Wrote {first_spike_path}")


if __name__ == "__main__":
    main()
