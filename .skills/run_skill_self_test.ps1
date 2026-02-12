param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName,
    [string]$ProjectRoot = ".",
    [string]$OutputDir = "temp",
    [switch]$Strict
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

function Convert-OutputToText {
    param([object[]]$OutputLines)
    if ($null -eq $OutputLines) {
        return ""
    }
    return (($OutputLines | ForEach-Object { $_.ToString() }) -join "`n")
}

function Invoke-ProbeStep {
    param(
        [string]$Name,
        [string]$ScriptPath,
        [string[]]$Arguments,
        [int[]]$AcceptExitCodes = @(0)
    )

    if (-not (Test-Path -LiteralPath $ScriptPath)) {
        $msg = "Probe script not found: $ScriptPath"
        $script:ProbeResults += [pscustomobject]@{
            Name     = $Name
            Command  = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" " + ($Arguments -join " ")
            ExitCode = -1
            Status   = "FAIL"
            Output   = $msg
        }
        $script:HasFailure = $true
        Write-Status -Level "FAIL" -Message $msg
        return
    }

    $cmdText = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" " + ($Arguments -join " ")
    Write-Status -Level "INFO" -Message "Running step: $Name"
    $output = & powershell -NoProfile -ExecutionPolicy Bypass -File $ScriptPath @Arguments 2>&1
    $exitCode = $LASTEXITCODE
    $ok = $AcceptExitCodes -contains $exitCode
    $status = if ($ok) { "PASS" } else { "FAIL" }

    $script:ProbeResults += [pscustomobject]@{
        Name     = $Name
        Command  = $cmdText
        ExitCode = $exitCode
        Status   = $status
        Output   = (Convert-OutputToText -OutputLines $output)
    }

    if ($ok) {
        Write-Status -Level "OK" -Message "$Name passed with exit code $exitCode"
    } else {
        Write-Status -Level "FAIL" -Message "$Name failed with exit code $exitCode"
        $script:HasFailure = $true
    }
}

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$skill = $SkillName.Trim().ToLowerInvariant()
$scriptRoot = Join-Path $root ".skills"

$supported = @(
    "update-release-workflow",
    "frontend-ui-implementation",
    "backend-api-implementation",
    "desktop-pyqt-ui-implementation",
    "checklist-backlog-governor",
    "exe-installer-build-setup",
    "publish-release-workflow"
)

if ($supported -notcontains $skill) {
    Fail "Unsupported skill: $SkillName. Supported skills: $($supported -join ', ')"
}

$probeToken = ""
$canary = ""
$ProbeResults = @()
$HasFailure = $false

# Print canary as the first visible line for probe checks.
switch ($skill) {
    "update-release-workflow" { Write-Output "CANARY_UPDATE_RELEASE_WORKFLOW_OK_20260210" }
    "frontend-ui-implementation" { Write-Output "CANARY_FRONTEND_UI_IMPLEMENTATION_OK_20260210" }
    "backend-api-implementation" { Write-Output "CANARY_BACKEND_API_IMPLEMENTATION_OK_20260210" }
    "desktop-pyqt-ui-implementation" { Write-Output "CANARY_DESKTOP_PYQT_UI_IMPLEMENTATION_OK_20260210" }
    "checklist-backlog-governor" { Write-Output "CANARY_CHECKLIST_BACKLOG_GOVERNOR_OK_20260210" }
    "exe-installer-build-setup" { Write-Output "CANARY_EXE_INSTALLER_BUILD_SETUP_OK_20260210" }
    "publish-release-workflow" { Write-Output "CANARY_PUBLISH_RELEASE_WORKFLOW_OK_20260210" }
}

