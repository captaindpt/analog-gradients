# Cadence Virtuoso Setup Guide (Mac via CMC Cloud)

This guide documents the working steps to access Cadence Virtuoso on a Mac through CMC Microsystems cloud.

## Prerequisites

- CMC Microsystems membership (through University of Guelph)
- XQuartz installed (`brew install --cask xquartz`)
- NoMachine Enterprise Client (optional, may not work on macOS 26+)

---

## Step 1: Access CMC Cloud

1. Go to [CMC Microsystems](https://www.cmc.ca)
2. Navigate to **CAD → Cadence University Software**
3. Click on **CMC Cloud Quick Start Guides**
4. Select **Quick Start Guide: Using CMC Cloud VCAD Design Environments**
5. Create/manage your cloud instance

---

## Step 2: Fix XQuartz for X11 Forwarding (macOS 26+)

XQuartz has issues on macOS 26 Tahoe. Run this to reset everything:

```bash
# Kill XQuartz and clean stale files
pkill -9 X11
rm -f /tmp/.X*-lock /tmp/.X11-unix/* ~/.Xauthority

# Restart XQuartz
open -a XQuartz

# Wait a few seconds, then verify
/opt/X11/bin/xauth list
# Should show: mani-mac/unix:0  MIT-MAGIC-COOKIE-1  <cookie>
```

### Add to Shell Profile

Add this to `~/.zshrc`:
```bash
export DISPLAY=:0
```

---

## Step 3: Connect to CMC Cloud Instance

Your instance will provide connection details like:
- **Host**: `130.15.52.59`
- **Port**: `31487` (SSH) or `39044` (NoMachine)
- **User**: `v71349` (example)
- **Password**: provided per session

### Connect via SSH with X11 Forwarding

```bash
export DISPLAY=:0
ssh -Y -p <SSH_PORT> <USER>@<HOST>
```

Example:
```bash
ssh -Y -p 31487 v71349@130.15.52.59
```

### Test X11 Works

On the remote machine:
```bash
xterm &
```

A terminal window should appear on your Mac.

---

## Step 4: Launch Cadence Virtuoso

### Source the Cadence Environment

```bash
source /CMC/scripts/cadence.ic23.10.140.csh
```

Available versions can be found with:
```bash
ls /CMC/scripts | grep cadence.ic
```

### Launch Virtuoso

```bash
virtuoso &
```

The Virtuoso GUI (CIW - Command Interpreter Window) will open.

---

## Step 5: Create Your First Library

1. In CIW menu: **File → New → Library**
2. Name it (e.g., `mani-test`)
3. When asked about technology file: **Attach to existing tech library → analogLib**

---

## Step 6: Create a Schematic (Inverter Example)

1. **File → New → Cell View**
   - Library: `mani-test`
   - Cell: `inverter`
   - View: `schematic`

2. Press **`i`** (instance) to place components:
   - Library: `analogLib`, Cell: `nmos4`, View: `symbol`
   - Library: `analogLib`, Cell: `pmos4`, View: `symbol`

3. Press **`w`** (wire) to connect:
   - PMOS drain → NMOS drain (output)
   - PMOS gate → NMOS gate (input)
   - PMOS source → VDD
   - NMOS source → GND
   - PMOS bulk → VDD
   - NMOS bulk → GND

4. Press **`p`** (pin) to add ports:
   - VDD (inputOutput)
   - GND (inputOutput)
   - IN (input)
   - OUT (output)

5. **Ctrl+S** to save

---

## Troubleshooting

### License error (LMC-01902)

If Spectre reports `LMC-01902` (license search path <none>), follow:
`my-workspace/docs/reference/Cadence/LICENSE_SETUP.md`.

### "No xauth data" or "Invalid MIT-MAGIC-COOKIE-1"

Reset XQuartz:
```bash
pkill -9 X11
rm -f /tmp/.X*-lock /tmp/.X11-unix/* ~/.Xauthority
open -a XQuartz
sleep 3
export DISPLAY=:0
```

### NoMachine doesn't work on macOS 26

Use SSH with X11 forwarding instead (see Step 3).

### License checkout fails

If you see license errors, click **"Session"** to use an alternative license tier (XL vs L).

---

## Useful Paths on CMC Cloud

| Path | Description |
|------|-------------|
| `/CMC/scripts/` | Setup scripts for all tools |
| `/CMC/tools/cadence/` | Cadence installations |
| `/CMC/tools/synopsys/` | Synopsys installations |
| `/CMC/kits/` | Process Design Kits (PDKs) |

---

## SKILL Scripting (Automation)

Everything in Virtuoso can be automated via SKILL (Lisp-based scripting).

Example - open a cell programmatically:
```lisp
dbOpenCellViewByType("mani-test" "inverter" "schematic")
```

Example - create an instance:
```lisp
schCreateInst(cellView "analogLib" "nmos4" "symbol" x:y "R0")
```

---

## Contact for On-Campus Access

**Bogdan Bunescu** - IT Manager, College of Engineering
- Thornbrough Building, Room 1416
- Phone: 519-824-4120 Ext. 56713
- Email: bbunescu@uoguelph.ca

Ask about Linux workstations with Cadence or who the STC administrator is.

---

## Future Vision: AI-Driven Chip Design

The goal is to build an MCP toolset that:
1. Takes high-level specs (e.g., "Build a 4-core GPU with 8-bit MAC units")
2. Generates DSL intermediate representation
3. Compiles to SKILL code
4. Executes in Virtuoso (creates schematics/layouts automatically)
5. Runs simulations and returns results

Demo prompt:
> "Create a 2-input NAND gate using CMOS logic. Use minimum-size transistors. Connect it to VDD and GND. Then create a testbench that applies all four input combinations and simulates the output."
