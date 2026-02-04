# EDA License Unblock Investigation

- Date: 2026-02-03
- Host: `vcl-vm0-159`
- User: `v71349`
- Repo: `/home/v71349/analog-gradients`

## Executive Verdict

- **Cadence/Spectre (control): YES, works** (license checkout succeeds).
- **Synopsys DC: YES for license unblock today** (current failure is local config; once license env is set, `DCSH-1` disappears).  
  - After license unblock, a **non-license** blocker remains: `DB-1` (target `.lib` used where DC expects `.db`).
- **Siemens Calibre DRC: YES, can be unblocked today** (local config; with license env set, DRC licenses are acquired and run completes).

## 1) Baseline Environment + Script Wiring

### Baseline license env (current shell)
Command:
```bash
for v in LM_LICENSE_FILE CDS_LIC_FILE SNPSLMD_LICENSE_FILE MGLS_LICENSE_FILE; do echo "$v=${!v-<unset>}"; done
```
Key output:
```text
LM_LICENSE_FILE=<unset>
CDS_LIC_FILE=<unset>
SNPSLMD_LICENSE_FILE=<unset>
MGLS_LICENSE_FILE=<unset>
```

### Repo setup script behavior
- `setup_cadence.sh` sets Cadence license only when unset:
  - `CDS_LIC_FILE=6055@licaccess.cmc.ca`
- No equivalent Synopsys/Siemens export is done in `scripts/run_dc_smoke.sh` or `scripts/run_calibre_smoke.sh`.

### Relevant CMC license scripts
- `/CMC/scripts/synopsys.syn.2024.09-SP2.csh` -> sources `/CMC/tools/licenses/synopsys.csh`
- `/CMC/tools/licenses/synopsys.csh` -> `SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca`
- `/CMC/scripts/siemens.calibre.2025.4_24.aok.csh` -> sources Siemens base
- `/CMC/tools/licenses/mentor.csh` -> `MGLS_LICENSE_FILE=6056@licaccess.cmc.ca`

## 2) Tool Binary + License Smoke Checks

### Cadence/Spectre (control)
Command:
```bash
source setup_cadence.sh
spectre netlists/inverter.scs > /tmp/spectre_probe_inverter_20260203_140941.log 2>&1
```
Result: PASS (`rc=0`)
Key lines (`/tmp/spectre_probe_inverter_20260203_140941.log`):
```text
[14:09:41.367537] Periodic Lic check successful
spectre completes with 0 errors, 0 warnings, and 16 notices.
```

### Synopsys DC

#### A) Current repo-style run (no Synopsys license env)
Command:
```bash
unset SNPSLMD_LICENSE_FILE LM_LICENSE_FILE
export REPO_DIR=/home/v71349/analog-gradients
/CMC/tools/synopsys/syn_vW-2024.09-SP2/syn/W-2024.09-SP2/bin/dc_shell \
  -f implementation/fullflow_demo/scripts/dc_synth.tcl \
  > /tmp/dc_nosource_20260203_140957.log 2>&1
```
Result: FAIL (`rc=255`)
Exact error (`/tmp/dc_nosource_20260203_140957.log`):
```text
Fatal: Design Compiler is not enabled. (DCSH-1)
```

#### B) With Synopsys license setup (via CMC script)
Command:
```bash
tcsh -fc 'source /CMC/scripts/synopsys.syn.2024.09-SP2.csh; \
  setenv REPO_DIR /home/v71349/analog-gradients; \
  /CMC/tools/synopsys/syn_vW-2024.09-SP2/syn/W-2024.09-SP2/bin/dc_shell \
  -f /home/v71349/analog-gradients/implementation/fullflow_demo/scripts/dc_synth.tcl' \
  > /tmp/dc_synth_with_source_20260203_140822.log 2>&1
```
Result: license-unblocked (`rc=0`, no `DCSH-1`)
New non-license error (`/tmp/dc_synth_with_source_20260203_140822.log`):
```text
Error: File is not a DB file. (DB-1)
Error: The file '.../slow_vdd1v0_basicCells.lib' is not a DB file.
```

#### C) With env-only (bash-friendly) license fix
Command:
```bash
export SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca
export REPO_DIR=/home/v71349/analog-gradients
/CMC/tools/synopsys/syn_vW-2024.09-SP2/syn/W-2024.09-SP2/bin/dc_shell \
  -f implementation/fullflow_demo/scripts/dc_synth.tcl \
  > /tmp/dc_envonly_20260203_141859.log 2>&1
```
Result: same as (B): no `DCSH-1`; now blocked by `DB-1` library-format issue.

### Siemens Calibre DRC

#### A) Current repo-style run (no Siemens license env)
Command:
```bash
unset MGLS_LICENSE_FILE SALT_LICENSE_SERVER LM_LICENSE_FILE
/CMC/tools/siemens/aok_cal_2025.4_24/bin/calibre -drc -hier /tmp/calibre_nosource_20260203_140959.svrf \
  > /tmp/calibre_nosource_20260203_140959.log 2>&1
```
Result: FAIL (`rc=1`)
Exact errors (`/tmp/calibre_nosource_20260203_140959.log`):
```text
No license file variables are set.
Unable to set the license server path. Licensing issues may occur.
ERROR: Unable to acquire the first license for one or more products
ERROR: The following products could not be licensed sufficiently:
ERROR: - DRC (Hierarchical)
```

