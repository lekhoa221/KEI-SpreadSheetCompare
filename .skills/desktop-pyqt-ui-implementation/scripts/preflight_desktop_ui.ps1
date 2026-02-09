param(
    [string]$ProjectRoot = ".",
    [switch]$VerifyQtImports,
    [switch]$RunCompile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Status {
    param(
        [ValidateSet("INFO", "OK", "WARN", "FAIL")]
        [string]$Level,
        [string]$Message
    )
    Write-Host "[$Level] $Message"
}

function Fail {
    param([string]$Message)
    Write-Status -Level "FAIL" -Message $Message
    exit 1
}

function Assert-Exists {
    param(
        [string]$Path,
        [string]$Label
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        Fail "$Label not found: $Path"
    }
    Write-Status -Level "OK" -Message "$Label found: $Path"
}

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
Write-Status -Level "INFO" -Message "Project root: $root"

Assert-Exists -Path (Join-Path $root "desktop_app.py") -Label "desktop app entry"
Assert-Exists -Path (Join-Path $root "run_desktop.bat") -Label "desktop run script"
Assert-Exists -Path (Join-Path $root "ui\main_window.py") -Label "main window"
Assert-Exists -Path (Join-Path $root "ui\file_drop.py") -Label "file drop widget"
Assert-Exists -Path (Join-Path $root "ui\excel\result_view.py") -Label "result view"
Assert-Exists -Path (Join-Path $root "core\config.py") -Label "desktop config"
Assert-Exists -Path (Join-Path $root "core\version.py") -Label "version module"
Assert-Exists -Path (Join-Path $root "core\update_manager.py") -Label "update manager"
Assert-Exists -Path (Join-Path $root "core\feedback_manager.py") -Label "feedback manager"

$logoPath = Join-Path $root "ui\logo.png"
if (Test-Path -LiteralPath $logoPath) {
    Write-Status -Level "OK" -Message "Logo asset found: $logoPath"
} else {
    Write-Status -Level "WARN" -Message "Logo asset not found: $logoPath"
}

$iconDir = Join-Path $root "ui\assets\icons"
if (Test-Path -LiteralPath $iconDir) {
    $iconCount = (Get-ChildItem -LiteralPath $iconDir -File | Measure-Object).Count
    if ($iconCount -gt 0) {
        Write-Status -Level "OK" -Message "Icon assets found: $iconCount files"
    } else {
        Write-Status -Level "WARN" -Message "Icon directory is empty: $iconDir"
    }
} else {
    Write-Status -Level "WARN" -Message "Icon directory not found: $iconDir"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "python command not found."
}
Write-Status -Level "OK" -Message "python command available."

if ($VerifyQtImports.IsPresent) {
    Write-Status -Level "INFO" -Message "Verifying PyQt and qdarktheme imports..."
    & python -c "import PyQt6; import qdarktheme"
    if ($LASTEXITCODE -ne 0) {
        Fail "PyQt6 or qdarktheme import failed."
    }
    Write-Status -Level "OK" -Message "PyQt6 and qdarktheme imports passed."
} else {
    Write-Status -Level "INFO" -Message "Qt import verification skipped."
}

if ($RunCompile.IsPresent) {
    Write-Status -Level "INFO" -Message "Running compile check..."
    & python -m compileall (Join-Path $root "desktop_app.py") (Join-Path $root "ui") (Join-Path $root "core")
    if ($LASTEXITCODE -ne 0) {
        Fail "Compile check failed."
    }
    Write-Status -Level "OK" -Message "Compile check passed."
} else {
    Write-Status -Level "INFO" -Message "Compile check skipped."
}

Write-Status -Level "OK" -Message "Desktop UI preflight passed."
exit 0
