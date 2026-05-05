"""
Nivel 5 — Dependency Inversion Principle (DIP)
"Los módulos de alto nivel no deben depender de módulos de bajo nivel.
 Ambos deben depender de abstracciones."

Contexto del nivel:
  Un sistema de notificaciones usa EmailSender directamente.
  Si querés cambiar a SMS, debés modificar la clase NotificationService.
  
  La solución: crear una interfaz NotificationSender y que
  NotificationService dependa de ella, no de EmailSender.
"""

from levels.base_level import BaseLevel
from core.constants import *


CODE_DIP_BROKEN = [
    ([("# ⚠ Viola el DIP — NotificationService depende de EmailSender", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("EmailSender", "broken"), (":", "default")], True),
    ([("  def ", "kw"), ("send", "broken"), ("(self, msg):", "default")], False),
    ([('    print(f"Email: {msg}")', "st")], False),
    ([], False),
    ([("class ", "kw"), ("NotificationService", "broken"), (":", "default")], True),
    ([('  """Depende directamente de EmailSender."""', "st")], False),
    ([], False),
    ([("  def ", "kw"), ("__init__", "fn"), ("(self):", "default")], False),
    ([("    self.sender = ", "default"), ("EmailSender", "broken"), ("()", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("notify", "broken"), ("(self, msg):", "default")], False),
    ([("    self.sender.", "default"), ("send", "broken"), ("(msg)", "default")], False),
    ([], False),
    ([("# Uso:", "cm")], False),
    ([("svc = ", "default"), ("NotificationService", "broken"), ("()", "default")], False),
    ([("svc.", "default"), ("notify", "broken"), ('("Hola")', "default")], False),
]

CODE_DIP_FIX = [
    ([("# ✅ Ambos dependen de abstracción NotificationSender", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("NotificationSender", "cls"), ("(", "default"), ("ABC", "cls"), ("):", "default")], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("send", "fn"), ("(self, msg):", "default")], False),
    ([], False),
    ([("class ", "kw"), ("EmailSender", "fixed"), ("(", "default"), ("NotificationSender", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("send", "fn"), ("(self, msg):", "default")], False),
    ([('    print(f"Email: {msg}")', "st")], False),
    ([], False),
    ([("class ", "kw"), ("SMSSender", "fixed"), ("(", "default"), ("NotificationSender", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("send", "fn"), ("(self, msg):", "default")], False),
    ([('    print(f"SMS: {msg}")', "st")], False),
    ([], False),
    ([("class ", "kw"), ("NotificationService", "fixed"), (":", "default")], False),
    ([('  """Depende de abstracción, no de EmailSender."""', "st")], False),
    ([], False),
    ([("  def ", "kw"), ("__init__", "fn"), ("(self, sender:", "default"), ("NotificationSender", "cls"), ("):", "default")], False),
    ([("    self.sender = sender", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("notify", "fn"), ("(self, msg):", "default")], False),
    ([("    self.sender.", "default"), ("send", "fn"), ("(msg)", "default")], False),
    ([], False),
    ([("# ✅ Podés cambiar el sender sin tocar NotificationService", "cm")], False),
]

CODE_DIP_CLIENT = [
    ([("# ✅ Cliente puede inyectar cualquier implementación", "cm")], False),
    ([], False),
    ([("email = ", "default"), ("EmailSender", "fixed"), ("()", "default")], False),
    ([("svc = ", "default"), ("NotificationService", "fixed"), ("(email)", "default")], False),
    ([("svc.", "default"), ("notify", "fixed"), ('("Hola por email")', "default")], False),
    ([], False),
    ([("sms = ", "default"), ("SMSSender", "fixed"), ("()", "default")], False),
    ([("svc2 = ", "default"), ("NotificationService", "fixed"), ("(sms)", "default")], False),
    ([("svc2.", "default"), ("notify", "fixed"), ('("Hola por SMS")', "default")], False),
    ([], False),
    ([("# La clase NotificationService NO cambia", "cm")], False),
    ([("# Solo cambia la inyección en el cliente", "cm")], False),
]


DIP_STEP_CHAOS    = 0
DIP_STEP_ABSTRACT = 1
DIP_STEP_INJECT   = 2


class DIPLevel(BaseLevel):
    level_number = 5
    title        = "THE CODE ARCHITECT"
    subtitle     = "NIVEL 05  //  DIP — DEPENDENCY INVERSION PRINCIPLE"
    principle    = "D.I.P."

    def setup(self, state, panel, overlay, win):
        self.state   = state
        self.panel   = panel
        self.overlay = overlay
        self.win     = win

        state.interface_created = False
        state.client_refactored = False

        panel.configure(
            tabs={
                "broken":    "notification.py ⚠",
                "fixed":    "notification_fixed.py",
                "client":  "app.py",
            },
            buttons=[
                (
                    "⚠  Simular: NotificationService depende de EmailSender",
                    "break", "danger", True,
                ),
                (
                    "✂  Crear abstracción NotificationSender",
                    "abstract", "normal", True,
                ),
                (
                    "▶  Inyectar dependencia en cliente",
                    "inject", "success", False,
                ),
            ],
            code_module="levels.dip_level",
        )

        panel.set_code_content({
            "broken":    CODE_DIP_BROKEN,
            "fixed":    CODE_DIP_FIX,
            "client":  CODE_DIP_CLIENT,
        })

        panel.set_tab("broken")

    def handle_action(self, action: str):
        if action == "break":
            self._simulate_break()
        elif action == "abstract":
            self._create_abstract()
        elif action == "inject":
            self._inject_dependency()

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
            title="¡ACOPLAMIENTO DIRECTO!",
            body=[
                "NotificationService crea EmailSender internamente.",
                "Si querés usar SMS, debés modificar la clase.",
                "",
                "El DIP dice: los módulos de alto nivel",
                "no deben depender de módulos de bajo nivel.",
                "",
                "Ambos deben depender de abstracciones.",
                "",
                "¡Creemos NotificationSender como interfaz!",
            ],
            btn_text="ENTENDIDO — VOY A REFACTORIZAR",
        )
        self.panel.set_tab("broken")

    def _create_abstract(self):
        if self.state.interface_created:
            return
        self.state.interface_created = True
        self.state.step             = DIP_STEP_ABSTRACT
        self.state.maintainability  = min(100, self.state.maintainability + 40)
        self.state.stability        = min(100, self.state.stability + 25)
        self.state.broken           = False
        self.state.add_score(250)
        self.panel.set_tab("fixed")
        self.overlay.show(
            kind="success",
            title="ABSTRACCIÓN CREADA  ✅",
            body=[
                "¡Bien! NotificationSender es una interfaz (ABC).",
                "",
                "EmailSender y SMSSender implementan esa interfaz.",
                "",
                "NotificationService ahora recibe un NotificationSender",
                "por inyección, no crea uno específico.",
                "",
                "Siguiente: inyectar dependencia en el cliente.",
            ],
            btn_text="CONTINUAR",
        )

    def _inject_dependency(self):
        if self.state.client_refactored or not self.state.interface_created:
            return
        self.state.client_refactored = True
        self.state.step             = DIP_STEP_INJECT
        self.state.maintainability  = 100
        self.state.stability        = 100
        self.state.add_score(350)
        self.win.visible = True
