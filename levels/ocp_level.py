"""
Nivel 2 — Open/Closed Principle (OCP)
"Las clases deben estar ABIERTAS para extensión,
 pero CERRADAS para modificación."

Contexto del nivel:
  El sistema de descuentos de una tienda online crece sin parar.
  Cada vez que llega un nuevo tipo de descuento, el programador
  abre DiscountCalculator y agrega un nuevo `if/elif`.
  La clase se vuelve frágil: al tocarla para agregar "Black Friday",
  accidentalmente rompe el descuento "VIP" que ya funcionaba.

  La solución: extraer cada descuento a su propia clase que implementa
  una interfaz Discount, y hacer que DiscountCalculator solo dependa
  de esa interfaz. Nunca más hay que modificar DiscountCalculator.
"""

from levels.base_level import BaseLevel
from core.constants import *


# ─────────────────────────────────────────────────────────────
# Código Python para las tres pestañas del nivel 2
# Formato idéntico a code_content_srp.py
# ─────────────────────────────────────────────────────────────

CODE_OCP_BROKEN = [
    ([("# ⚠ Viola el OCP — cada nuevo descuento", "cm")], False),
    ([("# ⚠ requiere modificar esta clase.", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("DiscountCalculator", "broken"), (":", "default")], True),  # noqa: E501
    ([], False),
    ([("  def ", "kw"), ("calculate", "broken"),
      ("(self, order, type):", "default")], True),
    ([("    if ", "kw"), ("type == ", "default"), ('"student"', "st"), (":", "default")], False),  # noqa: E501
    ([("      return ", "kw"), ("order.total * ", "default"), ("0.1", "num")], False),  # noqa: E501
    ([], False),
    ([("    elif ", "kw"), ("type == ", "default"), ('"vip"', "st"), (":", "default")], False),  # noqa: E501
    ([("      return ", "kw"), ("order.total * ", "default"), ("0.2", "num")], False),  # noqa: E501
    ([], False),
    ([("    elif ", "kw"), ("type == ", "default"), ('"employee"', "st"), (":", "default")], False),  # noqa: E501
    ([("      return ", "kw"), ("order.total * ", "default"), ("0.3", "num")], False),  # noqa: E501
    ([], False),
    ([("    # ← Para agregar 'Black Friday'", "cm")], False),
    ([("    # ← hay que MODIFICAR esta clase.", "cm")], False),
    ([("    # ← Riesgo de romper lo que ya funciona.", "cm")], False),
    ([], False),
    ([("    return ", "kw"), ("0", "num")], False),
    ([], False),
    ([("# Cada if nuevo = una razón para romper", "cm")], False),
    ([("# algo que ya estaba funcionando. ⚠", "cm")], False),
]

CODE_OCP_INTERFACE = [
    ([("# ✅ discount.py — Interfaz base (cerrada)", "cm")], False),
    ([], False),
    ([("from ", "kw"), ("abc ", "default"), ("import ", "kw"),
      ("ABC, abstractmethod", "cls")], False),
    ([], False),
    ([("class ", "kw"), ("Discount", "fixed"), ("(", "default"),
      ("ABC", "cls"), ("):", "default")], False),
    ([('  """Interfaz: abierta para extensión,', "st")], False),
    ([('     cerrada para modificación."""', "st")], False),
    ([], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("apply", "fn"),
      ("(self, order) -> float:", "default")], False),
    ([("    ...", "default")], False),
    ([], False),
    ([("# ✅ Cada descuento es una clase nueva,", "cm")], False),
    ([("# ✅ no una modificación de la existente.", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("StudentDiscount", "fixed"),
      ("(", "default"), ("Discount", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("apply", "fn"),
      ("(self, order) -> float:", "default")], False),
    ([("    return ", "kw"), ("order.total * ", "default"), ("0.1", "num")], False),  # noqa: E501
    ([], False),
    ([("class ", "kw"), ("VIPDiscount", "fixed"),
      ("(", "default"), ("Discount", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("apply", "fn"),
      ("(self, order) -> float:", "default")], False),
    ([("    return ", "kw"), ("order.total * ", "default"), ("0.2", "num")], False),  # noqa: E501
    ([], False),
    ([("class ", "kw"), ("EmployeeDiscount", "fixed"),
      ("(", "default"), ("Discount", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("apply", "fn"),
      ("(self, order) -> float:", "default")], False),
    ([("    return ", "kw"), ("order.total * ", "default"), ("0.3", "num")], False),  # noqa: E501
]

CODE_OCP_CALCULATOR = [
    ([("# ✅ calculator.py — Nunca se modifica", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("DiscountCalculator", "fixed"), (":", "default")], False),  # noqa: E501
    ([('  """Cerrada para modificación.', "st")], False),
    ([('     Abierta para extensión vía Discount."""', "st")], False),
    ([], False),
    ([("  def ", "kw"), ("calculate", "fn"),
      ("(self, order, discount:", "default")], False),
    ([("           ", "default"), ("Discount) -> float:", "cls")], False),
    ([('    """Aplica cualquier descuento', "st")], False),
    ([('       sin conocer su tipo concreto."""', "st")], False),
    ([("    return ", "kw"), ("discount.apply(order)", "fn")], False),
    ([], False),
    ([("# ✅ Para agregar 'Black Friday':", "cm")], False),
    ([("# ✅ solo creás una clase nueva.", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("BlackFridayDiscount", "fixed"),
      ("(", "default"), ("Discount", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("apply", "fn"),
      ("(self, order) -> float:", "default")], False),
    ([("    return ", "kw"), ("order.total * ", "default"), ("0.5", "num")], False),  # noqa: E501
    ([], False),
    ([("# ✅ DiscountCalculator NO se tocó.", "cm")], False),
    ([("# ✅ Lo que existía no puede romperse.", "cm")], False),
    ([], False),
    ([("calc = ", "default"), ("DiscountCalculator", "fixed"), ("()", "default")], False),  # noqa: E501
    ([("calc.calculate(order, ", "default"),
      ("BlackFridayDiscount", "fixed"), ("())", "default")], False),
]

# ─────────────────────────────────────────────────────────────
# Pasos del nivel 2
# ─────────────────────────────────────────────────────────────
OCP_STEP_CHAOS      = 0   # clase monstruo con if/elif
OCP_STEP_INTERFACE  = 1   # interfaz Discount extraída
OCP_STEP_REFACTOR   = 2   # DiscountCalculator limpia
OCP_STEP_EXTEND     = 3   # BlackFridayDiscount agregada sin modificar


class OCPLevel(BaseLevel):
    level_number = 2
    title        = "THE CODE ARCHITECT"
    subtitle     = "NIVEL 02  //  OCP — OPEN/CLOSED PRINCIPLE"
    principle    = "O.C.P."

    def setup(self, state, panel, overlay, win):
        self.state   = state
        self.panel   = panel
        self.overlay = overlay
        self.win     = win

        # Estado específico del nivel — lo colgamos del state directamente
        state.interface_created  = False
        state.calculator_clean   = False
        state.extension_added    = False

        panel.configure(
            tabs={
                "broken":     "calculator.py ⚠",
                "interface":  "discount.py",
                "calculator": "calculator_v2.py",
            },
            buttons=[
                ("⚠  Simular: Agregar descuento 'Black Friday'",    "break",     "danger",  True),  # noqa: E501
                ("✂  Crear interfaz Discount (abstracción)",         "interface", "normal",  True),  # noqa: E501
                ("✂  Limpiar DiscountCalculator (cerrar para mod.)", "refactor",  "normal",  False),  # noqa: E501
                ("▶  Extender: agregar BlackFridayDiscount",         "extend",    "success", False),  # noqa: E501
            ],
            code_module="levels.ocp_level",   # este mismo módulo provee el código  # noqa: E501
        )

        # Inyectar el contenido de código directamente al panel
        panel.set_code_content({
            "broken":     CODE_OCP_BROKEN,
            "interface":  CODE_OCP_INTERFACE,
            "calculator": CODE_OCP_CALCULATOR,
        })

        panel.set_tab("broken")

    def handle_action(self, action: str):
        if action == "break":
            self._simulate_break()
        elif action == "interface":
            self._create_interface()
        elif action == "refactor":
            self._clean_calculator()
        elif action == "extend":
            self._add_extension()

    # ── Acciones ──────────────────────────────

    def _simulate_break(self):
        self.state.broken    = True
        self.state.stability = max(0, self.state.stability - 40)
        self.overlay.show(
            kind="danger",
            title="¡CÓDIGO FRÁGIL!",
            body=[
                "Abriste DiscountCalculator para agregar",
                "'Black Friday' y rompiste el descuento VIP.",
                "",
                "El problema: cada if/elif está acoplado.",
                "MODIFICAR la clase para extenderla",
                "siempre arriesga romper lo que funciona.",
                "",
                "El OCP dice: cerrada para MODIFICACIÓN,",
                "abierta para EXTENSIÓN.",
                "¡Creá una interfaz Discount!",
            ],
            btn_text="ENTENDIDO — VOY A REFACTORIZAR",
        )
        self.panel.set_tab("broken")

    def _create_interface(self):
        if self.state.interface_created:
            return
        self.state.interface_created = True
        self.state.step              = OCP_STEP_INTERFACE
        self.state.maintainability   = min(100, self.state.maintainability + 35)  # noqa: E501
        self.state.stability         = min(100, self.state.stability + 20)
        self.state.broken            = False
        self.state.add_score(200)
        self.panel.set_tab("interface")
        self.overlay.show(
            kind="success",
            title="Interfaz Discount CREADA  ✅",
            body=[
                "¡Bien! La clase abstracta Discount",
                "define el contrato: apply(order).",
                "",
                "Cada tipo de descuento es ahora",
                "una clase independiente que la implementa.",
                "",
                "StudentDiscount, VIPDiscount y",
                "EmployeeDiscount ya no conviven",
                "en un mismo bloque de if/elif.",
                "",
                "Siguiente: limpiá DiscountCalculator.",
            ],
            btn_text="CONTINUAR",
        )

    def _clean_calculator(self):
        if self.state.calculator_clean or not self.state.interface_created:
            return
        self.state.calculator_clean = True
        self.state.step             = OCP_STEP_REFACTOR
        self.state.maintainability  = min(100, self.state.maintainability + 35)
        self.state.stability        = min(100, self.state.stability + 20)
        self.state.add_score(200)
        self.panel.set_tab("calculator")
        self.overlay.show(
            kind="success",
            title="DiscountCalculator LIMPIA  ✅",
            body=[
                "¡Perfecto! DiscountCalculator ahora",
                "solo llama a discount.apply(order).",
                "",
                "No sabe qué tipo de descuento es.",
                "No tiene if/elif. No se rompe.",
                "",
                "Está CERRADA para modificación.",
                "Ahora demostrá que está ABIERTA",
                "para extensión: agregá Black Friday",
                "sin tocar ninguna clase existente.",
            ],
            btn_text="CONTINUAR",
        )

    def _add_extension(self):
        if self.state.extension_added or not self.state.calculator_clean:
            return
        self.state.extension_added  = True
        self.state.step             = OCP_STEP_EXTEND
        self.state.maintainability  = 100
        self.state.stability        = 100
        self.state.add_score(300)
        self.win.visible = True
