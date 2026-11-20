<#
.SYNOPSIS
Runs the speak-text window in a Linux container on a virtual display.
.DESCRIPTION
Builds the image from docker/gui-test.Dockerfile and runs the window test with
the repository mounted read-only and a results folder mounted read-write. The
window never opens on the host desktop. Writes window.log, window.png and
xvfb.log to build/gui-results.
.EXAMPLE
pwsh scripts/gui-test.ps1
#>
[CmdletBinding()]
param([string]$Results = (Join-Path $PSScriptRoot '../build/gui-results'))

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
New-Item -ItemType Directory -Force -Path $Results | Out-Null
$results = (Resolve-Path $Results).Path
docker build -q -t pdf-to-audiobook-gui -f (Join-Path $repo 'docker/gui-test.Dockerfile') $repo
docker run --rm -v "${repo}:/app:ro" -v "${results}:/results" pdf-to-audiobook-gui sh /app/docker/run-gui-test.sh /results
exit $LASTEXITCODE
