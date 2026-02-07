<#
PowerShell launcher for Project Robot
Usage: Right-click -> Run with PowerShell, or execute in PowerShell:
  .\launch_robot.ps1
#>
try {
    $P = Split-Path -Parent $MyInvocation.MyCommand.Definition
    Set-Location $P
} catch {
    # fallback to current location
}

Write-Host "Starting Project Robot (with vocabulary + Wikipedia)..."
python robot_with_vocabulary.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Program exited with code $LASTEXITCODE"
}

Write-Host "Press Enter to close..."; [void][System.Console]::ReadLine()
