# Script PowerShell pour lancer l'interface AVOSDIM

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AVOSDIM Factory Planning Interface" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si l'environnement virtuel existe
if (-not (Test-Path "..\venv\Scripts\Activate.ps1")) {
    Write-Host "[ERREUR] Environnement virtuel non trouvé!" -ForegroundColor Red
    Write-Host "Veuillez d'abord créer l'environnement virtuel:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Activer l'environnement virtuel
Write-Host "[1/3] Activation de l'environnement virtuel..." -ForegroundColor Green
& ..\venv\Scripts\Activate.ps1

# Vérifier si streamlit est installé
Write-Host "[2/3] Vérification des dépendances..." -ForegroundColor Green
$streamlitInstalled = python -c "import streamlit" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Streamlit non installé. Installation en cours..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Lancer Streamlit
Write-Host "[3/3] Lancement de l'interface..." -ForegroundColor Green
Write-Host ""
Write-Host "L'interface va s'ouvrir dans votre navigateur..." -ForegroundColor Cyan
Write-Host "URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

streamlit run App.py
