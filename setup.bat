@echo off
REM setup.bat — Crea el entorno virtual e instala dependencias (Windows)

echo.
echo  The Code Architect — Setup
echo ================================

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado.
    echo         Descargalo desde https://www.python.org/downloads/
    echo         Asegurate de marcar "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python encontrado: %PYVER%

REM Crear venv
if exist venv\ (
    echo [INFO] El entorno virtual ya existe. Saltando creacion.
) else (
    echo [..] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado en .\venv
)

REM Activar e instalar
echo [..] Instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt

echo.
echo [OK] Todo listo!
echo.
echo Para jugar:
echo   venv\Scripts\activate
echo   python main.py
echo.
pause
