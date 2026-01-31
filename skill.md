# CMC Cloud + Claude + OCEAN Workflow

## Mission

Hook up Claude to Cadence OCEAN on CMC Cloud. Build circuit elements bottom-up: transistors → gates → adders → ALU. Verify each component via simulation before composing.

---

## Quick Connect

```bash
# From iTerm (with XQuartz running)
ssh -Y -p 31487 v71349@130.15.52.59
```

Password: get from CMC Cloud portal each session.

---

## On CMC Cloud

### Setup (every session)
```bash
source /CMC/scripts/cadence.ic23.10.140.csh
source /CMC/scripts/cadence.spectre23.10.802.csh
```

### Run Claude (print mode - TUI broken)
```bash
claude --print "your task here"
claude --print --permission-mode acceptEdits "task with file access"
```

### Run OCEAN
```bash
ocean -nograph
```

### Run Virtuoso GUI (needs X11)
```bash
virtuoso &
```

---

## Constraints

| What | Status |
|------|--------|
| OCEAN interactive | ✅ Works |
| OCEAN simulation scripts | ✅ Works |
| Claude --print mode | ✅ Works |
| Claude TUI | ❌ Raw mode error |
| Headless schematic creation | ❌ Needs X11 |
| GUI + SKILL scripts | ✅ Works (load in CIW) |

**Key insight:** Schematic creation via SKILL requires X11 display even in "nograph" mode. Two paths:
1. **GUI-assisted:** Run Virtuoso with X11, load SKILL via CIW
2. **Virtual display:** Use Xvfb for headless X11 (untested)

---

## Build Hierarchy

```
Level 5: CMOS (inverter, NAND, NOR)
Level 4: Logic gates (AND, OR, XOR)
Level 3: Building blocks (adder, mux, register)
Level 2: RTL (ALU, SRAM, FSM)
Level 1: Functional blocks (PE array, memory)
Level 0: System (GPU core)
```

---

## Library Setup

```bash
# Your library
~/inverter/

# cds.lib
SOFTINCLUDE /CMC/tools/cadence/IC23.10.140_lnx86/share/cdssetup/cds.lib
DEFINE inverter /home/v71349/inverter

# analogLib components available via SOFTINCLUDE:
# nmos4, pmos4, vdc, gnd, vpulse, res, cap, etc.
```

---

## OCEAN Script Template

```lisp
; simulation_test.ocn
out = outfile("/home/v71349/sim_results.txt" "w")

simulator('spectre)
design("/path/to/netlist")
analysis('tran ?stop "100n")
run()

vout = value(VT("/vout") 100n)
if(vout > 0.9 then
    fprintf(out "PASS\n")
else
    fprintf(out "FAIL\n")
)

close(out)
exit()
```

Run: `ocean -nograph < simulation_test.ocn`

---

## SKILL Schematic Template

```lisp
; create_nand.il - run in Virtuoso CIW with: load("create_nand.il")
lib = "inverter"
cell = "nand2"
view = "schematic"

cv = dbOpenCellViewByType(lib cell view "schematic" "w")

; Add instances, wires, pins here
; dbCreateInst(...)
; dbCreateNet(...)
; dbCreatePin(...)

dbSave(cv)
dbClose(cv)
printf("Created %s/%s/%s\n" lib cell view)
```

---

## Next Steps

1. SSH into CMC Cloud with X11
2. Source Cadence scripts
3. Launch Virtuoso
4. Use Claude --print to generate SKILL scripts
5. Load scripts in CIW to create schematics
6. Run OCEAN simulations to verify
7. Build up the hierarchy

---

## System Info

- **Host:** CMC Cloud (Rocky Linux 8.10)
- **Shell:** tcsh (not bash)
- **Tools:** IC23.10.140, Spectre 23.10.802
- **User:** v71349
- **No sudo access**
