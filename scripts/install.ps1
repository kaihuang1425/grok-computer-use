$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvPath = Join-Path $RepoRoot ".venv"
$Python = Join-Path $VenvPath "Scripts\python.exe"

Push-Location $RepoRoot
try {
    if (-not (Test-Path $Python)) {
        python -m venv $VenvPath
    }

    & $Python -m pip install --upgrade pip
    & $Python -m pip install -e ".[windows,dev]"
    & $Python -m pip check

    Write-Host ""
    Write-Host "Installed Grok Computer Use in: $VenvPath"
    Write-Host "Next run:"
    Write-Host "  grok inspect"
    Write-Host "  grok mcp doctor grok-computer-use"
    Write-Host "  .\.venv\Scripts\python.exe -m pytest -q"
} finally {
    Pop-Location
}
