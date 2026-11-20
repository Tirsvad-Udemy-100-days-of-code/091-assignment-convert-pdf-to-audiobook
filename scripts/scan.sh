#!/usr/bin/env bash
# Runs the opengrep security scan on the repository. Run it before every push.
# Rule sets: p/secrets and p/python (fetched from the rule registry).
# Usage:  bash scripts/scan.sh
# Env:    OPENGREP  path of the binary (default ~/.opengrep/cli/latest/opengrep.exe)
# Exit:   0 no finding; non-zero a finding or a setup problem
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
opengrep="${OPENGREP:-$HOME/.opengrep/cli/latest/opengrep.exe}"

if [[ ! -x "$opengrep" ]]; then
  echo "opengrep not found at $opengrep" >&2
  exit 2
fi

cd "$root"
"$opengrep" scan --config p/secrets --config p/python --error --quiet \
  --exclude framework --exclude .venv --exclude .env --exclude docs/doxygen .
echo "opengrep: 0 findings"
