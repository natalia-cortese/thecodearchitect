"""
Nivel 3 — Liskov Substitution Principle (LSP)
"Los objetos de una subclase deben poder sustituir
 a los objetos de la clase base sin romper el programa."

Contexto del nivel:
  Un sistema de entregas usa una clase Bird para distintos tipos.
  El código principal llama bird.fly() asumiendo que todas las aves vuelan.
  Pero Penguin es un Bird que no puede volar — ¡explota en runtime!

  La solución: separar la capacidad de volar en una interfaz propia,
  para que solo las aves que realmente vuelan la implementen.
"""

from levels.base_level import BaseLevel
from core.constants import *


CODE_LSP_BROKEN = [
    ([("# ⚠ Viola el LSP — Penguin NO puede volar", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("Bird", "broken"), (":", "default")], True),
    ([('  """Todas las aves pueden volar y nadar."""', "st")], False),
    ([], False),
    ([("  def ", "kw"), ("fly", "broken"), ("(self):", "default")], False),
    ([('    raise ", "default'), ("NotImplementedError", "cls"), ('"', "default")], False),
    ([], False),
    ([("  def ", "kw"), ("swim", "fn"), ("(self):", "default")], False),
    ([('    print("Nadando...")', "st")], False),
    ([], False),
    ([("class ", "kw"), ("Penguin", "broken"), ("(", "default"), ("Bird", "cls"), ("):", "default")], True),  # noqa: E501
    ([('  """Un pingüino es un ave... pero no vuela."""', "st")], False),
    ([], False),
    ([("  def ", "kw"), ("fly", "broken"), ("(self):", "default")], False),
    ([('    raise Exception("¡No puedo volar!")', "st")], False),
    ([], False),
    ([("# Código que usa Bird sin saber el tipo:", "cm")], False),
    ([("def ", "kw"), ("deliver", "fn"), ("(package, bird):", "default")], False),
    ([("  bird.fly()  # ← ¡Explota con Penguin!", "cm")], False),
]

CODE_LSP_FIX = [
    ([("# ✅ Separamos la capacidad de volar", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("Bird", "fixed"), (":", "default")], False),
    ([('  """Solo comportamiento común a todas."""', "st")], False),
    ([], False),
    ([("  def ", "kw"), ("swim", "fn"), ("(self):", "default")], False),
    ([('    print("Nadando...")', "st")], False),
    ([], False),
    ([("class ", "kw"), ("Flyer", "cls"), ("(", "default"), ("Bird", "cls"), ("):", "default")], False),
    ([('  """Interface: aves que saben volar."""', "st")], False),
    ([], False),
    ([("  def ", "kw"), ("fly", "fn"), ("(self):", "default")], False),
    ([('    raise ", "default'), ("NotImplementedError", "cls"), ('"', "default")], False),
    ([], False),
    ([("class ", "kw"), ("Penguin", "fixed"), ("(", "default"), ("Bird", "cls"), ("):", "default")], False),  # noqa: E501
    ([("  def ", "kw"), ("swim", "fn"), ("(self):", "default")], False),
    ([('    print("Nadando en el océano...")', "st")], False),
    ([], False),
    ([("# ✅ Penguin NO hereda fly() — es Flyer lo que se rompe.", "cm")], False),
    ([("# ✅ El código cliente usa Flyer para entregas.", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("Eagle", "fixed"), ("(", "default"), ("Flyer", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("fly", "fn"), ("(self):", "default")], False),
    ([('    print("Volando alto...")', "st")], False),
]

CODE_LSP_CLIENT = [
    ([("# ✅ Código cliente usa abstracción correcta", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("DeliveryService", "fixed"), (":", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("__init__", "fn"), ("(self, flyer:", "default"), ("Flyer", "cls"), ("):", "default")], False),
    ([("    self.flyer = flyer", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("deliver", "fn"), ("(self, package):", "default")], False),
    ([("    self.flyer.fly()", "default")], False),
    ([('    print(f"Entregando {package}")', "st")], False),
    ([], False),
    ([("# ✅ Solo pájaros que vuelan se registran aquí.", "cm")], False),
    ([("# ✅ Penguin no puede pasar como Flyer — error en lint.", "cm")], False),
    ([], False),
    ([("eagle = ", "default"), ("Eagle", "fixed"), ("()", "default")], False),
    ([("service = ", "default"), ("DeliveryService", "fixed"), ("(eagle)", "default")], False),
    ([("service.deliver", "fixed"), ("(package)", "default")], False),
    ([], False),
    ([("# Si intentás pasar Penguin como Flyer:", "cm")], False),
    ([("# penguin = Penguin()", "cm")], False),
    ([("# service = DeliveryService(penguin)  # TypeError en lint ✅", "cm")], False),
]


LSP_STEP_CHAOS     = 0
LSP_STEP_SEPARATE  = 1
LSP_STEP_REFACTOR  = 2


class LSPLevel(BaseLevel):
    level_number = 3
    title        = "THE CODE ARCHITECT"
    subtitle     = "NIVEL 03  //  LSP — LISKOV SUBSTITUTION PRINCIPLE"
    principle    = "L.S.P."

    def setup(self, state, panel, overlay, win):
        self.state   = state
        self.panel   = panel
        self.overlay = overlay
        self.win     = win

        state.interface_created = False
        state.client_refactored = False

        panel.configure(
            tabs={
                "broken":    "bird.py ⚠",
                "separate":  "separated.py",
                "client":    "delivery.py",
            },
            buttons=[
                (
                    "⚠  Simular: Penguin intenta volar",
                    "break", "danger", True,
                ),
                (
                    "✂  Separar interfaz Flyer",
                    "separate", "normal", True,
                ),
                (
                    "▶  Refactorizar DeliveryService",
                    "refactor", "success", False,
                ),
            ],
            code_module="levels.lsp_level",
        )

        panel.set_code_content({
            "broken":    CODE_LSP_BROKEN,
            "separate":  CODE_LSP_FIX,
            "client":    CODE_LSP_CLIENT,
        })

        panel.set_tab("broken")

    def handle_action(self, action: str):
        if action == "break":
            self._simulate_break()
        elif action == "separate":
            self._separate_interface()
        elif action == "refactor":
            self._refactor_client()

    def update_panel_buttons(self, state):
        st = state
        self.panel.buttons[0].enabled = not st.broken
        self.panel.buttons[1].enabled = not st.interface_created
        self.panel.buttons[2].enabled = (
            st.interface_created and not st.client_refactored
        )

    def _simulate_break(self):
        self.state.broken    = True
        self.state.stability = max(0, self.state.stability - 35)
        self.overlay.show(
            kind="danger",
            title="¡ERROR EN RUNTIME!",
            body=[
                "Penguin heredó fly() de Bird",
                "pero no puede implementarlo.",
                "",
                "Cuando el código hace bird.fly(),",
                "espera que funcione para CUALQUIER Bird.",
                "Pero Penguin rompe esa expectativa.",
                "",
                "El LSP dice: si S es subtipo de T,",
                "entonces objetos de tipo T pueden",
                "reemplazarse por S sin alterar",
                "las propiedades del programa.",
                "",
                "¡Separemos Flyer de Bird!",
            ],
            btn_text="ENTENDIDO — VOY A REFACTORIZAR",
        )
        self.panel.set_tab("broken")

    def _separate_interface(self):
        if self.state.interface_created:
            return
        self.state.interface_created = True
        self.state.step             = LSP_STEP_SEPARATE
        self.state.maintainability  = min(100, self.state.maintainability + 40)
        self.state.stability        = min(100, self.state.stability + 25)
        self.state.broken           = False
        self.state.add_score(250)
        self.panel.set_tab("separate")
        self.overlay.show(
            kind="success",
            title="Flyer SEPARADO  ✅",
            body=[
                "¡Bien! Ahora Bird solo tiene",
                "comportamiento común (swim).",
                "",
                "Flyer es una clase separada",
                "que hereda de Bird Y añade fly().",
                "",
                "Penguin es Bird, pero NO Flyer.",
                "El compilador o linter detectaría",
                "si intentás asignar Penguin a Flyer.",
                "",
                "Siguiente: refactorizar el cliente.",
            ],
            btn_text="CONTINUAR",
        )

    def _refactor_client(self):
        if self.state.client_refactored or not self.state.interface_created:
            return
        self.state.client_refactored = True
        self.state.step             = LSP_STEP_REFACTOR
        self.state.maintainability  = 100
        self.state.stability        = 100
        self.state.add_score(350)
        self.win.visible = True
