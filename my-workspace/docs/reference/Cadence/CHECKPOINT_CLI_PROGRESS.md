# Checkpoint: CLI Automation Progress

> Historical checkpoint (Dec 2024). Keep for traceability only.
> Current execution truth lives in `my-workspace/docs/vision.md`,
> `my-workspace/docs/DEVELOPMENT.md`, and `my-workspace/docs/STATUS.md`.

**Date:** Dec 19, 2024
**Status:** CLI path validated, hit GUI dependency issue. Claude Code installed but TUI broken.

---

## CMC Cloud Environment Details

### System Info
- **OS:** Rocky Linux 8.10 (Green Obsidian)
- **Kernel:** 4.18.0-553.27.1.el8_10.x86_64
- **Shell:** tcsh (`/bin/tcsh`) - NOT bash!
- **User:** v71349
- **No sudo access** - user-level installations only

### SSH Connection
```bash
ssh -Y -p 31487 v71349@130.15.52.59
# Password provided per session via CMC cloud portal
```

### Shell Configuration (tcsh)
Create `~/.tcshrc`:
```tcsh
setenv TERM xterm-256color
setenv PATH "${HOME}/.local/bin:${PATH}"
```

---

## Claude Code Installation ✅

### Install Method (works without sudo)
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Installs to `~/.local/bin/claude` (symlink to `~/.local/share/claude/versions/2.0.74`)

### Interactive TUI Issue ❌
The interactive TUI launches but **exits immediately** due to raw mode issue:
```
ERROR Raw mode is not supported on the current process.stdin
```

**Tried and failed:**
- `bash -i` then `claude` - still exits
- `script -q -c claude /dev/null` - still exits
- Verified `stdin.isatty()` returns True
- Terminal is proper TTY (`/dev/pts/0`)
- `TERM=xterm-256color`
- No tmux/screen available on this system

### Workaround: Print Mode Works! ✅
```bash
claude --print "your prompt here"
claude --print --permission-mode acceptEdits "task with file access"
```

This enables agentic workflows (file read/write, bash commands) without the TUI.

---

## Cadence Environment Setup

```bash
source /CMC/scripts/cadence.ic23.10.140.csh
source /CMC/scripts/cadence.spectre23.10.802.csh
```

### Tools Verified
- `which ocean` → `/CMC/tools/cadence/IC23.10.140_lnx86/tools.lnx86/dfII/bin/ocean`
- `which spectre` → `/CMC/tools/cadence/SPECTRE23.10.802_lnx86/tools.lnx86/bin/spectre`
- `which virtuoso` → available after sourcing

### OCEAN Interactive Mode Works
```bash
ocean -nograph
> 1 + 1
2
> printf("hello\n")
hello
> exit()
```

---

## Library Setup

### Your Library
- **Original name:** `mani#2dtest` (URL-encoded dash)
- **Renamed to:** `inverter` at `/home/v71349/inverter`
- Contains: `inverter/inverter/schematic/` (manually created CMOS inverter)

### Rename Command Used
```bash
mv ~/mani#2dtest ~/inverter
sed -i 's/mani#2dtest/inverter/g' ~/cds.lib
```

### analogLib Location
```
/CMC/tools/cadence/IC23.10.140_lnx86/tools/dfII/etc/cdslib/artist/analogLib
```

Contains: `nmos4`, `pmos4`, `vdc`, `gnd`, `vpulse`, `res`, `cap`, etc.

### cds.lib Configuration
```bash
cat ~/cds.lib
```
```
SOFTINCLUDE /CMC/tools/cadence/IC23.10.140_lnx86/share/cdssetup/cds.lib
DEFINE inverter /home/v71349/inverter
```

**Note:** Don't add `DEFINE analogLib` - it's already included via SOFTINCLUDE and causes duplicate warning.

---

## What's NOT Working ❌

### SKILL Script Execution via OCEAN (Headless)
When running SKILL scripts that create schematics via `ocean -nograph`, ocean crashes:

```
IO Error 11 (Resource temporarily unavailable) on Display ":4621"
Aborting due to fatal X IO error.
*WARNING* Process was terminated with SIGABRT signal
```

**Root cause:** `dbOpenCellViewByType` and schematic creation still require X11 display even in "nograph" mode.

### The Failed Script
```lisp
lib = "inverter"
cell = "nand2"
view = "schematic"
cv = dbOpenCellViewByType(lib cell view "schematic" "w")
; ... dbCreateInst calls ...
dbSave(cv)
dbClose(cv)
```

This creates a panic file at `~/inverter/nand2/schematic/sch.oa-`

---

## Next Steps: Try GUI Approach

### Option 1: Run via Virtuoso GUI
1. SSH with X11 forwarding: `ssh -Y -p 31487 v71349@130.15.52.59`
2. Source scripts
3. Launch `virtuoso &`
4. In CIW, run: `load("/home/v71349/create_nand.il")`

### Option 2: Virtuoso Batch Mode with Display
```bash
export DISPLAY=:0  # or appropriate display
virtuoso -nograph -replay create_nand.il
```

### Option 3: Use Socket IPC
Start Virtuoso with a SKILL server socket, then send commands from external process.

---

## Cleanup Commands (if needed)
```bash
rm -rf ~/inverter/nand2
rm ~/panic.log.*
echo 'SOFTINCLUDE /CMC/tools/cadence/IC23.10.140_lnx86/share/cdssetup/cds.lib
DEFINE inverter /home/v71349/inverter' > ~/cds.lib
```

---

## The Goal We're Working Toward

**Agent Loop:**
1. Decompose "GPU core" → dependency tree
2. Build each component bottom-up (transistors → gates → adders → ALU)
3. Test each component via OCEAN/Spectre simulation
4. Save verified components to library
5. Compose into final design

**MCP Toolset Needed:**
- `create_schematic(name, skill_code)` → builds in Virtuoso
- `run_simulation(name, test_vectors)` → returns PASS/FAIL
- `save_to_library(name, interface)` → persist verified component

---

## Key Insight

The CLI-only path via `ocean -nograph` doesn't fully work for schematic creation because Cadence's database operations have hidden X11 dependencies.

**Two viable paths forward:**
1. **GUI-assisted:** Run Virtuoso with X11, load SKILL scripts via CIW
2. **Headless with virtual display:** Use Xvfb to provide a dummy X11 display

The simulation/verification part (OCEAN + Spectre) should work headlessly once the schematics exist.
