# Cadence License Setup (CMC Cloud)

This repo expects the Cadence license environment to be configured on the CMC
host. If it is missing you will see:

```
lmStatus: ERROR (LMC-01902): License call failed.
The license server search path is defined as <none>.
Can't find license file.
```

## Quick Check

```bash
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "CDS_LIC_FILE=$CDS_LIC_FILE"
```

If both are empty, Spectre/Virtuoso cannot find a license.

## Common Fixes

### 1) Use CMC environment launcher

CMC often provides a wrapper that sets license variables. On the CMC host:

```bash
ls /CMC/scripts | grep '^cmc\.'
```

Then source the latest available CMC script (example):

```bash
source /CMC/scripts/cmc.2023.1.csh
```

Re-check the license vars after sourcing.

### 2) Ask CMC for the license server string

If the wrapper does not set it, CMC support can provide the license string.
Set it in your shell:

```bash
export LM_LICENSE_FILE="27000@license.server.example"
```

Some installations prefer `CDS_LIC_FILE`:

```bash
export CDS_LIC_FILE="27000@license.server.example"
```

CMC Cloud default (observed on this host):

```bash
export CDS_LIC_FILE="6055@licaccess.cmc.ca"
```

### 3) Check for a local license file

If CMC provides a file path (e.g., `/path/to/license.dat`), use:

```bash
export LM_LICENSE_FILE="/path/to/license.dat"
```

## Verify

After setting the license variable:

```bash
source setup_cadence.sh
./build.sh inverter
```

If the license is valid, Spectre should run and the build will proceed.
