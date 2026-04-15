# Makefile — Comandos de conveniencia para The Code Architect
# Uso: make <comando>

.PHONY: setup run srp clean help test test-cov lint

VENV      = venv
PYTHON    = $(VENV)/bin/python
PIP       = $(VENV)/bin/pip

# Detectar OS para activación correcta
ifeq ($(OS),Windows_NT)
    PYTHON  = $(VENV)/Scripts/python
    PIP     = $(VENV)/Scripts/pip
    ACTIVATE = $(VENV)/Scripts/activate
else
    ACTIVATE = $(VENV)/bin/activate
endif

## help: Muestra esta ayuda
help:
	@echo ""
	@echo " 🏙️  The Code Architect — Comandos disponibles"
	@echo " ─────────────────────────────────────────────"
	@grep -E '^## ' Makefile | sed 's/## /  make /'
	@echo ""

## setup: Crea el venv e instala dependencias
setup: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip -q
	$(PIP) install -r requirements.txt
	@echo "✅ Setup completo. Ejecutá: make run"

## run: Inicia el juego
run: $(VENV)/bin/activate
	$(PYTHON) main.py

## srp: Ejecuta el ejemplo SRP en terminal (sin pygame)
srp: $(VENV)/bin/activate
	$(PYTHON) levels/srp_example.py

## test: Ejecuta los tests
test: $(VENV)/bin/activate
	$(PYTHON) -m pytest tests/ -v

## test-cov: Ejecuta tests con coverage
test-cov: $(VENV)/bin/activate
	$(PYTHON) -m pytest tests/ -v --cov=. --cov-report=term-missing

## lint: Ejecuta linter flake8
lint: $(VENV)/bin/activate
	$(PYTHON) -m flake8 . --count --max-line-length=120 --statistics

## clean: Elimina el entorno virtual y archivos temporales
clean:
	rm -rf $(VENV) __pycache__ */__pycache__ *.pyc */*.pyc .pytest_cache .coverage
	@echo "🧹 Limpieza completa."
