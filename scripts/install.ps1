$ErrorActionPreference = "Stop"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[windows,dev]"
Write-Host "Installed. Next run:"
Write-Host "  grok inspect"
Write-Host "  grok mcp doctor grok-computer-use"
Write-Host "  pytest -q"
