#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PAPER_DIR="$REPO_DIR/competition/paper"
PAPER_TEX="$PAPER_DIR/neurocore_workthrough.tex"

python3 "$REPO_DIR/scripts/prepare_paper_data.py"

LATEX_BIN=""
for candidate in pdflatex xelatex lualatex tectonic; do
  if command -v "$candidate" >/dev/null 2>&1; then
    LATEX_BIN="$candidate"
    break
  fi
done

if [[ -z "$LATEX_BIN" ]]; then
  echo "No LaTeX engine found (pdflatex/xelatex/lualatex/tectonic)." >&2
  echo "Prepared sources only:" >&2
  echo "  $PAPER_TEX" >&2
  echo "Install a LaTeX engine, then re-run scripts/build_paper.sh." >&2
  exit 2
fi

echo "Using LaTeX engine: $LATEX_BIN"
if [[ "$LATEX_BIN" == "tectonic" ]]; then
  "$LATEX_BIN" "$PAPER_TEX" --outdir "$PAPER_DIR"
else
  "$LATEX_BIN" -interaction=nonstopmode -output-directory "$PAPER_DIR" "$PAPER_TEX"
  "$LATEX_BIN" -interaction=nonstopmode -output-directory "$PAPER_DIR" "$PAPER_TEX"
fi

echo "Paper build complete:"
echo "  $PAPER_DIR/neurocore_workthrough.pdf"
