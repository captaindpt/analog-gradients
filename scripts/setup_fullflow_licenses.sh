#!/usr/bin/env bash
set -euo pipefail

# Defaults observed on CMC host vcl-vm0-159 (2026-02-03).
DEFAULT_SNPS="6053@licaccess.cmc.ca"
DEFAULT_MGLS="6056@licaccess.cmc.ca"

if [[ -z "${SNPSLMD_LICENSE_FILE:-}" ]]; then
    export SNPSLMD_LICENSE_FILE="$DEFAULT_SNPS"
fi

if [[ -z "${MGLS_LICENSE_FILE:-}" ]]; then
    export MGLS_LICENSE_FILE="$DEFAULT_MGLS"
fi

if [[ -z "${SALT_LICENSE_SERVER:-}" ]]; then
    export SALT_LICENSE_SERVER="$MGLS_LICENSE_FILE"
fi

if [[ "${FULLFLOW_LICENSE_VERBOSE:-1}" == "1" ]]; then
    echo "License env:"
    echo "  SNPSLMD_LICENSE_FILE=$SNPSLMD_LICENSE_FILE"
    echo "  MGLS_LICENSE_FILE=$MGLS_LICENSE_FILE"
    echo "  SALT_LICENSE_SERVER=$SALT_LICENSE_SERVER"
fi