switch ($skill) {
    "update-release-workflow" {
        $probeToken = "SKILL_PROBE_UPDATE_RELEASE_WORKFLOW"
        $canary = "CANARY_UPDATE_RELEASE_WORKFLOW_OK_20260210"
        $stepScript = Join-Path $scriptRoot "update-release-workflow\scripts\preflight_update.ps1"
        $args = @("-ProjectRoot", $root)
        if ($Strict.IsPresent) { $args += "-RequireInstaller" }
        Invoke-ProbeStep -Name "Update preflight" -ScriptPath $stepScript -Arguments $args
    }
    "frontend-ui-implementation" {
        $probeToken = "SKILL_PROBE_FRONTEND_UI_IMPLEMENTATION"
        $canary = "CANARY_FRONTEND_UI_IMPLEMENTATION_OK_20260210"
        $stepScript = Join-Path $scriptRoot "frontend-ui-implementation\scripts\preflight_frontend.ps1"
        $args = @("-ProjectRoot", $root)
        if ($Strict.IsPresent) {
            $args += "-RunLint"
            $args += "-RunBuild"
        }
        Invoke-ProbeStep -Name "Frontend preflight" -ScriptPath $stepScript -Arguments $args
    }
    "backend-api-implementation" {
        $probeToken = "SKILL_PROBE_BACKEND_API_IMPLEMENTATION"
        $canary = "CANARY_BACKEND_API_IMPLEMENTATION_OK_20260210"
        $stepScript = Join-Path $scriptRoot "backend-api-implementation\scripts\preflight_backend.ps1"
        $args = @("-ProjectRoot", $root, "-RunCompile")
        if ($Strict.IsPresent) { $args += "-RunPytest" }
        Invoke-ProbeStep -Name "Backend preflight" -ScriptPath $stepScript -Arguments $args
    }
    "desktop-pyqt-ui-implementation" {
        $probeToken = "SKILL_PROBE_DESKTOP_PYQT_UI_IMPLEMENTATION"
        $canary = "CANARY_DESKTOP_PYQT_UI_IMPLEMENTATION_OK_20260210"
        $stepScript = Join-Path $scriptRoot "desktop-pyqt-ui-implementation\scripts\preflight_desktop_ui.ps1"
        $args = @("-ProjectRoot", $root, "-RunCompile")
        if ($Strict.IsPresent) { $args += "-VerifyQtImports" }
        Invoke-ProbeStep -Name "Desktop UI preflight" -ScriptPath $stepScript -Arguments $args
    }
    "checklist-backlog-governor" {
        $probeToken = "SKILL_PROBE_CHECKLIST_BACKLOG_GOVERNOR"
        $canary = "CANARY_CHECKLIST_BACKLOG_GOVERNOR_OK_20260210"

        $ensureScript = Join-Path $scriptRoot "checklist-backlog-governor\scripts\ensure_checklist_backlog.ps1"
        $historyScript = Join-Path $scriptRoot "checklist-backlog-governor\scripts\log_history.ps1"
        $sandboxRoot = Join-Path $root (Join-Path $OutputDir "skill_probe_checklist_backlog_governor_sandbox")

        if (-not (Test-Path -LiteralPath $sandboxRoot)) {
            New-Item -ItemType Directory -Path $sandboxRoot | Out-Null
        }

        # First run should create SSOT file and return exit code 3.
        Invoke-ProbeStep -Name "Checklist SSOT initialization" -ScriptPath $ensureScript -Arguments @("-ProjectRoot", $sandboxRoot) -AcceptExitCodes @(3)
        # Second run should validate existing file and return 0.
        Invoke-ProbeStep -Name "Checklist SSOT validation" -ScriptPath $ensureScript -Arguments @("-ProjectRoot", $sandboxRoot)
        # History append should return 0.
        Invoke-ProbeStep -Name "Checklist history append" -ScriptPath $historyScript -Arguments @("-ProjectRoot", $sandboxRoot, "-Bucket", "CHECKLIST", "-StepId", "CL-PROBE", "-Status", "DOING", "-Entry", "Standardized self-test entry")
    }
    "exe-installer-build-setup" {
        $probeToken = "SKILL_PROBE_EXE_INSTALLER_BUILD_SETUP"
        $canary = "CANARY_EXE_INSTALLER_BUILD_SETUP_OK_20260210"
        $stepScript = Join-Path $scriptRoot "exe-installer-build-setup\scripts\preflight_build_pipeline.ps1"
        $args = @("-ProjectRoot", $root, "-RequireBuildOutput")
        if ($Strict.IsPresent) {
            $args += "-RequireInstallerOutput"
            $args += "-RequireInnoSetup"
        }
        Invoke-ProbeStep -Name "EXE/Installer preflight" -ScriptPath $stepScript -Arguments $args
    }
    "publish-release-workflow" {
        $probeToken = "SKILL_PROBE_PUBLISH_RELEASE_WORKFLOW"
        $canary = "CANARY_PUBLISH_RELEASE_WORKFLOW_OK_20260210"
        $stepScript = Join-Path $scriptRoot "publish-release-workflow\scripts\preflight_publish_release.ps1"
        $args = @("-ProjectRoot", $root)
        if ($Strict.IsPresent) {
            $args += "-RequireInstaller"
            $args += "-RequireRemoteRoot"
        }
        Invoke-ProbeStep -Name "Publish preflight" -ScriptPath $stepScript -Arguments $args
    }
}

Write-Status -Level "INFO" -Message "Probe token: $probeToken"

$reportDir = Join-Path $root $OutputDir
if (-not (Test-Path -LiteralPath $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir | Out-Null
}
$reportPath = Join-Path $reportDir ("skill_probe_{0}.md" -f $skill)

$reportLines = @()
$reportLines += "# Skill Self-Test Report"
$reportLines += ""
$reportLines += "- Skill: $skill"
$reportLines += "- Probe token: $probeToken"
$reportLines += "- Canary: $canary"
$reportLines += "- Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$reportLines += "- Strict mode: $($Strict.IsPresent)"
$reportLines += ""
$reportLines += "## Steps"
$reportLines += ""
$reportLines += "| Step | Command | Exit Code | Status |"
$reportLines += "| --- | --- | --- | --- |"

foreach ($step in $ProbeResults) {
    $safeCmd = ($step.Command -replace '\|', '\\|')
    $reportLines += "| $($step.Name) | $safeCmd | $($step.ExitCode) | $($step.Status) |"
}

$reportLines += ""
$reportLines += "## Output Preview"

foreach ($step in $ProbeResults) {
    $reportLines += ""
    $reportLines += "### $($step.Name)"
    $reportLines += '```text'
    $preview = ($step.Output -split "`r?`n" | Select-Object -First 40) -join "`n"
    if ([string]::IsNullOrWhiteSpace($preview)) {
        $preview = "(no output)"
    }
    $reportLines += $preview
    $reportLines += '```'
}

$reportLines += ""
$reportLines += "## Outcome"
$reportLines += ""
if ($HasFailure) {
    $reportLines += "- Final status: **FAIL**"
} else {
    $reportLines += "- Final status: **PASS**"
}

[System.IO.File]::WriteAllText(
    $reportPath,
    ($reportLines -join "`r`n"),
    (New-Object System.Text.UTF8Encoding($false))
)

Write-Status -Level "INFO" -Message "Report written: $reportPath"

if ($HasFailure) {
    exit 1
}
exit 0
