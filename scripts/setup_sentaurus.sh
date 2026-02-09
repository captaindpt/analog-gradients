#!/usr/bin/env bash
# Sentaurus TCAD environment setup for bash.
# Source this: source scripts/setup_sentaurus.sh
#
# Sentaurus ships with a tcsh setup script. This wrapper extracts the
# key environment variables and sets them in the current bash shell.

export CMC_HOME="${CMC_HOME:-/CMC}"

# Use latest available Sentaurus version
export STROOT="${CMC_HOME}/tools/synopsys/sentaurus_vX_2025.09/sentaurus"

if [[ ! -d "$STROOT/bin" ]]; then
  echo "ERROR: Sentaurus not found at $STROOT" >&2
  return 1 2>/dev/null || exit 1
fi

# Synopsys license (same server as other Synopsys tools)
export SNPSLMD_LICENSE_FILE="${SNPSLMD_LICENSE_FILE:-6053@licaccess.cmc.ca}"

# Add Sentaurus binaries to PATH (prepend so they take priority)
case ":$PATH:" in
  *":$STROOT/bin:"*) ;;
  *) export PATH="$STROOT/bin:$PATH" ;;
esac

echo "Sentaurus TCAD vX-2025.09 ready"
echo "  sde:     $(which sde 2>/dev/null || echo 'not found')"
echo "  snmesh:  $(which snmesh 2>/dev/null || echo 'not found')"
echo "  sdevice: $(which sdevice 2>/dev/null || echo 'not found')"
echo "  svisual: $(which svisual 2>/dev/null || echo 'not found')"
echo "  license: SNPSLMD_LICENSE_FILE=${SNPSLMD_LICENSE_FILE}"
