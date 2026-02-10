# Memristor Paper Stock

Purpose: durable, manifest-complete index for the memristor paper library under
`papers/`, so primitive work can quickly resolve theory, physics, compact-model,
and system-level references.

Primary inventory sources:
- `papers/manifest.md`
- `my-workspace/logs/2026-02-09-memristor-paper-manifest.md`

## Priority Stack for Primitive Build

Use this order for physics-first primitive work:

1. `papers/12_chua_1971_memristor_missing_circuit_element.pdf`
2. `papers/09_chua_kang_memristive_devices_1975.pdf`
3. `papers/13b_nature06932_missing_memristor_found.pdf`
4. `papers/14_waser_aono_2007_nanoionics_resistive_switching.pdf`
5. `papers/10_vteam_improved_numerical_performance.pdf`
6. `papers/03_compact_VerilogA_ReRAM_switching.pdf`
7. `papers/04_data_driven_VerilogA_ReRAM.pdf`
8. `papers/05_reliable_spice_memristors.pdf`

## Manifest-Complete Catalog

Legend:
- `Tier`: P0 mandatory primitive references, P1 direct modeling references,
  P2 integration/training references, P3 context-only.
- `Primitive Use`: how directly useful the paper is for the new device primitive.

| ID | PDF | Markdown | Summary | Tier | Domain | Primitive Use |
|---|---|---|---|---|---|---|
| 01 | `papers/01_verilogA_memristor_models.pdf` | `papers/papers-markdown/01_verilogA_memristor_models.md` | no | P1 | compact modeling | Verilog-A implementation patterns |
| 02 | `papers/02_TEAM_CCIT_804.pdf` | `papers/papers-markdown/02_TEAM_CCIT_804.md` | no | P1 | compact modeling | threshold adaptive state equation |
| 03 | `papers/03_compact_VerilogA_ReRAM_switching.pdf` | `papers/papers-markdown/03_compact_VerilogA_ReRAM_switching.md` | no | P0 | compact modeling | data-guided switching-rate equations |
| 04 | `papers/04_data_driven_VerilogA_ReRAM.pdf` | `papers/papers-markdown/04_data_driven_VerilogA_ReRAM.md` | no | P0 | compact modeling | parameter extraction workflow |
| 05 | `papers/05_reliable_spice_memristors.pdf` | `papers/papers-markdown/05_reliable_spice_memristors.md` | no | P0 | numerical reliability | SPICE convergence and robustness rules |
| 06 | `papers/06_spice_model_nonlinear_dopant_drift.pdf` | `papers/papers-markdown/06_spice_model_nonlinear_dopant_drift.md` | no | P1 | compact modeling | baseline nonlinear drift model |
| 07 | `papers/07_cmos_level_memristor.pdf` | none | no | P3 | invalid source | invalid PDF (access-denied HTML), do not use |
| 08 | `papers/08_cmos_memristor_emulator_circuits.pdf` | `papers/papers-markdown/08_cmos_memristor_emulator_circuits.md` | no | P2 | CMOS fallback | backup primitive emulation direction |
| 09 | `papers/09_chua_kang_memristive_devices_1975.pdf` | `papers/papers-markdown/09_chua_kang_memristive_devices_1975.md` | no | P0 | theory | generalized memristive systems formalism |
| 10 | `papers/10_vteam_improved_numerical_performance.pdf` | `papers/papers-markdown/10_vteam_improved_numerical_performance.md` | no | P0 | compact modeling | voltage-threshold model + robust implementation |
| 11 | `papers/11_missing_memristor_has_not_been_found.pdf` | `papers/papers-markdown/11_missing_memristor_has_not_been_found.md` | no | P2 | claim hygiene | critical view to constrain wording/claims |
| 12 | `papers/12_chua_1971_memristor_missing_circuit_element.pdf` | `papers/papers-markdown/12_chua_1971_memristor_missing_circuit_element.md` | no | P0 | theory | original q-phi memristor definition |
| 13 | `papers/13_strukov_2008_missing_memristor_found.pdf` | `papers/papers-markdown/13_strukov_2008_missing_memristor_found.md` | no | P0 | device physics | drift-coupled physical model |
| 13b | `papers/13b_nature06932_missing_memristor_found.pdf` | `papers/papers-markdown/13b_nature06932_missing_memristor_found.md` | no | P0 | device physics | preferred citation variant of Strukov 2008 |
| 14 | `papers/14_waser_aono_2007_nanoionics_resistive_switching.pdf` | `papers/papers-markdown/14_waser_aono_2007_nanoionics_resistive_switching.md` | no | P0 | device physics | RRAM mechanism taxonomy |
| A1 | `papers/1712.05895v1.pdf` | `papers/papers-markdown/1712.05895v1.md` | yes | P2 | AIMC hardware | early on-chip training evidence |
| A2 | `papers/2006.01981v2.pdf` | `papers/papers-markdown/2006.01981v2.md` | yes | P3 | photonic context | adjacent analog-compute modality |
| A3 | `papers/2305.14547v1.pdf` | `papers/papers-markdown/2305.14547v1.md` | yes | P2 | AIMC training | mixed-precision training with memristors |
| A4 | `papers/2406.12774v1.pdf` | `papers/papers-markdown/2406.12774v1.md` | yes | P2 | training theory | analog SGD convergence limits |
| A5 | `papers/2412.09010v1.pdf` | `papers/papers-markdown/2412.09010v1.md` | yes | P2 | physical NN | train-on-hardware physical NN framing |
| A6 | `papers/2502.06309v3.pdf` | `papers/papers-markdown/2502.06309v3.md` | yes | P2 | training theory | residual learning on non-ideal devices |
| A7 | `papers/2506.17174v1.pdf` | `papers/papers-markdown/2506.17174v1.md` | yes | P1 | device evidence | modern forming/compliance-free device data |
| A8 | `papers/2506.18041v1.pdf` | `papers/papers-markdown/2506.18041v1.md` | yes | P3 | photonic training | adjacent analog training architecture |
| A9 | `papers/2510.02516v1.pdf` | `papers/papers-markdown/2510.02516v1.md` | yes | P2 | training theory | multi-tile residual learning |
| A10 | `papers/s41467-024-51221-z.pdf` | `papers/papers-markdown/s41467-024-51221-z.md` | yes | P2 | training algorithm | AGAD / c-TTv2 robustness algorithms |

