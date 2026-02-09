#!/usr/bin/env python3
"""
Extract I-V data from Sentaurus SDevice .plt (DF-ISE text) files.

Parses the DF-ISE xyplot format and outputs a CSV with columns:
  time_s, voltage_v, current_a

Usage:
  python3 scripts/extract_plt_to_csv.py <input.plt> <output.csv> [--electrode top]
"""

import argparse
import csv
import re
import sys
from typing import List, Tuple


def parse_plt(path: str) -> Tuple[List[str], List[List[float]]]:
    """Parse a DF-ISE xyplot .plt file. Returns (dataset_names, rows)."""
    with open(path, "r") as f:
        text = f.read()

    # Extract dataset names from Info block
    ds_match = re.search(r'datasets\s*=\s*\[(.*?)\]', text, re.DOTALL)
    if not ds_match:
        raise ValueError("No datasets block found in PLT file")

    names = re.findall(r'"([^"]+)"', ds_match.group(1))

    # Extract numeric data from Data block
    data_match = re.search(r'Data\s*\{(.*)\}', text, re.DOTALL)
    if not data_match:
        raise ValueError("No Data block found in PLT file")

    numbers = re.findall(r'[+-]?\d+\.\d+[Ee][+-]?\d+|[+-]?\d+\.\d+|\d+', data_match.group(1))
    values = [float(x) for x in numbers]

    ncols = len(names)
    if len(values) % ncols != 0:
        print(f"WARNING: {len(values)} values not evenly divisible by {ncols} columns",
              file=sys.stderr)

    rows = []
    for i in range(0, len(values) - ncols + 1, ncols):
        rows.append(values[i:i + ncols])

    return names, rows


def extract_iv(names: List[str], rows: List[List[float]],
               electrode: str) -> List[Tuple[float, float, float]]:
    """Extract (time, voltage, current) for the given electrode name."""

    # Find voltage column: "<electrode> OuterVoltage"
    v_name = f"{electrode} OuterVoltage"
    i_name = f"{electrode} TotalCurrent"

    v_idx = None
    i_idx = None
    for idx, name in enumerate(names):
        if name == v_name:
            v_idx = idx
        if name == i_name:
            i_idx = idx

    if v_idx is None:
        avail = [n for n in names if "Voltage" in n or "Current" in n]
        raise ValueError(f"Electrode '{electrode}' voltage not found. Available: {avail}")
    if i_idx is None:
        avail = [n for n in names if "Current" in n]
        raise ValueError(f"Electrode '{electrode}' current not found. Available: {avail}")

    result = []
    for row in rows:
        if len(row) > max(v_idx, i_idx):
            result.append((row[0], row[v_idx], row[i_idx]))

    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract I-V from Sentaurus PLT file.")
    ap.add_argument("input", help="Input .plt file")
    ap.add_argument("output", help="Output .csv file")
    ap.add_argument("--electrode", default="top",
                    help="Electrode name to extract (default: top)")
    args = ap.parse_args()

    names, rows = parse_plt(args.input)

    # Print available datasets for debugging
    print(f"PLT datasets ({len(names)} columns): {names[:6]}...")
    print(f"PLT rows: {len(rows)}")

    iv = extract_iv(names, rows, args.electrode)

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "voltage_v", "current_a"])
        for t, v, i in iv:
            writer.writerow([t, v, i])

    print(f"Wrote {len(iv)} data points to {args.output}")


if __name__ == "__main__":
    main()
