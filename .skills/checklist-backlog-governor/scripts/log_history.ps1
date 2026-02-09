param(
    [string]$ProjectRoot = ".",
    [string]$FileName = "Checklist & backlog.md",
    [string]$Bucket = "CHECKLIST",
    [string]$StepId = "",
    [string]$Status = "",
    [Parameter(Mandatory = $true)]
    [string]$Entry
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Status {
    param(
        [ValidateSet("INFO", "OK", "FAIL")]
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

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$targetPath = Join-Path $root $FileName

if (-not (Test-Path -LiteralPath $targetPath)) {
    Fail "Không tìm thấy file SSOT: $targetPath"
}

$content = Get-Content -LiteralPath $targetPath -Raw
if ($content -notmatch [regex]::Escape("## 5. Lịch sử thay đổi")) {
    Fail "File SSOT thiếu section '## 5. Lịch sử thay đổi'."
}

$bucketRaw = ""
if ($null -ne $Bucket) {
    $bucketRaw = [string]$Bucket
}
$bucketUpper = $bucketRaw.Trim().ToUpperInvariant()
if ([string]::IsNullOrWhiteSpace($bucketUpper)) {
    $bucketUpper = "CHECKLIST"
}

$stepRaw = ""
if ($null -ne $StepId) {
    $stepRaw = [string]$StepId
}
$step = $stepRaw.Trim()
if ([string]::IsNullOrWhiteSpace($step)) {
    $step = "-"
}

$stateRaw = ""
if ($null -ne $Status) {
    $stateRaw = [string]$Status
}
$state = $stateRaw.Trim().ToUpperInvariant()
if ([string]::IsNullOrWhiteSpace($state)) {
    $state = "-"
}

$text = $Entry.Trim()
if ([string]::IsNullOrWhiteSpace($text)) {
    Fail "Entry không được để trống."
}

$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$line = "- $stamp | $bucketUpper | $step | $state | $text"

Add-Content -LiteralPath $targetPath -Value $line -Encoding UTF8

Write-Status -Level "OK" -Message "Đã ghi lịch sử vào: $targetPath"
Write-Host $line
exit 0
