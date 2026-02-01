# GPU Demo Spec (Path of Least Resistance)

This is a minimal, end-to-end demo target that is realistic for netlist-based
verification and builds directly on the Level 4 gates.

## GPU-Lite v0 (M0)

**Goal:** A verified, combinational 4-bit ALU block with simple opcode control.

### Block
- Inputs: `A[3:0]`, `B[3:0]`, `OP[1:0]`
- Outputs: `Y[3:0]`, `COUT`
- Operations:
  - `00`: AND
  - `01`: OR
  - `10`: XOR
  - `11`: ADD (ripple-carry)

### Acceptance Criteria
- Netlist + OCEAN tests for each op
- Truth-table-based spot checks at multiple vectors
- Integrated ALU netlist passes OCEAN verification

## GPU-Lite v1 (M1)

**Goal:** Add minimal state to make it feel like a “core.”

### Block Additions
- 2x 4-bit input registers (A/B)
- 4-bit output register
- 2-bit opcode register
- Single clock input

### Acceptance Criteria
- Register write/read verified
- ALU integration verified across clock edges

## GPU-Lite v2 (M2)

**Goal:** Minimal multi-PE demo.

### Block Additions
- 2–4 PEs sharing opcode
- Shared input bus, per-PE output

### Acceptance Criteria
- Parallel operation verified (same opcode, independent A/B)

### Current Implementation
- `pe1.scs`: single PE with ALU4
- `pe4.scs`: 4x PE array with shared opcode

## GPU-Lite v3 (M3)

**Goal:** Minimal system wrapper (GPU core).

### Block Additions
- Top-level wrapper around PE4
- Single entry point for opcode and IO vectors

### Acceptance Criteria
- `gpu_core.scs` netlist + `test_gpu_core.ocn`
- Spot-check verification passes

---

This spec keeps the demo “GPU-shaped” while staying feasible with the current
netlist + OCEAN flow.
