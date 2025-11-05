# Script to download customer logos
# This script attempts to download logos from various sources

$logoDir = "images\logos"
New-Item -ItemType Directory -Force -Path $logoDir | Out-Null

# Customer names and their potential logo URLs
# NOTE: Some logos (Paratos, Boss-Steinlen) are available in email attachments in Kostmails folder
# Those should be extracted manually from the .eml files
$logos = @(
    @{
        Name = "Paratos GmbH"
        FileName = "paratos.png"
        URLs = @(
            "https://www.paratos.de/images/logo.png",
            "https://www.paratos.de/assets/logo.png"
        )
        Note = "Check email attachments in Kostmails folder"
    },
    @{
        Name = "BOSS-Steinlen"
        FileName = "boss-steinlen.png"
        URLs = @(
            "https://www.boss-steinlen.de/images/logo.png",
            "https://www.boss-steinlen.de/assets/logo.png"
        )
        Note = "Check email attachments - Logo_Boss-Steinlen-1400x142.png"
    },
    @{
        Name = "Deutsches Fußballmuseum"
        FileName = "fussballmuseum.png"
        URLs = @(
            "https://www.deutsches-fussballmuseum.de/wp-content/themes/dfb/images/logo.png",
            "https://www.deutsches-fussballmuseum.de/assets/img/logo.png",
            "https://www.deutsches-fussballmuseum.de/img/logo.png"
        )
    },
    @{
        Name = "WDI Schwerte"
        FileName = "wdi-schwerte.png"
        URLs = @(
            "https://www.wdi-schwerte.de/images/logo.png",
            "https://www.wdi-schwerte.de/assets/logo.png"
        )
    },
    @{
        Name = "Universität Münster"
        FileName = "uni-muenster.png"
        URLs = @(
            "https://www.uni-muenster.de/de/_assets/images/logo/logo-uni-muenster.png",
            "https://www.uni-muenster.de/imperia/md/images/logo/logo-uni-muenster.png",
            "https://www.uni-muenster.de/assets/images/logo.png"
        )
    },
    @{
        Name = "HSE Getränkewelt Essen"
        FileName = "hse-getraenkewelt.png"
        URLs = @(
            "https://www.hse-getraenkewelt.de/images/logo.png",
            "https://www.hse-getraenkewelt.de/assets/logo.png"
        )
    },
    @{
        Name = "Kurt Pietsch GmbH Group"
        FileName = "kurt-pietsch.png"
        URLs = @(
            "https://www.kurt-pietsch.de/images/logo.png",
            "https://www.kurt-pietsch.de/assets/logo.png"
        )
    },
    @{
        Name = "Olympia Gruppe"
        FileName = "olympia-gruppe.png"
        URLs = @(
            "https://www.olympia-gruppe.de/images/logo.png",
            "https://www.olympia-gruppe.de/assets/logo.png"
        )
    },
    @{
        Name = "L'Arrivée"
        FileName = "larrivee.png"
        URLs = @(
            "https://www.larrivee.de/images/logo.png",
            "https://www.larrivee.de/assets/logo.png"
        )
    },
    @{
        Name = "FUTURE-X"
        FileName = "future-x.png"
        URLs = @(
            "https://www.future-x.de/images/logo.png",
            "https://www.future-x.de/assets/logo.png"
        )
    },
    @{
        Name = "versatel"
        FileName = "versatel.png"
        URLs = @(
            "https://www.versatel.de/images/logo.png",
            "https://www.versatel.de/assets/logo.png"
        )
    },
    @{
        Name = "McFIT"
        FileName = "mcfit.png"
        URLs = @(
            "https://www.mcfit.com/images/logo.png",
            "https://www.mcfit.com/assets/logo.png"
        )
    },
    @{
        Name = "Dortmund"
        FileName = "dortmund.png"
        URLs = @(
            "https://www.dortmund.de/images/logo.png",
            "https://www.dortmund.de/assets/logo.png"
        )
    },
    @{
        Name = "Carlos"
        FileName = "carlos.png"
        URLs = @(
            "https://www.carlos.de/images/logo.png",
            "https://www.carlos.de/assets/logo.png"
        )
    }
)

Write-Host "Starting logo download process..." -ForegroundColor Green

foreach ($logo in $logos) {
    $filePath = Join-Path $logoDir $logo.FileName
    
    # Skip if file already exists
    if (Test-Path $filePath) {
        Write-Host "Logo already exists: $($logo.FileName)" -ForegroundColor Yellow
        continue
    }
    
    $downloaded = $false
    
    foreach ($url in $logo.URLs) {
        try {
            Write-Host "Trying to download $($logo.Name) from $url..." -ForegroundColor Cyan
            $response = Invoke-WebRequest -Uri $url -Method Get -ErrorAction Stop
            
            if ($response.StatusCode -eq 200 -and $response.Content.Length -gt 0) {
                [System.IO.File]::WriteAllBytes($filePath, $response.Content)
                Write-Host "Successfully downloaded: $($logo.FileName)" -ForegroundColor Green
                $downloaded = $true
                break
            }
        }
        catch {
            Write-Host "Failed to download from $url" -ForegroundColor Red
        }
    }
    
    if (-not $downloaded) {
        Write-Host "Could not download logo for $($logo.Name). Please download manually and save as $filePath" -ForegroundColor Yellow
        if ($logo.Note) {
            Write-Host "  NOTE: $($logo.Note)" -ForegroundColor Cyan
        }
        Write-Host "You can search for the logo at:" -ForegroundColor Yellow
        Write-Host "  - Official website of the company" -ForegroundColor Gray
        Write-Host "  - Logo databases like logodix.com, brandfetch.com, or clearbit.com" -ForegroundColor Gray
        Write-Host ""
    }
}

Write-Host "`nLogo download process completed!" -ForegroundColor Green
Write-Host "Please check the $logoDir folder for downloaded logos." -ForegroundColor Cyan
Write-Host "If any logos are missing, download them manually and place them in the logos folder." -ForegroundColor Yellow

