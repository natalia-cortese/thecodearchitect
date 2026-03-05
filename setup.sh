#!/bin/bash
# setup.sh — Crea el entorno virtual e instala dependencias

set -e

echo ""
echo "🏙️  The Code Architect — Setup"
echo "================================"

# Verificar Python 3.11+
python_cmd=""
for cmd in python3.11 python3.12 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" -c "import sys; print(sys.version_info[:2])")
        if "$cmd" -c "import sys; assert sys.version_info >= (3,11)" 2>/dev/null; then
            python_cmd="$cmd"
            break
        fi
    fi
done

if [ -z "$python_cmd" ]; then
    echo "❌ Se requiere Python 3.11 o superior."
    echo "   Descargalo desde https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python encontrado: $($python_cmd --version)"

# Crear venv
if [ -d "venv" ]; then
    echo "ℹ️  El entorno virtual ya existe. Saltando creación."
else
    echo "📦 Creando entorno virtual..."
    "$python_cmd" -m venv venv
    echo "✅ Entorno virtual creado en ./venv"
fi

# Activar e instalar
echo "📥 Instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

echo ""
echo "✅ ¡Todo listo!"
echo ""
echo "Para jugar:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
