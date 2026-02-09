param(
    [string]$ProjectRoot = ".",
    [string]$BackendDir = "backend",
    [switch]$RunCompile,
    [switch]$RunPytest
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
$backend = Join-Path $root $BackendDir
Write-Status -Level "INFO" -Message "Project root: $root"
Write-Status -Level "INFO" -Message "Backend dir: $backend"

Assert-Exists -Path $backend -Label "Backend directory"
Assert-Exists -Path (Join-Path $backend "main.py") -Label "main.py"
Assert-Exists -Path (Join-Path $backend "requirements.txt") -Label "requirements.txt"
Assert-Exists -Path (Join-Path $backend "routers\upload.py") -Label "upload router"
Assert-Exists -Path (Join-Path $backend "routers\compare.py") -Label "compare router"
Assert-Exists -Path (Join-Path $backend "routers\sheets.py") -Label "sheets router"
Assert-Exists -Path (Join-Path $backend "routers\analyze.py") -Label "analyze router"
Assert-Exists -Path (Join-Path $backend "core\engine.py") -Label "engine module"
Assert-Exists -Path (Join-Path $backend "core\reader.py") -Label "reader module"
Assert-Exists -Path (Join-Path $backend "core\ai.py") -Label "ai module"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "python command not found."
}
Write-Status -Level "OK" -Message "python command available."

$requirementsPath = Join-Path $backend "requirements.txt"
$requirementsText = Get-Content -LiteralPath $requirementsPath -Raw
foreach ($pkg in @("fastapi", "uvicorn", "pandas", "openpyxl")) {
    if ($requirementsText -match "(?im)^$pkg\s*$") {
        Write-Status -Level "OK" -Message "Requirement found: $pkg"
    } else {
        Write-Status -Level "WARN" -Message "Requirement missing in requirements.txt: $pkg"
    }
}

if ($RunCompile.IsPresent) {
    Write-Status -Level "INFO" -Message "Running compile check..."
    & python -m compileall $backend
    if ($LASTEXITCODE -ne 0) {
        Fail "Compile check failed."
    }
    Write-Status -Level "OK" -Message "Compile check passed."
} else {
    Write-Status -Level "INFO" -Message "Compile check skipped."
}

if ($RunPytest.IsPresent) {
    $pytestAvailable = Get-Command pytest -ErrorAction SilentlyContinue
    if (-not $pytestAvailable) {
        Write-Status -Level "WARN" -Message "pytest command not found; skipping tests."
    } else {
        Write-Status -Level "INFO" -Message "Running pytest for backend..."
        Push-Location $root
        try {
            & pytest backend -q
            if ($LASTEXITCODE -ne 0) {
                Fail "pytest failed."
            }
            Write-Status -Level "OK" -Message "pytest passed."
        } finally {
            Pop-Location
        }
    }
} else {
    Write-Status -Level "INFO" -Message "pytest check skipped."
}

Write-Status -Level "OK" -Message "Backend preflight passed."
exit 0
