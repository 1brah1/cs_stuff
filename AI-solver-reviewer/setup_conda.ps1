# Anaconda/Conda Setup Script for AI Document Reviewer
# This script helps you set up the project using Anaconda

Write-Host "Anaconda Setup for AI Document Reviewer" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Common Anaconda installation paths
$condaPaths = @(
    "$env:USERPROFILE\Anaconda3\Scripts\conda.exe",
    "$env:USERPROFILE\Anaconda3\condabin\conda.bat",
    "$env:USERPROFILE\Miniconda3\Scripts\conda.exe",
    "$env:USERPROFILE\Miniconda3\condabin\conda.bat",
    "C:\ProgramData\Anaconda3\Scripts\conda.exe",
    "C:\ProgramData\Anaconda3\condabin\conda.bat",
    "C:\Users\$env:USERNAME\AppData\Local\Continuum\anaconda3\Scripts\conda.exe"
)

$condaPath = $null
foreach ($path in $condaPaths) {
    if (Test-Path $path) {
        $condaPath = $path
        Write-Host "Found Anaconda at: $path" -ForegroundColor Green
        break
    }
}

if (-not $condaPath) {
    Write-Host "Could not find Anaconda automatically." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please provide your Anaconda installation path:" -ForegroundColor Cyan
    Write-Host "Example: C:\Users\YourName\Anaconda3\Scripts\conda.exe"
    $customPath = Read-Host "Enter path to conda.exe"
    if (Test-Path $customPath) {
        $condaPath = $customPath
    } else {
        Write-Host "Path not found. Please initialize Anaconda manually." -ForegroundColor Red
        Write-Host ""
        Write-Host "To initialize Anaconda, run:" -ForegroundColor Yellow
        Write-Host "& 'C:\Users\YourName\Anaconda3\Scripts\Anaconda3-64.exe' -Command 'conda init powershell'" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Or use Anaconda Prompt from Start Menu instead." -ForegroundColor Cyan
        exit 1
    }
}

Write-Host ""
Write-Host "Creating conda environment 'ai-reviewer' with Python 3.11..." -ForegroundColor Cyan

# Create conda environment
& $condaPath create -n ai-reviewer python=3.11 -y

if ($LASTEXITCODE -eq 0) {
    Write-Host "Environment created successfully!" -ForegroundColor Green
} else {
    Write-Host "Error creating environment. Trying alternative method..." -ForegroundColor Yellow
    # Try using conda.bat instead
    $condaBat = $condaPath -replace "conda.exe", "conda.bat"
    if (Test-Path $condaBat) {
        & cmd /c "$condaBat create -n ai-reviewer python=3.11 -y"
    }
}

Write-Host ""
Write-Host "To use this environment:" -ForegroundColor Cyan
Write-Host "1. Activate it: conda activate ai-reviewer" -ForegroundColor Yellow
Write-Host "2. Navigate to backend: cd backend" -ForegroundColor Yellow
Write-Host "3. Install dependencies: pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "4. Run backend: python run.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or use Anaconda Prompt and run:" -ForegroundColor Cyan
Write-Host "  conda activate ai-reviewer" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor Yellow
Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "  python run.py" -ForegroundColor Yellow




