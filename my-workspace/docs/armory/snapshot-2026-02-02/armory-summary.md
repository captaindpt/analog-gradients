# EDA Armory Snapshot (2026-02-02)

- Host: `vcl-vm0-159`
- Repo: `/home/v71349/analog-gradients`
- Snapshot UTC: `2026-02-02T16:30:07.156226Z`

## Vendor Tool Inventory
- **BEEcube**: 2 entries
- **COMSOL**: 8 entries
- **Coventor**: 0 entries
- **Matlab**: 1 entries
- **altera**: 1 entries
- **ansys**: 8 entries
- **cadence**: 232 entries
- **intel**: 1 entries
- **keysight**: 18 entries
- **licenses**: 16 entries
- **lumerical**: 2 entries
- **mentor**: 69 entries
- **siemens**: 13 entries
- **synopsys**: 162 entries
- **xilinx**: 8 entries

## Script Prefix Counts (/CMC/scripts)
- **agilent**: 15 scripts
- **ansys**: 11 scripts
- **cadence**: 523 scripts
- **intel**: 4 scripts
- **keysight**: 24 scripts
- **mentor**: 101 scripts
- **siemens**: 14 scripts
- **synopsys**: 169 scripts
- **xilinx**: 15 scripts

## Kits
- Total `/CMC/kits` entries: 40
- Cadence generic kits include ADVGPDK, GPDK045, GPDK090, GPDK180 (see `raw/cadence_kits_tree.txt`).

## Notable Live Checks
- `cadence_local_setup`: rc=0 virtuoso=/CMC/tools/cadence/IC23.10.140_lnx86/tools.lnx86/dfII/bin/virtuoso
- `cadence_xcelium`: rc=0 /CMC/tools/cadence/XCELIUMMAIN25.09.001_lnx86/tools.lnx86/bin/xrun
- `cadence_innovus`: rc=0 /CMC/tools/cadence/INNOVUS21.17.000_lnx86/tools.lnx86/bin/innovus
- `cadence_pegasus`: rc=141 /CMC/tools/cadence/PEGASUS23.26.000_lnx86/tools.lnx86/bin/pegasus
- `synopsys_vcs_verdi`: rc=0 /CMC/tools/synopsys/vcs_vW-2024.09-SP1/vcs/W-2024.09-SP1/bin/vcs
- `synopsys_dc_shell`: rc=0 /CMC/tools/synopsys/syn_vW-2024.09-SP2/syn/W-2024.09-SP2/bin/dc_shell
- `synopsys_hspice_script`: rc=1 hspice: Command not found.
- `synopsys_hspice_direct`: rc=0   HSPICE Version V-2023.12 linux64 (Nov 17 2023 8561338)
- `siemens_questa`: rc=0 /CMC/tools/siemens/questasim_2025.2_2/questasim/bin/vsim
- `siemens_calibre`: rc=0 /CMC/tools/siemens/aok_cal_2025.4_24/bin/calibre
- `xilinx_vivado`: rc=0 /CMC/tools/xilinx/2025.2/2025.2/Vivado/bin/vivado
- `intel_quartus`: rc=0 /CMC/tools/intel/intelFPGA_pro/25.3/quartus/bin/quartus_sh
- `keysight_ads`: rc=141 /CMC/tools/keysight/ADS2026U0.1/bin/ads
- `ansys_tools`: rc=0 /CMC/tools/ansys/ansys.2025r2/ansys_inc/v252/AnsysEM/ansysedt

## Known Caveats
- `synopsys.hspice.2023.12.csh` failed in this shell context because `/usr/sbin/lsof` is missing; direct HSPICE binary works.
- Jasper 23.09 works with `jg -allow_unsupported_OS`; newer 24.09 script has restrictive file permissions for this user.
- No `module` command detected; this environment relies on `/CMC/scripts/*.csh` setup scripts.

## File Index
- `inventory.json` (structured snapshot)
- `raw/tools/*.txt` (full vendor entries)
- `raw/scripts/*.txt` (full setup script lists by prefix)
- `raw/live_checks.txt` (all command outputs)
- `raw/repo_setup_cadence.sh`, `raw/repo_build.sh` (project setup flow)
- `raw/licenses_ls.txt`, `raw/license_scripts.txt` (license wiring)
- `raw/kits.txt`, `raw/cadence_kits_tree.txt` (PDK/kit inventory)
