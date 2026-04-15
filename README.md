# 🏙️ The Code Architect

> Un videojuego didáctico 2D para aprender los principios **SOLID** de diseño de software.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Nivel](https://img.shields.io/badge/Nivel-1%20de%205-orange)

---

## 🎮 Concepto

El jugador asume el rol de un **Arquitecto de Software** en una ciudad digital. Su misión: construir y mantener sistemas bien diseñados. Si el código está mal organizado, **la ciudad colapsa bajo su propio peso**.

Cada nivel enseña uno de los cinco principios SOLID usando mecánicas de juego, código Python real y feedback inmediato.

---

## 📐 Niveles (Roadmap)

| # | Principio | Estado |
|---|-----------|--------|
| 1 | **S** — Single Responsibility (SRP) | ✅ Disponible |
| 2 | **O** — Open/Closed (OCP) | ✅ Disponible |
| 3 | **L** — Liskov Substitution (LSP) | ✅ Disponible |
| 4 | **I** — Interface Segregation (ISP) | 🔜 Planeado |
| 5 | **D** — Dependency Inversion (DIP) | 🔜 Planeado |

---

## 🧩 Nivel 1 — Single Responsibility Principle (SRP)

### El Desafío

Recibís una **Clase Monstruo** llamada `Video` que viola el SRP: intenta calcular estadísticas Y guardar en la base de datos al mismo tiempo.

```
┌─────────────────────────────┐
│          Video  ⚠           │
│  - get_full_length()   ─────┼──► Cálculo
│  - get_total_size()    ─────┼──► Cálculo
│  - save()              ─────┼──► Base de datos
│  - update()            ─────┼──► Base de datos
│  - delete()            ─────┼──► Base de datos
└─────────────────────────────┘
   DOS razones para cambiar = Viola el SRP
```

### La Solución

Aplicar la herramienta de **refactorización** para separar en:

```
┌──────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│    Video     │      │   VideoStats     │      │  VideoRepository     │
│  (datos)     │◄─────│  - get_length()  │      │  - save(video)       │
│              │      │  - get_size()    │      │  - update(video)     │
└──────────────┘      └──────────────────┘      │  - delete(title)     │
                       Una razón para            └──────────────────────┘
                       cambiar ✅                 Una razón para
                                                 cambiar ✅
```

### Mecánicas de Juego

- **Ciudad digital animada** con edificios y cables que reflejan el estado del código
- **Cables enredados** = código acoplado / **Cables ordenados** = SRP aplicado
- **Simulación del desastre**: tocá "Actualizar cálculo" y mirá cómo se rompe la ciudad
- **Código Python real** con resaltado de sintaxis en el panel lateral
- **Métricas en tiempo real**: Mantenibilidad, Estabilidad y Puntos

---

## 🚀 Instalación y Ejecución

### Requisitos

- Python 3.11 o superior
- pip

### Opción A — Script automático (recomendado)

**Linux / macOS:**
```bash
git clone https://github.com/natalia-cortese/code-architect.git
cd code-architect
chmod +x setup.sh && ./setup.sh
```

**Windows:**
```bat
git clone https://github.com/natalia-cortese/code-architect.git
cd code-architect
setup.bat
```

### Opción B — Make

```bash
make setup      # crea venv + instala dependencias
make run        # inicia el juego
make srp        # corre el ejemplo SRP en terminal (sin pygame)
make test       # ejecuta los tests
make test-cov   # ejecuta tests con coverage
make lint       # ejecuta linter flake8
make clean      # borra el venv
```

### Opción C — Manual

```bash
git clone https://github.com/natalia-cortese/code-architect.git
cd code-architect

python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt
python main.py
```

### Solo quiero ver el código Python del SRP (sin pygame)

```bash
source venv/bin/activate
python levels/srp_example.py
```

---

## 🧪 Testing

El proyecto usa **pytest** para tests y **pytest-cov** para coverage.

```bash
# Instalar dependencias de desarrollo
pip3 install -r requirements.txt

# Ejecutar tests
make test

# Ejecutar tests con coverage
make test-cov

# Ejecutar linter
make lint
```

### Estructura de tests

```
tests/
├── conftest.py              # Fixtures compartidos
├── test_constants.py        # Tests de constantes
├── test_state.py           # Tests de GameState
├── test_base_level.py      # Tests de interfaz BaseLevel
├── test_srp_level.py       # Tests del nivel SRP
├── test_ocp_level.py       # Tests del nivel OCP
└── test_lsp_level.py       # Tests del nivel LSP
```

### CI/CD

Los tests corren automáticamente en GitHub Actions en cada PR:
- Python 3.10, 3.11, 3.12
- Coverage reporting con Codecov
- Linting con flake8

---

## 🕹️ Controles

| Tecla / Acción | Función |
|----------------|---------|
| `Clic` | Interactuar con botones |
| `1` | Ver pestaña `video.py` (clase monstruo) |
| `2` | Ver pestaña `video_stats.py` |
| `3` | Ver pestaña `video_repo.py` |
| `ESC` | Cerrar modal / Salir |

---

## 📁 Estructura del Proyecto

```
code_architect/
│
├── main.py                   # Punto de entrada
├── requirements.txt
├── README.md
│
├── core/                     # Motor del juego
│   ├── constants.py          # Colores, dimensiones, constantes
│   ├── game.py               # Bucle principal y orquestación
│   ├── state.py              # Estado mutable del juego
│   ├── fonts.py              # Carga de fuentes
│   └── draw_utils.py         # Utilidades de dibujo
│
├── levels/                   # Contenido de cada nivel
│   ├── city_view.py          # Vista animada de la ciudad
│   └── srp_example.py        # Código Python educativo ejecutable
│
└── ui/                       # Componentes de interfaz
    ├── hud.py                # Barra superior con estadísticas
    ├── panel.py              # Panel lateral (código + acciones)
    ├── code_content.py       # Contenido de las pestañas de código
    ├── feedback.py           # Modal de feedback
    └── win_screen.py         # Pantalla de victoria
```

---

## 🎓 Elementos Didácticos

### ¿Por qué un videojuego?

1. **Aprender fallando**: Los jugadores ven *en tiempo real* qué sucede cuando el código está mal diseñado.
2. **Feedback inmediato**: Cada acción tiene consecuencias visibles (la ciudad se estabiliza o colapsa).
3. **Código real**: No son bloques de colores abstractos, son clases Python reales.
4. **Independencia de funciones**: El juego demuestra que con SRP podés cambiar una parte sin romper la otra.

### Dirigido a

- Estudiantes de programación (15+ años)
- Docentes que enseñan diseño orientado a objetos
- Cualquiera que quiera entender SOLID de forma práctica

---

## Hora de Jugar

https://natalia-cortese.github.io/thecodearchitect/game/

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! En especial:

- Nuevos niveles (O, L, I, D)
- Traducciones a otros idiomas
- Mejoras de sonido y música
- Soporte para pantallas más pequeñas

```bash
# Fork → rama → PR
git checkout -b feature/nivel-2-ocp
```

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir con atribución.

---

## 👤 Autor

Creado con ❤️ para enseñar programación de forma divertida.

*"El código limpio no se escribe, se refactoriza."*
