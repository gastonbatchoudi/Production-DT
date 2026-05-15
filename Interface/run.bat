@echo off
echo ========================================
echo   AVOSDIM Factory Planning Interface
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "..\venv\Scripts\activate.bat" (
    echo [ERREUR] Environnement virtuel non trouve!
    echo Veuillez d'abord creer l'environnement virtuel:
    echo   python -m venv venv
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo [1/3] Activation de l'environnement virtuel...
call ..\venv\Scripts\activate.bat

REM Vérifier si streamlit est installé
echo [2/3] Verification des dependances...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Streamlit non installe. Installation en cours...
    pip install -r requirements.txt
)

REM Lancer Streamlit
echo [3/3] Lancement de l'interface...
echo.
echo L'interface va s'ouvrir dans votre navigateur...
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.
streamlit run App.py

pause
