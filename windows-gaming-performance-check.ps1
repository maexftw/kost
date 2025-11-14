# Windows Gaming Performance Diagnostic Script
# Checks common settings that can degrade gaming performance

Write-Host '=== Windows Gaming Performance Diagnostic ===' -ForegroundColor Cyan
Write-Host ''

$issues = @()
$warnings = @()
$good = @()

# Check 1: Windows Game Mode
Write-Host '[1/10] Checking Windows Game Mode...' -ForegroundColor Yellow
try {
    $gameMode = Get-ItemProperty -Path "HKCU:\Software\Microsoft\GameBar" -Name "AllowAutoGameMode" -ErrorAction SilentlyContinue
    if ($gameMode.AllowAutoGameMode -eq 1) {
        $good += 'Game Mode is enabled'
        Write-Host '  [OK] Game Mode is enabled' -ForegroundColor Green
    } else {
        $issues += 'Game Mode is disabled - Enable in Settings > Gaming > Game Mode'
        Write-Host '  [ISSUE] Game Mode is disabled' -ForegroundColor Red
    }
} catch {
    $warnings += 'Could not check Game Mode status'
    Write-Host '  [WARN] Could not check Game Mode' -ForegroundColor Yellow
}

# Check 2: Windows Visual Effects
Write-Host '[2/10] Checking Visual Effects settings...' -ForegroundColor Yellow
try {
    $visualEffects = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Name "VisualFXSetting" -ErrorAction SilentlyContinue
    if ($visualEffects.VisualFXSetting -eq 2) {
        $good += "Visual Effects set to 'Adjust for best performance'"
        Write-Host '  [OK] Visual Effects optimized for performance' -ForegroundColor Green
    } elseif ($visualEffects.VisualFXSetting -eq 0) {
        $warnings += "Visual Effects set to 'Let Windows decide' - Consider 'Adjust for best performance'"
        Write-Host '  [WARN] Visual Effects: Let Windows decide (could be optimized)' -ForegroundColor Yellow
    } else {
        $issues += "Visual Effects may be set to 'Best appearance' - Change to 'Best performance' in System Properties"
        Write-Host '  [ISSUE] Visual Effects may favor appearance over performance' -ForegroundColor Red
    }
} catch {
    $warnings += 'Could not check Visual Effects'
    Write-Host '  [WARN] Could not check Visual Effects' -ForegroundColor Yellow
}

# Check 3: Power Plan
Write-Host '[3/10] Checking Power Plan...' -ForegroundColor Yellow
try {
    $powerPlan = powercfg /getactivescheme
    if ($powerPlan -match "High performance" -or $powerPlan -match "Gaming") {
        $good += 'High performance power plan is active'
        Write-Host '  [OK] High performance power plan active' -ForegroundColor Green
    } else {
        $issues += 'Not using High Performance power plan - Switch in Power Options'
        Write-Host '  [ISSUE] Not using High Performance power plan' -ForegroundColor Red
        Write-Host '    Run: powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c' -ForegroundColor Gray
    }
} catch {
    $warnings += 'Could not check power plan'
    Write-Host '  [WARN] Could not check power plan' -ForegroundColor Yellow
}

# Check 4: Windows Update Delivery Optimization (P2P)
Write-Host '[4/10] Checking Windows Update Delivery Optimization...' -ForegroundColor Yellow
try {
    $deliveryOpt = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config" -Name "DODownloadMode" -ErrorAction SilentlyContinue
    if ($deliveryOpt.DODownloadMode -eq 0) {
        $good += 'Windows Update Delivery Optimization disabled (good for gaming)'
        Write-Host '  [OK] Update Delivery Optimization disabled' -ForegroundColor Green
    } else {
        $warnings += 'Windows Update Delivery Optimization enabled - May use bandwidth/CPU'
        Write-Host '  [WARN] Update Delivery Optimization enabled (may use resources)' -ForegroundColor Yellow
    }
} catch {
    $warnings += 'Could not check Update Delivery Optimization'
    Write-Host '  [WARN] Could not check Update Delivery Optimization' -ForegroundColor Yellow
}

# Check 5: Xbox Game Bar
Write-Host '[5/10] Checking Xbox Game Bar...' -ForegroundColor Yellow
try {
    $gameBar = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\GameDVR" -Name "AppCaptureEnabled" -ErrorAction SilentlyContinue
    if ($gameBar.AppCaptureEnabled -eq 0) {
        $good += 'Xbox Game Bar recording disabled'
        Write-Host '  [OK] Game Bar recording disabled' -ForegroundColor Green
    } else {
        $warnings += 'Xbox Game Bar recording enabled - May impact performance'
        Write-Host '  [WARN] Game Bar recording enabled (may impact performance)' -ForegroundColor Yellow
    }
} catch {
    $warnings += 'Could not check Xbox Game Bar'
    Write-Host '  [WARN] Could not check Xbox Game Bar' -ForegroundColor Yellow
}

