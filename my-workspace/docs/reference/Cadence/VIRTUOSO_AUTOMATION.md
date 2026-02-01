# Virtuoso Automation - Working Solutions

This file documents the working technical solutions for automating Cadence Virtuoso.

---

## Environment Setup (CMC Cloud)

```bash
# Source both scripts to get all tools
source /CMC/scripts/cadence.ic23.10.140.csh
source /CMC/scripts/cadence.spectre23.10.802.csh

# Verify tools are available
which virtuoso   # /CMC/tools/cadence/IC23.10.140_lnx86/...
which spectre    # /CMC/tools/cadence/SPECTRE23.10.802_lnx86/tools.lnx86/bin/spectre
which ocean      # /CMC/tools/cadence/IC23.10.140_lnx86/tools.lnx86/dfII/bin/ocean
```

---

## Repo Automation Runner (Headless-Friendly)

This repo includes a helper that runs SKILL scripts via Virtuoso replay mode,
handling DISPLAY vs Xvfb automatically.

```bash
./scripts/virtuoso_replay.sh skill/L5_inverter.il
```

Behavior:
- If `DISPLAY` is set, it uses it directly.
- If `DISPLAY` is not set but `xvfb-run` exists, it runs under Xvfb.
- Otherwise it fails with a clear error message and next steps.

---

## License Configuration

If Spectre/Virtuoso fails with `LMC-01902`, configure license variables first.
See `my-workspace/docs/reference/Cadence/LICENSE_SETUP.md`.

---

## OCEAN Scripting (Verified Working)

OCEAN is the scriptable simulation interface. It uses SKILL syntax.

### Running OCEAN Interactively

```bash
ocean -nograph
```

Then at the `>` prompt:
```lisp
1 + 1          ; returns 2
printf("hello\n")  ; prints "hello"
exit()         ; exits ocean
```

### Running OCEAN Scripts

**Issue:** stdout is buffered in non-interactive mode. Use file output instead.

```lisp
; test_ocean.ocn
out = outfile("/home/v71349/test_output.txt" "w")
fprintf(out "OCEAN is working\n")
close(out)
exit()
```

Run with:
```bash
ocean -nograph < test_ocean.ocn
cat ~/test_output.txt
```

---

## Virtuoso Automation Methods

### 1. CIW Command Line
Pipe SKILL commands to CIW via stdin when launching:
```bash
virtuoso -replay script.il
```

### 2. Socket-based IPC
Virtuoso supports socket communication through SKILL:
```lisp
; Create server socket that listens for commands
ipcSkillProcess("server")
```

### 3. Batch Mode
Run SKILL scripts non-interactively:
```bash
virtuoso -replay script.il -nograph
```

### 4. OCEAN for Simulation Automation
Best for running Spectre simulations:
```lisp
simulator('spectre)
design("/path/to/netlist")
analysis('tran ?stop "100n")
run()

; Check results
vout = value(VT("/vout") 100n)
if(vout > 0.9 then
    printf("PASS\n")
else
    printf("FAIL\n")
)
```

---

## Key Paths on CMC Cloud

| Path | Description |
|------|-------------|
| `/CMC/scripts/` | Setup scripts for all tools |
| `/CMC/tools/cadence/` | Cadence installations |
| `/CMC/tools/cadence/IC23.10.140_lnx86/` | Virtuoso IC23 |
| `/CMC/tools/cadence/SPECTRE23.10.802_lnx86/` | Spectre 23 |
| `/CMC/kits/` | Process Design Kits (PDKs) |
| `~/cds.lib` | Your library definitions |

---

## Agent Loop Architecture

```
┌─────────────────────────────────────────────────┐
│  USER PROMPT: "Build me a GPU core"             │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│  DECOMPOSITION SCRATCHPAD                       │
│  GPU_core → ALU → adder → full_adder → gates   │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│  FOR EACH COMPONENT (bottom-up):                │
│  1. Generate SKILL code                         │
│  2. Execute in Virtuoso (MCP tool)              │
│  3. Run OCEAN simulation                        │
│  4. If pass → save to COMPONENT_LIBRARY         │
│  5. Compact context, keep interface only        │
└─────────────────────────────────────────────────┘
```

### MCP Toolset

```typescript
tools: [
  "create_schematic",      // SKILL → Virtuoso
  "create_testbench",      // SKILL → test harness
  "run_ocean_test",        // OCEAN script → PASS/FAIL
  "save_to_library",       // persist verified component
  "list_library",          // what's available
  "instantiate_component", // place existing component
  "connect"                // wire things together
]
```

---

## Guelph-1 Student GPU Spec

### Target Demo

```
Prompt: "Build me a 4-core SIMD execution unit, 8-bit ALUs"

Agent builds:
1. Transistors → NAND gate (verified)
2. NANDs → XOR, AND, OR (verified)
3. Gates → full adder (verified)
4. Adders → 8-bit ALU (verified)
5. ALU × 4 with shared control
```

### Spec

- **Compute:** 4 PEs, 16-bit integer ALU each, SIMD execution
- **Memory:** 4KB shared SRAM, 16-bit bus
- **Control:** 8-bit instruction encoding, ~16 instructions
- **Physical:** 180nm process, 10-25 MHz, <100mW

### Hierarchy

```
Level 5: CMOS (inverter, NAND, NOR, transmission gate)
Level 4: Logic gates (AND, OR, XOR, NOT)
Level 3: Building blocks (adder, mux, register, decoder)
Level 2: RTL components (ALU, SRAM, FSM)
Level 1: Functional blocks (PE array, memory, control)
Level 0: System (GPU core)
```

---

## Demo Timeline

| Date | Milestone |
|------|-----------|
| Dec 19-30 | Build the tool |
| Dec 31 - Jan 2 | Record polished demo video |
| Jan 3-7 | Warm up LinkedIn |
| **Jan 8** | **Launch day** |

### Target Audience
- Thomas Andersen (Synopsys VP of AI/ML)
- Anupam Verma (Cadence Director, AI/UX)
- EDA LinkedIn community

### Clickbait
> "Watch AI design a GPU core in 60 seconds"

Building from transistors up, verified at each level.
