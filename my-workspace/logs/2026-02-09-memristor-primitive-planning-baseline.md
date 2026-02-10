# 2026-02-09 - Memristor Primitive Planning Baseline

## Objective

Convert the newly pulled memristor paper drop into reusable repo knowledge:

1. A durable paper reference stock inside source docs.
2. One exhaustive planning spec for a physics-first memristor primitive path.

## Work Completed

- Pulled latest `origin/main` with memristor paper library additions under
  `papers/` and `papers/papers-markdown/`.
- Reviewed `papers/manifest.md` and extracted markdown/summary files across:
  - theory/foundations
  - RRAM device physics and switching mechanisms
  - Verilog-A/SPICE compact modeling
  - recent AIMC training and hardware-algorithm co-design context
- Added reference stock index:
  - `my-workspace/docs/reference/MEMRISTOR_PAPER_STOCK.md`
- Added exhaustive planning specification:
  - `my-workspace/docs/reference/MEMRISTOR_PRIMITIVE_SPEC.md`
- Linked new docs into canonical navigation:
  - `my-workspace/docs/reference/README.md`
  - `my-workspace/docs/INDEX.md`
  - `my-workspace/docs/STATUS.md`
- Opened tracking ticket:
  - `my-workspace/tickets/0020-memristor-primitive-physics-first-workstream.md`

## Planning Outcomes Frozen

- Mainstream baseline class: oxide-based bipolar VCM ReRAM.
- Primary physical simulation direction: Sentaurus-first.
- Downstream integration direction: Spectre + OCEAN compact-model verification.
- Initial acceptance allows energy/event within 2x to 3x of anchor-paper
  operating point for proof-of-concept.

## Next Steps

1. Choose anchor paper/device target for phase-A calibration.
2. Create minimal headless physics run and metric extractor scripts.
3. Fit first compact model candidate and build Spectre/OCEAN verifier.