# Check 6: Fullscreen Optimizations
Write-Host '[6/10] Checking Fullscreen Optimizations...' -ForegroundColor Yellow
Write-Host '  [INFO] Check each game executable: Right-click `> Properties `> Compatibility `> Disable fullscreen optimizations' -ForegroundColor Cyan

# Check 7: Windows Search Indexing
Write-Host '[7/10] Checking Windows Search Indexing...' -ForegroundColor Yellow
try {
    $searchService = Get-Service -Name "WSearch" -ErrorAction SilentlyContinue
    if ($searchService.Status -eq "Running") {
        $warnings += 'Windows Search Indexing is running - May use CPU/disk during gaming'
        Write-Host '  [WARN] Search Indexing is running (may use resources)' -ForegroundColor Yellow
    } else {
        $good += 'Search Indexing is stopped'
        Write-Host '  [OK] Search Indexing is stopped' -ForegroundColor Green
    }
} catch {
    $warnings += 'Could not check Search Indexing'
    Write-Host '  [WARN] Could not check Search Indexing' -ForegroundColor Yellow
}

# Check 8: Background Apps
Write-Host '[8/10] Checking Background Apps setting...' -ForegroundColor Yellow
try {
    $null = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" -ErrorAction SilentlyContinue
    Write-Host '  [INFO] Review Settings `> Privacy `> Background apps - Disable unnecessary apps' -ForegroundColor Cyan
} catch {
    Write-Host "  ? Could not check Background Apps" -ForegroundColor Yellow
}

# Check 9: Windows Defender Real-time Protection
Write-Host '[9/10] Checking Windows Defender...' -ForegroundColor Yellow
try {
    $defenderStatus = Get-MpComputerStatus -ErrorAction SilentlyContinue
    if ($defenderStatus) {
        Write-Host '  [INFO] Windows Defender is active - Consider adding game folders to exclusions' -ForegroundColor Cyan
        Write-Host '    Settings `> Virus `& threat protection `> Manage settings `> Exclusions' -ForegroundColor Gray
    }
} catch {
    Write-Host "  ? Could not check Windows Defender (may require admin rights)" -ForegroundColor Yellow
}

# Check 10: V-Sync and GPU Settings
Write-Host '[10/10] Checking GPU-related settings...' -ForegroundColor Yellow
Write-Host '  [INFO] Review NVIDIA Control Panel / AMD Radeon Settings:' -ForegroundColor Cyan
Write-Host "    - Set Power Management Mode to 'Prefer maximum performance'" -ForegroundColor Gray
Write-Host '    - Disable V-Sync globally (enable per-game if needed)' -ForegroundColor Gray
Write-Host "    - Set Texture Filtering Quality to 'Performance'" -ForegroundColor Gray

Write-Host ''
Write-Host '=== Summary ===' -ForegroundColor Cyan
Write-Host ''

if ($good.Count -gt 0) {
    Write-Host ("Good Settings ({0}):" -f $good.Count) -ForegroundColor Green
    foreach ($item in $good) {
        Write-Host ("  - {0}" -f $item) -ForegroundColor Green
    }
    Write-Host ''
}

if ($warnings.Count -gt 0) {
    Write-Host ("Warnings ({0}):" -f $warnings.Count) -ForegroundColor Yellow
    foreach ($item in $warnings) {
        Write-Host ("  - {0}" -f $item) -ForegroundColor Yellow
    }
    Write-Host ''
}

if ($issues.Count -gt 0) {
    Write-Host ("Issues Found ({0}):" -f $issues.Count) -ForegroundColor Red
    foreach ($item in $issues) {
        Write-Host ("  - {0}" -f $item) -ForegroundColor Red
    }
    Write-Host ''
}

Write-Host '=== Manual Checks Recommended ===' -ForegroundColor Cyan
Write-Host '1. Disable Windows Visual Effects: System Properties `> Advanced `> Performance Settings `> Adjust for best performance' -ForegroundColor White
Write-Host '2. Set Power Plan to High Performance: Control Panel `> Power Options' -ForegroundColor White
Write-Host '3. Disable Game Bar recording if not needed: Settings `> Gaming `> Game Bar' -ForegroundColor White
Write-Host '4. Add game folders to Windows Defender exclusions' -ForegroundColor White
Write-Host '5. Disable unnecessary startup programs: Task Manager `> Startup tab' -ForegroundColor White
Write-Host '6. Check GPU driver settings (NVIDIA/AMD control panel)' -ForegroundColor White
Write-Host '7. Disable fullscreen optimizations per-game: Right-click exe `> Properties `> Compatibility' -ForegroundColor White
Write-Host '8. Close unnecessary background applications before gaming' -ForegroundColor White
Write-Host ''

