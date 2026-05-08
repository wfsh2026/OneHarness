$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
Write-Host "============================================================"
Write-Host " Unity UI Auto Slicer v2 - no cv2 / OpenCV"
Write-Host "============================================================"

$pyCmd = $null
try {
    & py -3 --version | Out-Null
    $pyCmd = "py -3"
} catch {}

if (-not $pyCmd) {
    try {
        & python --version | Out-Null
        $pyCmd = "python"
    } catch {}
}

if (-not $pyCmd) {
    Write-Host "Python 3 was not found. Download Python from: https://www.python.org/downloads/"
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating local Python environment..."
    if ($pyCmd -eq "py -3") { & py -3 -m venv .venv } else { & python -m venv .venv }
}

$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
Write-Host "Installing/updating Pillow..."
& $py -m pip install --upgrade pip | Out-Null
& $py -m pip install --upgrade pillow
& $py (Join-Path $PSScriptRoot "unity_ui_auto_slicer.py")
Read-Host "Press Enter to exit"
