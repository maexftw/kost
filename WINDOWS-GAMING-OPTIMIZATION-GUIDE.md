# Windows Gaming Performance Optimization Guide

## Quick Fixes (Most Impact)

### 1. Power Plan → High Performance
**Impact: High** | **Difficulty: Easy**

```powershell
# Run as Administrator
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

Or manually:
- Control Panel > Power Options > Select "High performance"
- If not visible: Create custom plan > High performance

### 2. Visual Effects → Best Performance
**Impact: Medium-High** | **Difficulty: Easy**

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Advanced tab > Performance Settings
3. Select "Adjust for best performance"
4. Click OK

### 3. Windows Game Mode
**Impact: Medium** | **Difficulty: Easy**

1. Settings (Win + I) > Gaming > Game Mode
2. Toggle "Game Mode" ON

### 4. Disable Fullscreen Optimizations (Per Game)
**Impact: Medium** | **Difficulty: Easy**

1. Right-click game executable (.exe)
2. Properties > Compatibility tab
3. Check "Disable fullscreen optimizations"
4. Apply

### 5. Windows Defender Exclusions
**Impact: Medium** | **Difficulty: Easy**

1. Settings > Privacy & Security > Windows Security
2. Virus & threat protection > Manage settings
3. Exclusions > Add or remove exclusions
4. Add folders: Game installation folders, save game folders

---

## GPU Settings

### NVIDIA Control Panel
1. Right-click desktop > NVIDIA Control Panel
2. **Manage 3D Settings:**
   - Power management mode: **Prefer maximum performance**
   - Texture filtering - Quality: **High performance**
   - Vertical sync: **Off** (enable per-game if needed)
   - Threaded optimization: **On**
3. **Set PhysX configuration:** Select your GPU (not Auto)

### AMD Radeon Settings
1. Right-click desktop > AMD Radeon Settings
2. **Gaming > Global Settings:**
   - Power Tuning: **Maximum**
   - Radeon Anti-Lag: **Enabled** (if supported)
   - Radeon Boost: **Enabled** (if supported)
   - Wait for Vertical Refresh: **Off, unless application specifies**

---

## Background Processes

### Disable Xbox Game Bar Recording
**Impact: Low-Medium** | **Difficulty: Easy**

1. Settings > Gaming > Game Bar
2. Toggle "Record game clips, screenshots, and broadcast using Game bar" OFF

### Disable Background Apps
**Impact: Low-Medium** | **Difficulty: Easy**

1. Settings > Privacy > Background apps
2. Turn OFF apps you don't need running in background

### Disable Windows Search Indexing (Optional)
**Impact: Low** | **Difficulty: Medium**

Only if you don't use Windows Search frequently:

1. Services (Win + R, type `services.msc`)
2. Find "Windows Search"
3. Right-click > Properties > Startup type: **Disabled**
4. Stop the service

**Warning:** This will make Windows Search slower. Only disable if you rarely use it.

---

## Windows Update & Delivery Optimization

### Limit Update Delivery Optimization
**Impact: Low** | **Difficulty: Easy**

1. Settings > Windows Update > Advanced options
2. Delivery Optimization > Advanced options
3. Set "Download from other PCs" to **Off** or **PCs on my local network**

---

## Startup Programs

**Impact: Medium** | **Difficulty: Easy**

1. Task Manager (Ctrl + Shift + Esc)
2. Startup tab
3. Disable unnecessary programs
4. Keep only essential: Antivirus, GPU drivers, audio drivers

---

## Advanced Optimizations

### Disable HPET (High Precision Event Timer)
**Impact: Low-Medium** | **Difficulty: Advanced**

⚠️ **Only if you experience micro-stutters**

```powershell
# Run as Administrator
bcdedit /set useplatformclock false
```

To revert:
```powershell
bcdedit /deletevalue useplatformclock
```

### Disable Windows Defender Real-time Protection Temporarily
**Impact: Medium** | **Difficulty: Easy** ⚠️ **Security Risk**

Only for testing if you suspect Defender is causing issues:
1. Settings > Privacy & Security > Windows Security
2. Virus & threat protection > Manage settings
3. Temporarily disable Real-time protection

**Better solution:** Add game folders to exclusions (see above)

---

## Monitoring Tools

### Check Current Performance
- **Task Manager:** See CPU, GPU, RAM usage
- **MSI Afterburner:** Monitor FPS, GPU temp, usage
- **HWiNFO64:** Detailed hardware monitoring

### What to Look For
- CPU usage > 90% during gaming → CPU bottleneck
- GPU usage < 80% during gaming → CPU bottleneck or vsync limiting
- High RAM usage → Close background apps
- High disk usage → Disable indexing or move game to SSD

---

## Quick Diagnostic Script

Run the included PowerShell script:
```powershell
.\windows-gaming-performance-check.ps1
```

This will check common settings automatically.

---

## Common Issues & Solutions

### Stuttering / Frame Drops
1. Check CPU/GPU temperatures (should be < 80°C)
2. Disable fullscreen optimizations
3. Update GPU drivers
4. Check for Windows updates
5. Disable Windows Game Bar recording

### Low FPS
1. Set Power Plan to High Performance
2. Check GPU settings (see above)
3. Lower in-game graphics settings
4. Close background applications
5. Check if CPU/GPU is thermal throttling

### Input Lag
1. Disable V-Sync (or use G-Sync/FreeSync if available)
2. Disable fullscreen optimizations
3. Set GPU to "Prefer maximum performance"
4. Check mouse polling rate settings

---

## Notes

- **Always update GPU drivers** - Use manufacturer's tool (GeForce Experience, AMD Software)
- **Keep Windows updated** - But pause updates during gaming sessions if needed
- **Monitor temperatures** - Overheating causes throttling and performance loss
- **Test one change at a time** - So you know what actually helps

---

## When to Consider Hardware Upgrades

If after all optimizations you still have issues:
- **Low FPS:** GPU upgrade
- **Stuttering:** CPU or RAM upgrade
- **Long load times:** SSD upgrade (if using HDD)



