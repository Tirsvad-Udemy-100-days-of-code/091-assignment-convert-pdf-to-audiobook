<#
.SYNOPSIS
    Runs the opengrep security scan on the repository. Run it before every push.

.DESCRIPTION
    Uses the rule sets p/secrets, p/python and p/security-audit, fetched from the rule registry,
    and fails (non-zero exit code) when a finding is reported. The framework
    submodule and the local .env file are not scanned.

.EXAMPLE
    pwsh scripts/scan.ps1
#>
[CmdletBinding()]
param(
    [string]$Opengrep = (Join-Path $HOME '.opengrep/cli/latest/opengrep.exe')
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot

if (-not (Test-Path $Opengrep)) {
    Write-Error "opengrep not found at $Opengrep"
    exit 2
}

Push-Location $root
try {
    & $Opengrep scan --config p/secrets --config p/python --config p/security-audit --error --quiet `
        --exclude framework --exclude .venv --exclude .env --exclude docs/doxygen .
    $code = $LASTEXITCODE
}
finally {
    Pop-Location
}

if ($code -eq 0) {
    Write-Host 'opengrep: 0 findings'
}
else {
    Write-Host "opengrep: findings or error (exit code $code)"
}
exit $code