#### B) With Siemens setup script sourced
Command:
```bash
tcsh -fc 'source /CMC/scripts/siemens.calibre.2025.4_24.aok.csh; \
  /CMC/tools/siemens/aok_cal_2025.4_24/bin/calibre -drc -hier /tmp/calibre_probe_20260203_140844.svrf' \
  > /tmp/calibre_probe_20260203_140844.log 2>&1
```
Result: PASS (`rc=0`)
Key licensing lines (`/tmp/calibre_probe_20260203_140844.log`):
```text
calibrehdrc license acquired.
calibredrc license acquired.
Licensed Products
- DRC (Hierarchical)
... CALIBRE::DRC-H COMPLETED ...
```

#### C) With env-only (bash-friendly) license fix
Command:
```bash
export MGLS_LICENSE_FILE=6056@licaccess.cmc.ca
export SALT_LICENSE_SERVER=$MGLS_LICENSE_FILE
/CMC/tools/siemens/aok_cal_2025.4_24/bin/calibre -drc -hier /tmp/calibre_envonly_20260203_141903.svrf \
  > /tmp/calibre_envonly_20260203_141903.log 2>&1
```
Result: PASS (`rc=0`)
Key lines (`/tmp/calibre_envonly_20260203_141903.log`):
```text
calibrehdrc license acquired.
calibredrc license acquired.
- DRC (Hierarchical)
```

## 3) Existing Project Evidence (as requested)

- DC log: `implementation/fullflow_demo/work/dc/dc_shell.log`
  - `Fatal: Design Compiler is not enabled. (DCSH-1)`
- Calibre log: `implementation/fullflow_demo/work/calibre/calibre_drc.log`
  - `No license file variables are set.`
  - `Unable to acquire the first license...`
  - Feature: `DRC (Hierarchical)`
- Evidence doc: `competition/full-flow-smoke-evidence.md`
  - Records DC blocked by `DCSH-1` and Calibre DRC license block.

## 4) Server/Connectivity Sanity

### TCP reachability checks
Command family: `timeout 3 bash -lc "</dev/tcp/HOST/PORT"`

- `licaccess.cmc.ca:6053` -> OPEN
- `licaccess.cmc.ca:6055` -> OPEN
- `licaccess.cmc.ca:6056` -> OPEN
- Alternative hostnames from old script comments (`lm-synopsys-01`, `lka-ic-01`, `lka-ic-02`) were not DNS-resolvable in this VM context.

### lmutil/lmstat availability
- `lmutil` is available in Siemens/Calibre tree (for example `/CMC/tools/siemens/aok_cal_2025.4_24/bin/lmutil`).
- `lmutil lmpath -status` after Siemens source shows vendor path set:
  - `mgls: 6056@licaccess.cmc.ca`

Note: direct feature checkout from tools (DC/Calibre runs above) is treated as higher-confidence evidence than generic `lmstat` output in this environment.

## 5) Root-Cause Classification

| Tool | Classification | Can unblock today? | Why |
|---|---|---|---|
| Synopsys DC license failure (`DCSH-1`) | **CONFIG issue** | **YES** | `DCSH-1` occurs when Synopsys license env is absent; disappears immediately when `SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca` is set. |
| Siemens Calibre DRC license failure | **CONFIG issue** | **YES** | Failure shows missing license vars; with `MGLS_LICENSE_FILE/SALT_LICENSE_SERVER` set to `6056@licaccess.cmc.ca`, Calibre acquires `calibrehdrc` + `calibredrc` and completes. |

### Important non-license follow-up
- DC currently hits `DB-1` with `slow_vdd1v0_basicCells.lib` (text `.lib` where DC expects `.db` in this flow script path). This is separate from licensing.

## Evidence Table

| Tool | Command run | Result | Exact error code/text | Likely cause |
|---|---|---|---|---|
| Spectre | `source setup_cadence.sh; spectre netlists/inverter.scs` | PASS | `Periodic Lic check successful` | Cadence license path configured correctly via repo setup |
| DC (no Synopsys env) | `dc_shell -f dc_synth.tcl` | FAIL | `Fatal: Design Compiler is not enabled. (DCSH-1)` | Missing `SNPSLMD_LICENSE_FILE` in stage environment |
| DC (with `SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca`) | same | license-unblocked | `DCSH-1` gone; next error `DB-1` | License fixed; now blocked by non-license library-format config |
| Calibre (no Siemens env) | `calibre -drc -hier <rule>` | FAIL | `No license file variables are set` + `Unable to acquire the first license` + `DRC (Hierarchical)` | Missing `MGLS_LICENSE_FILE`/`SALT_LICENSE_SERVER` |
| Calibre (with `MGLS_LICENSE_FILE=6056@licaccess.cmc.ca`) | same | PASS | `calibrehdrc license acquired` + `calibredrc license acquired` | Local env fix resolves license block |

## Exact Remediation Commands (config-fixable)

Use in current shell before running smoke/fullflow scripts:

```bash
export SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca
export MGLS_LICENSE_FILE=6056@licaccess.cmc.ca
export SALT_LICENSE_SERVER=$MGLS_LICENSE_FILE
```

Then run:

```bash
scripts/run_dc_smoke.sh
scripts/run_calibre_smoke.sh
```

(or `scripts/run_fullflow_smoke.sh` after exporting the same variables).

## Support Escalation Status

- **Entitlement/server-side block determination:** not indicated by current evidence for DC or Calibre.
- **CMC/admin request needed right now for licensing:** **No**, not for the observed failures.

If escalation is later needed (for example, if failures persist even with the env above), include:
- host/user/time: `vcl-vm0-159 / v71349 / 2026-02-03T19:21:43Z`
- tool versions: DC `W-2024.09-SP2`, Calibre `v2025.4_24.16`
- failing command + full log path + exact text from `/tmp/dc_nosource_20260203_140957.log` or `/tmp/calibre_nosource_20260203_140959.log`.
