param(
    [string]$ProjectRoot = ".",
    [string]$Version = "",
    [switch]$RequireInstaller
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

function Read-TrimmedText {
    param([string]$Path)
    return ((Get-Content -LiteralPath $Path -Raw).Trim())
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

function Assert-VersionFormat {
    param(
        [string]$Value,
        [string]$Label
    )
    if ($Value -notmatch '^\d+\.\d+\.\d+$') {
        Fail "$Label must match x.y.z format. Received: $Value"
    }
    Write-Status -Level "OK" -Message "$Label format is valid: $Value"
}

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
Write-Status -Level "INFO" -Message "Project root: $root"

$versionFile = Join-Path $root "VERSION.txt"
Assert-Exists -Path $versionFile -Label "VERSION.txt"
$sourceVersion = Read-TrimmedText -Path $versionFile
if ([string]::IsNullOrWhiteSpace($sourceVersion)) {
    Fail "VERSION.txt is empty."
}
Assert-VersionFormat -Value $sourceVersion -Label "VERSION.txt"

if ([string]::IsNullOrWhiteSpace($Version)) {
    $targetVersion = $sourceVersion
    Write-Status -Level "INFO" -Message "Target version not provided; using VERSION.txt ($targetVersion)."
} else {
    $targetVersion = $Version.Trim()
    Assert-VersionFormat -Value $targetVersion -Label "Input -Version"
}

if ($targetVersion -ne $sourceVersion) {
    Fail "Input -Version ($targetVersion) does not match VERSION.txt ($sourceVersion)."
}

$buildExe = Join-Path $root "dist\DocCompareAI\DocCompareAI.exe"
Assert-Exists -Path $buildExe -Label "Build output executable"

$distVersionFile = Join-Path $root "dist\DocCompareAI\VERSION.txt"
Assert-Exists -Path $distVersionFile -Label "dist VERSION.txt"
$distVersion = Read-TrimmedText -Path $distVersionFile
if ($distVersion -ne $sourceVersion) {
    Fail "dist VERSION mismatch. dist=$distVersion, source=$sourceVersion"
}
Write-Status -Level "OK" -Message "dist VERSION matches source version."

$publishScript = Join-Path $root "publish_release.bat"
Assert-Exists -Path $publishScript -Label "publish_release.bat"

$workflowDoc = Join-Path $root "docs\UPDATE_WORKFLOW.md"
if (Test-Path -LiteralPath $workflowDoc) {
    Write-Status -Level "OK" -Message "Workflow doc found: $workflowDoc"
} else {
    Write-Status -Level "WARN" -Message "Workflow doc not found: $workflowDoc"
}

$changelogPath = Join-Path $root ("changelog\{0}.txt" -f $targetVersion)
if (Test-Path -LiteralPath $changelogPath) {
    Write-Status -Level "OK" -Message "Changelog found: $changelogPath"
} else {
    Write-Status -Level "WARN" -Message "Changelog missing for version ${targetVersion}: $changelogPath"
}

if ($RequireInstaller.IsPresent) {
    $installerPath = Join-Path $root ("installer\DocCompareAI_Setup_v{0}.exe" -f $targetVersion)
    Assert-Exists -Path $installerPath -Label "Installer"
} else {
    Write-Status -Level "INFO" -Message "Installer check skipped."
}

$localLatestPath = Join-Path $root "LATEST.txt"
if (Test-Path -LiteralPath $localLatestPath) {
    $localLatest = Read-TrimmedText -Path $localLatestPath
    if ([string]::IsNullOrWhiteSpace($localLatest)) {
        Write-Status -Level "WARN" -Message "Local LATEST.txt is empty."
    } elseif ($localLatest -ne $targetVersion) {
        Write-Status -Level "WARN" -Message "Local LATEST.txt points to $localLatest (target: $targetVersion)."
    } else {
        Write-Status -Level "OK" -Message "Local LATEST.txt matches target version."
    }
} else {
    Write-Status -Level "WARN" -Message "Local LATEST.txt not found."
}

Write-Status -Level "OK" -Message "Preflight passed. Ready to run publish flow."
exit 0
