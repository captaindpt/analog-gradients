# Session: 2026-02-02 - Paper Workthrough Bring-Up

## Summary

Focused fully on a LaTeX technical workthrough for competition/demo support.
Added dark-theme, raw-point plotting in LaTeX (PGFPlots), tables, and scripted
paper data preparation.

## Added

- `competition/paper/neurocore_workthrough.tex`
- `competition/paper/README.md`
- `competition/paper/data/` derived CSV artifacts
- `scripts/prepare_paper_data.py`
- `scripts/build_paper.sh`
- Ticket: `my-workspace/tickets/0011-competition-paper-workthrough.md`

## Validation

- Data prep script runs and writes parsed paper data.
- Paper build script executes and reports missing local LaTeX engine.

## Notes

- Paper source is ready for compile in a LaTeX-enabled environment.
- Figures are intentionally unsmoothed and use real sampled data points.