## Grouped Reading Order

1. Theory foundation:
   `papers/12_chua_1971_memristor_missing_circuit_element.pdf`,
   `papers/09_chua_kang_memristive_devices_1975.pdf`.
2. Physical mechanisms:
   `papers/14_waser_aono_2007_nanoionics_resistive_switching.pdf`,
   `papers/13b_nature06932_missing_memristor_found.pdf`.
3. Compact model stack:
   `papers/10_vteam_improved_numerical_performance.pdf`,
   `papers/03_compact_VerilogA_ReRAM_switching.pdf`,
   `papers/04_data_driven_VerilogA_ReRAM.pdf`,
   `papers/05_reliable_spice_memristors.pdf`.
4. Fallback and integration context:
   `papers/08_cmos_memristor_emulator_circuits.pdf`,
   `papers/2305.14547v1.pdf`,
   `papers/2506.17174v1.pdf`.

## Immediate Primitive Baseline Citations

Any internal memristor primitive spec/report should cite at minimum:

1. `papers/12_chua_1971_memristor_missing_circuit_element.pdf`
2. `papers/09_chua_kang_memristive_devices_1975.pdf`
3. `papers/13b_nature06932_missing_memristor_found.pdf`
4. `papers/14_waser_aono_2007_nanoionics_resistive_switching.pdf`
5. `papers/10_vteam_improved_numerical_performance.pdf`
6. `papers/03_compact_VerilogA_ReRAM_switching.pdf` or
   `papers/04_data_driven_VerilogA_ReRAM.pdf`

## Extracted Text Locations

- Full extracted text: `papers/papers-markdown/*.md`
- Human-readable summaries: `papers/papers-markdown/*_summary.md`
