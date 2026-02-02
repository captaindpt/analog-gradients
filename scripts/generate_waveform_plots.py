#!/usr/bin/env python3
"""Generate SVG waveform plots from exported CSV data."""

import csv
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_DIR / "competition" / "data"
OUT_DIR = REPO_DIR / "competition" / "plots"


PALETTES = [
    "#1565c0",
    "#2e7d32",
    "#ef6c00",
    "#6a1b9a",
    "#00838f",
    "#c62828",
]


def read_csv(path):
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    header = rows[0].keys()
    series = {k: [] for k in header}
    for row in rows:
        for k in header:
            series[k].append(float(row[k]))
    return series


def polyline(xs, ys, x0, y0, w, h, xmin, xmax, ymin, ymax):
    points = []
    xspan = max(xmax - xmin, 1e-9)
    yspan = max(ymax - ymin, 1e-9)
    for x, y in zip(xs, ys):
        px = x0 + (x - xmin) * w / xspan
        py = y0 + h - (y - ymin) * h / yspan
        points.append(f"{px:.2f},{py:.2f}")
    return " ".join(points)


def text(x, y, val, size=14, weight="normal", fill="#1f2937"):
    esc = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc}</text>'
    )


def render_plot(csv_name, title, signals, y_min=0.0, y_max=1.8):
    src = DATA_DIR / csv_name
    data = read_csv(src)
    t = data["time_ns"]

    width, height = 1400, 820
    left, top = 110, 90
    plot_w, plot_h = 1180, 560
    xmin, xmax = min(t), max(t)

    body = []
    body.append('<rect x="0" y="0" width="100%" height="100%" fill="#f8fbff"/>')
    body.append(text(30, 44, title, size=30, weight="bold"))
    body.append(
        f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" '
        'fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>'
    )

    for i in range(0, 11):
        y = top + plot_h * i / 10.0
        val = y_max - (y_max - y_min) * i / 10.0
        body.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" '
            'stroke="#e2e8f0" stroke-width="1"/>'
        )
        body.append(text(30, y + 5, f"{val:.2f}V", size=13, fill="#64748b"))

    for i in range(0, 11):
        x = left + plot_w * i / 10.0
        val = xmin + (xmax - xmin) * i / 10.0
        body.append(
            f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_h}" '
            'stroke="#e2e8f0" stroke-width="1"/>'
        )
        body.append(text(x - 18, top + plot_h + 26, f"{val:.0f}ns", size=13, fill="#64748b"))

    for idx, sig in enumerate(signals):
        pts = polyline(t, data[sig], left, top, plot_w, plot_h, xmin, xmax, y_min, y_max)
        color = PALETTES[idx % len(PALETTES)]
        body.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.4"/>'
        )

    leg_x, leg_y = left + 20, top + plot_h + 55
    for idx, sig in enumerate(signals):
        color = PALETTES[idx % len(PALETTES)]
        y = leg_y + idx * 28
        body.append(f'<line x1="{leg_x}" y1="{y}" x2="{leg_x+30}" y2="{y}" stroke="{color}" stroke-width="4"/>')
        body.append(text(leg_x + 40, y + 5, sig, size=18))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        + "\n".join(body)
        + "\n</svg>\n"
    )
    out_name = csv_name.replace(".csv", ".svg")
    (OUT_DIR / out_name).write_text(svg, encoding="utf-8")


def write_readme():
    content = """# Competition Waveform Plots

Generated from:

```bash
scripts/export_competition_waveforms.sh
python3 scripts/generate_waveform_plots.py
```

## Files

- `synapse_waveform.svg`
- `lif_neuron_waveform.svg`
- `neuron_tile_waveform.svg`
- `neuro_tile4_spikes.svg`
- `neuro_tile4_mems.svg`
- `neuro_tile4_coupled_spikes.svg`
- `neuro_tile4_coupled_mems.svg`
"""
    (OUT_DIR / "README.md").write_text(content, encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    render_plot("synapse_waveform.csv", "Synapse Waveforms (pre/post/out)", ["pre", "post", "out"])
    render_plot("lif_neuron_waveform.csv", "LIF Neuron Waveforms (mem/spike/out)", ["mem", "spike", "out"])
    render_plot("neuron_tile_waveform.csv", "Neuron Tile Waveforms (syn_post/mem/spike)", ["syn_post", "mem", "spike"])
    render_plot("neuro_tile4_spikes.csv", "Neuro Tile4 Spike Channels", ["spike0", "spike1", "spike2", "spike3"])
    render_plot("neuro_tile4_mems.csv", "Neuro Tile4 Membrane Channels", ["mem0", "mem1", "mem2", "mem3"])
    render_plot("neuro_tile4_coupled_spikes.csv", "Neuro Tile4 Coupled Spike Channels", ["spike0", "spike1", "spike2", "spike3"])
    render_plot("neuro_tile4_coupled_mems.csv", "Neuro Tile4 Coupled Membrane Channels", ["mem0", "mem1", "mem2", "mem3"])
    write_readme()
    print(f"Generated waveform plots in {OUT_DIR}")


if __name__ == "__main__":
    main()
