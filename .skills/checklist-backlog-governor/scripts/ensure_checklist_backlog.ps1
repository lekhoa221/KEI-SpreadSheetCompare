param(
    [string]$ProjectRoot = ".",
    [string]$FileName = "Checklist & backlog.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Status {
    param(
        [ValidateSet("INFO", "OK", "WARN", "FAIL", "ACTION")]
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
$templatePath = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\assets\checklist-backlog.template.md")).Path

Write-Status -Level "INFO" -Message "Project root: $root"
Write-Status -Level "INFO" -Message "Target SSOT: $targetPath"

if (-not (Test-Path -LiteralPath $templatePath)) {
    Fail "Template not found: $templatePath"
}

if (-not (Test-Path -LiteralPath $targetPath)) {
    $date = Get-Date -Format "yyyy-MM-dd"
    $time = Get-Date -Format "HH:mm:ss"
    $content = Get-Content -LiteralPath $templatePath -Raw
    $content = $content.Replace("{{DATE}}", $date).Replace("{{TIME}}", $time)

    [System.IO.File]::WriteAllText(
        $targetPath,
        $content,
        (New-Object System.Text.UTF8Encoding($false))
    )

    Write-Status -Level "WARN" -Message "File SSOT chưa tồn tại. Đã tạo mới: $targetPath"
    Write-Status -Level "ACTION" -Message "Prompt đầu tiên phải dừng tại đây và yêu cầu user xác nhận nội dung file trước khi làm task khác."
    exit 3
}

$requiredHeadings = @(
    "## 1. Quy ước sử dụng",
    "## 2. Danh sách thành phần trong bộ skill",
    "## 3. Checklist chính",
    "## 4. Backlog phụ trợ",
    "## 5. Lịch sử thay đổi"
)

$existing = Get-Content -LiteralPath $targetPath -Raw
$missingHeadings = @()

foreach ($heading in $requiredHeadings) {
    if ($existing -notmatch [regex]::Escape($heading)) {
        $missingHeadings += $heading
    }
}

if ($missingHeadings.Count -gt 0) {
    Write-Status -Level "FAIL" -Message "File SSOT thiếu section bắt buộc:"
    foreach ($h in $missingHeadings) {
        Write-Host " - $h"
    }
    exit 1
}

Write-Status -Level "OK" -Message "File SSOT hợp lệ và sẵn sàng: $targetPath"
exit 0
