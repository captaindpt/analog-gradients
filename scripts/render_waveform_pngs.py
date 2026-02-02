#!/usr/bin/env python3
"""Render lightweight PNG waveform plots from competition CSV exports."""

import argparse
import csv
import struct
import zlib
from pathlib import Path
from typing import Dict, List, Tuple


PALETTES = [
    (21, 101, 192),
    (46, 125, 50),
    (239, 108, 0),
    (106, 27, 154),
    (0, 131, 143),
    (198, 40, 40),
]

BG = (248, 251, 255)
PLOT_BG = (255, 255, 255)
GRID = (226, 232, 240)
BORDER = (148, 163, 184)


def read_csv(path: Path) -> Dict[str, List[float]]:
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"No data rows in {path}")
    keys = list(rows[0].keys())
    out = {k: [] for k in keys}
    for row in rows:
        for key in keys:
            out[key].append(float(row[key]))
    return out


def set_px(buf: bytearray, width: int, height: int, x: int, y: int, rgb: Tuple[int, int, int]) -> None:
    if x < 0 or y < 0 or x >= width or y >= height:
        return
    idx = (y * width + x) * 3
    buf[idx : idx + 3] = bytes(rgb)


def draw_line(
    buf: bytearray,
    width: int,
    height: int,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    rgb: Tuple[int, int, int],
    thickness: int = 1,
) -> None:
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0

    while True:
        for tx in range(-thickness, thickness + 1):
            for ty in range(-thickness, thickness + 1):
                if tx * tx + ty * ty <= thickness * thickness:
                    set_px(buf, width, height, x + tx, y + ty, rgb)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def draw_rect(
    buf: bytearray,
    width: int,
    height: int,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    fill: Tuple[int, int, int],
    border: Tuple[int, int, int],
) -> None:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            set_px(buf, width, height, x, y, fill)
    draw_line(buf, width, height, x0, y0, x1, y0, border)
    draw_line(buf, width, height, x1, y0, x1, y1, border)
    draw_line(buf, width, height, x1, y1, x0, y1, border)
    draw_line(buf, width, height, x0, y1, x0, y0, border)


def png_chunk(tag: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(tag + payload) & 0xFFFFFFFF
    return struct.pack("!I", len(payload)) + tag + payload + struct.pack("!I", crc)


def write_png(path: Path, width: int, height: int, buf: bytearray) -> None:
    rows = []
    row_bytes = width * 3
    for y in range(height):
        start = y * row_bytes
        rows.append(b"\x00" + bytes(buf[start : start + row_bytes]))
    raw = b"".join(rows)
    compressed = zlib.compress(raw, level=9)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)
    data = sig + png_chunk(b"IHDR", ihdr) + png_chunk(b"IDAT", compressed) + png_chunk(b"IEND", b"")
    path.write_bytes(data)


def render_plot(csv_path: Path, signals: List[str], out_png: Path) -> None:
    data = read_csv(csv_path)
    t = data["time_ns"]

    width, height = 1600, 900
    left, top = 120, 90
    plot_w, plot_h = 1400, 700
    x0, y0 = left, top
    x1, y1 = left + plot_w, top + plot_h

    xmin, xmax = min(t), max(t)
    y_values = [v for sig in signals for v in data[sig]]
    ymin, ymax = min(y_values), max(y_values)
    if ymax - ymin < 1e-9:
        ymax = ymin + 1.0

    buf = bytearray(bytes(BG) * (width * height))
    draw_rect(buf, width, height, x0, y0, x1, y1, PLOT_BG, BORDER)

    for i in range(1, 10):
        yy = y0 + int((plot_h * i) / 10)
        draw_line(buf, width, height, x0, yy, x1, yy, GRID)
    for i in range(1, 10):
        xx = x0 + int((plot_w * i) / 10)
        draw_line(buf, width, height, xx, y0, xx, y1, GRID)

    def map_xy(x: float, y: float) -> Tuple[int, int]:
        px = x0 + int((x - xmin) * plot_w / max(xmax - xmin, 1e-9))
        py = y1 - int((y - ymin) * plot_h / max(ymax - ymin, 1e-9))
        return px, py

    for idx, sig in enumerate(signals):
        color = PALETTES[idx % len(PALETTES)]
        xs = data["time_ns"]
        ys = data[sig]
        prev = map_xy(xs[0], ys[0])
        for x, y in zip(xs[1:], ys[1:]):
            curr = map_xy(x, y)
            draw_line(buf, width, height, prev[0], prev[1], curr[0], curr[1], color, thickness=2)
            prev = curr

    write_png(out_png, width, height, buf)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    jobs = [
        ("synapse_waveform.csv", ["pre", "post", "out"]),
        ("lif_neuron_waveform.csv", ["mem", "spike", "out"]),
        ("neuron_tile_waveform.csv", ["syn_post", "mem", "spike"]),
        ("neuro_tile4_spikes.csv", ["spike0", "spike1", "spike2", "spike3"]),
        ("neuro_tile4_mems.csv", ["mem0", "mem1", "mem2", "mem3"]),
        ("neuro_tile4_coupled_spikes.csv", ["spike0", "spike1", "spike2", "spike3"]),
        ("neuro_tile4_coupled_mems.csv", ["mem0", "mem1", "mem2", "mem3"]),
    ]

    for csv_name, signals in jobs:
        csv_path = data_dir / csv_name
        png_name = csv_name.replace(".csv", ".png")
        render_plot(csv_path, signals, out_dir / png_name)

    print(f"Generated PNG waveforms in {out_dir}")


if __name__ == "__main__":
    main()
