@echo off
echo =========================================
echo Instalacja bibliotek Python (s2p plot)
echo =========================================

REM Sprawdzenie czy Python jest dostepny
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo BLAD: Python nie jest zainstalowany lub nie jest w PATH
    pause
    exit /b 1
)

echo Python OK
echo.

REM Aktualizacja pip
echo Aktualizacja pip...
python -m pip install --upgrade pip

REM Instalacja wymaganych bibliotek
echo.
echo Instalacja bibliotek...
python -m pip install numpy matplotlib

IF ERRORLEVEL 1 (
    echo.
    echo BLAD podczas instalacji bibliotek
    pause
    exit /b 1
)

echo.
echo =========================================
echo Instalacja zakonczona pomyslnie
echo =========================================
pause