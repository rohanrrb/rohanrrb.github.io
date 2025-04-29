# Exit on error
$ErrorActionPreference = "Stop"

# Define paths
$zipPath = "frontend.zip"
$tempExtract = "frontend"
$targetDir = "docs"

try {
    Write-Host "Exporting Reflex app..."
    # Run reflex export and check for success
    $reflexProcess = Start-Process -FilePath "reflex" -ArgumentList "export" -NoNewWindow -PassThru -Wait
    if ($reflexProcess.ExitCode -ne 0) {
        Write-Host "Error: 'reflex export' failed with exit code $($reflexProcess.ExitCode)."
        exit 1
    }

    # Check if frontend.zip exists
    if (-not (Test-Path $zipPath)) {
        Write-Host "Error: frontend.zip not found. Did 'reflex export' succeed?"
        exit 1
    }

    Write-Host "Unzipping frontend.zip..."
    # Remove existing temp extract directory
    if (Test-Path $tempExtract) {
        Remove-Item -Recurse -Force $tempExtract -ErrorAction Stop
    }

    # Unzip frontend.zip
    Expand-Archive -Path $zipPath -DestinationPath $tempExtract -Force -ErrorAction Stop

    # Verify extraction
    if (-not (Test-Path $tempExtract)) {
        Write-Host "Error: Failed to extract frontend.zip to $tempExtract."
        exit 1
    }

    Write-Host "Moving contents to /docs..."
    # Remove existing docs directory
    if (Test-Path $targetDir) {
        Remove-Item -Recurse -Force $targetDir -ErrorAction Stop
    }

    # Create docs directory and copy files
    New-Item -ItemType Directory -Force -Path $targetDir -ErrorAction Stop
    Copy-Item -Recurse -Force "$tempExtract\*" "$targetDir\" -ErrorAction Stop

    Write-Host "Adding .nojekyll..."
    # Create .nojekyll file
    New-Item -ItemType File -Path "$targetDir\.nojekyll" -Force -ErrorAction Stop

    Write-Host "Committing and pushing to GitHub..."
    # Verify git is available
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "Error: Git is not installed or not in PATH."
        exit 1
    }

    # Add, commit, and push
    git add "$targetDir/" | Out-Null
    git commit -m "Deploy Reflex static site from frontend.zip" | Out-Null
    git push | Out-Null

    Write-Host "Deployment completed successfully!"
}
catch {
    Write-Host "Error occurred: $($_.Exception.Message)"
    Write-Host "At: $($_.ScriptStackTrace)"
    exit 1
}
finally {
    # Clean up temp extract directory
    if (Test-Path $tempExtract) {
        Write-Host "Cleaning up temporary files..."
        Remove-Item -Recurse -Force $tempExtract -ErrorAction SilentlyContinue
    }
}