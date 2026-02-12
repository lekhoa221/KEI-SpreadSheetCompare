param(
    [string]$ProjectRoot = ".",
    [string]$RemoteRoot = "\\10.1.3.2\KEIToolsData\SpreadSheetCompare",
    [switch]$RequireInstaller,
    [switch]$RequireRemoteRoot
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

$versionFile = Join-Path $root "VERSION.txt"
$publishScript = Join-Path $root "publish_release.bat"
$distExe = Join-Path $root "dist\DocCompareAI\DocCompareAI.exe"
$distVersionFile = Join-Path $root "dist\DocCompareAI\VERSION.txt"

Assert-Exists -Path $versionFile -Label "VERSION.txt"
Assert-Exists -Path $publishScript -Label "publish_release.bat"
Assert-Exists -Path $distExe -Label "dist executable"

$version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$') {
    Write-Status -Level "WARN" -Message "VERSION format is not x.y.z: $version"
} else {
    Write-Status -Level "OK" -Message "VERSION format looks valid: $version"
}

if (Test-Path -LiteralPath $distVersionFile) {
    $distVersion = (Get-Content -LiteralPath $distVersionFile -Raw).Trim()
    if ($distVersion -eq $version) {
        Write-Status -Level "OK" -Message "dist VERSION matches source VERSION."
    } else {
        Write-Status -Level "WARN" -Message "dist VERSION mismatch. dist=$distVersion source=$version"
    }
} else {
    Write-Status -Level "WARN" -Message "dist VERSION file missing: $distVersionFile"
}

$expectedInstaller = Join-Path $root ("installer\DocCompareAI_Setup_v{0}.exe" -f $version)
if (Test-Path -LiteralPath $expectedInstaller) {
    Write-Status -Level "OK" -Message "Installer found: $expectedInstaller"
} else {
    if ($RequireInstaller.IsPresent) {
        Fail "Required installer missing: $expectedInstaller"
    }
    Write-Status -Level "WARN" -Message "Installer missing: $expectedInstaller"
}

$changelogFile = Join-Path $root ("changelog\{0}.txt" -f $version)
if (Test-Path -LiteralPath $changelogFile) {
    Write-Status -Level "OK" -Message "Changelog found: $changelogFile"
} else {
    Write-Status -Level "WARN" -Message "Changelog missing for version $version"
}

if ([string]::IsNullOrWhiteSpace($RemoteRoot)) {
    Write-Status -Level "WARN" -Message "RemoteRoot is empty."
} else {
    if (Test-Path -LiteralPath $RemoteRoot) {
        Write-Status -Level "OK" -Message "Remote root reachable: $RemoteRoot"
    } else {
        if ($RequireRemoteRoot.IsPresent) {
            Fail "Required remote root not reachable: $RemoteRoot"
        }
        Write-Status -Level "WARN" -Message "Remote root not reachable: $RemoteRoot"
    }
}

$localReleaseRoot = Join-Path $root "releases"
if (Test-Path -LiteralPath $localReleaseRoot) {
    Write-Status -Level "OK" -Message "Local release root exists: $localReleaseRoot"
} else {
    Write-Status -Level "WARN" -Message "Local release root does not exist yet: $localReleaseRoot"
}

Write-Status -Level "OK" -Message "Publish preflight completed."
exit 0
