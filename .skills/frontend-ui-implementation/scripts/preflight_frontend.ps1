param(
    [string]$ProjectRoot = ".",
    [string]$FrontendDir = "frontend",
    [switch]$RunLint,
    [switch]$RunBuild
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
$front = Join-Path $root $FrontendDir
Write-Status -Level "INFO" -Message "Project root: $root"
Write-Status -Level "INFO" -Message "Frontend dir: $front"

Assert-Exists -Path $front -Label "Frontend directory"

$packageJsonPath = Join-Path $front "package.json"
Assert-Exists -Path $packageJsonPath -Label "package.json"

$packageJson = Get-Content -LiteralPath $packageJsonPath -Raw | ConvertFrom-Json
if (-not $packageJson.scripts) {
    Fail "package.json has no scripts section."
}

foreach ($scriptName in @("dev", "build", "lint")) {
    if (-not $packageJson.scripts.$scriptName) {
        Write-Status -Level "WARN" -Message "package.json missing script: $scriptName"
    } else {
        Write-Status -Level "OK" -Message "Script found: $scriptName"
    }
}

foreach ($depName in @("react", "react-dom", "axios")) {
    $hasDep = $false
    if ($packageJson.dependencies -and $packageJson.dependencies.PSObject.Properties.Name -contains $depName) {
        $hasDep = $true
    }
    if ($hasDep) {
        Write-Status -Level "OK" -Message "Dependency found: $depName"
    } else {
        Write-Status -Level "WARN" -Message "Dependency not found in package.json dependencies: $depName"
    }
}

Assert-Exists -Path (Join-Path $front "vite.config.js") -Label "vite config"
Assert-Exists -Path (Join-Path $front "src/main.jsx") -Label "main entry"
Assert-Exists -Path (Join-Path $front "src/App.jsx") -Label "app root"
Assert-Exists -Path (Join-Path $front "src/index.css") -Label "global css"

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Fail "npm command not found. Install Node.js/npm first."
}

Push-Location $front
try {
    if ($RunLint.IsPresent) {
        Write-Status -Level "INFO" -Message "Running lint..."
        & npm run lint
        if ($LASTEXITCODE -ne 0) {
            Fail "Lint failed."
        }
        Write-Status -Level "OK" -Message "Lint passed."
    } else {
        Write-Status -Level "INFO" -Message "Lint check skipped."
    }

    if ($RunBuild.IsPresent) {
        Write-Status -Level "INFO" -Message "Running build..."
        & npm run build
        if ($LASTEXITCODE -ne 0) {
            Fail "Build failed."
        }
        Write-Status -Level "OK" -Message "Build passed."
    } else {
        Write-Status -Level "INFO" -Message "Build check skipped."
    }
}
finally {
    Pop-Location
}

Write-Status -Level "OK" -Message "Frontend preflight passed."
exit 0
