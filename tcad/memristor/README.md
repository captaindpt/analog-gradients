# Memristor TCAD Workspace

This folder tracks physics-first memristor work for ticket 0020.

Primary planning references:
- `my-workspace/docs/reference/MEMRISTOR_PRIMITIVE_SPEC.md`
- `my-workspace/docs/reference/MEMRISTOR_PAPER_STOCK.md`

## Layout

- `config/`: run configs and anchor-paper parameter selections.
- `runs/`: timestamped run directories (generated; avoid committing heavy raw data).
- `templates/`: schema/templates for run manifests and metric tables.

## Phase-A Anchor

Current default anchor:
- Strukov et al. 2008 (`papers/13b_nature06932_missing_memristor_found.pdf`)
- VCM-style bipolar behavior target.

## Workflow

1. Initialize run folder:
```bash
scripts/init_memristor_phase_a.sh
```

2. Place simulator decks and outputs under:
```text
tcad/memristor/runs/<timestamp>_<tag>/
```

3. Export time-voltage-current CSV from physics simulator and analyze:
```bash
python3 scripts/analyze_memristor_waveform.py \
  --csv tcad/memristor/runs/<run>/waveform.csv \
  --out-json tcad/memristor/runs/<run>/metrics.json \
  --out-md tcad/memristor/runs/<run>/metrics.md
```

## Notes

- Keep run artifacts reproducible, but avoid committing large binary dumps.
- Commit run manifests and derived metric summaries needed for evidence.
