@echo off
REM Script para ejecutar AutoForense en Windows
REM Ejecutar como Administrador para funcionalidad completa

echo ========================================
echo      AutoForense - Iniciando...
echo ========================================
echo.

REM Verificar si estamos en el directorio correcto
if not exist "src\AutoForense.py" (
    echo Error: No se encuentra AutoForense.py
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no esta instalado o no esta en PATH
    echo Instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python detectado correctamente
echo.

echo ========================================
echo   Iniciando AutoForense...
echo ========================================
echo.

REM Cambiar al directorio src y ejecutar
cd src
python AutoForense.py

REM Volver al directorio original
cd ..

echo.
echo ========================================
echo   AutoForense finalizado
echo ========================================
pause


