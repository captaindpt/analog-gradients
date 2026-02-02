# NeuroCore Paper Workthrough

LaTeX source for a video-aligned technical workthrough with:
- dark-theme unsmoothed waveform figures plotted from raw CSV points,
- robustness sweep figure,
- stack/full-flow status tables,
- reproducibility command section.

## Main Source

- `competition/paper/neurocore_workthrough.tex`

## Data Inputs

- `competition/data/*.csv`
- `competition/sweeps/neuro_tile4_coupled_sweep.csv`

## Derived Data (auto-generated)

- `competition/paper/data/neuro_tile4_coupled_sweep_parsed.csv`
- `competition/paper/data/first_spike_summary.csv`
- `competition/paper/data/sweep_mem2_rleak_*.csv`

## Build

```bash
scripts/build_paper.sh
```

If no LaTeX engine is installed, the script still prepares all sources/data and
prints what to install next.
