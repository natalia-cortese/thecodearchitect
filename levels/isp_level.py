"""
Nivel 4 — Interface Segregation Principle (ISP)
"Los clientes no deben depender de interfaces que no usan."

Contexto del nivel:
  Una fotocopiadora moderna necesita implementar IMachine con
  print(), scan(), fax(), copy(). Un Robot simple que solo sabe
  copiar debe implementar todos los métodos, aunque no los use.

  La solución:拆分 la interfaz grande en interfaces más pequeñas
  y específicas. Cada máquina solo implementa lo que necesita.
"""

from levels.base_level import BaseLevel
from core.constants import *


CODE_ISP_BROKEN = [
    ([("# ⚠ Viola el ISP — IMachine es demasiado grande", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("IMachine", "broken"), ("(", "default"), ("ABC", "cls"), ("):", "default")], True),
    ([('  """Interface para TODAS las máquinas."""', "st")], False),
    ([], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("print", "broken"), ("(self, doc):", "default")], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("scan", "broken"), ("(self, doc):", "default")], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("fax", "broken"), ("(self, doc):", "default")], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("copy", "broken"), ("(self, doc):", "default")], False),
    ([], False),
    ([("class ", "kw"), ("RobotCopier", "broken"), ("(", "default"), ("IMachine", "cls"), ("):", "default")], True),
    ([("  '\"Solo sabe copiar. ¿Por qué debe implementar fax?'", "st")], False),
    ([], False),
    ([("  def ", "kw"), ("print", "broken"), ("(self, doc):", "default")], False),
    ([('    raise NotImplementedError("No sé imprimir")', "st")], False),
    ([("  def ", "kw"), ("scan", "broken"), ("(self, doc):", "default")], False),
    ([('    raise NotImplementedError("No sé escanear")', "st")], False),
    ([("  def ", "kw"), ("fax", "broken"), ("(self, doc):", "default")], False),
    ([('    raise NotImplementedError("No sé enviar fax")', "st")], False),
    ([("  def ", "kw"), ("copy", "fn"), ("(self, doc):", "default")], False),
    ([('    print("Copiando...")', "st")], False),
]

CODE_ISP_SEPARATED = [
    ([("# ✅ Interfaces pequeñas y específicas", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("IPrinter", "fixed"), ("(", "default"), ("ABC", "cls"), ("):", "default")], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("print", "fn"), ("(self, doc):", "default")], False),
    ([], False),
    ([("class ", "kw"), ("IScanner", "fixed"), ("(", "default"), ("ABC", "cls"), ("):", "default")], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("scan", "fn"), ("(self, doc):", "default")], False),
    ([], False),
    ([("class ", "kw"), ("ICopier", "fixed"), ("(", "default"), ("ABC", "cls"), ("):", "default")], False),
    ([("  @", "kw"), ("abstractmethod", "fn")], False),
    ([("  def ", "kw"), ("copy", "fn"), ("(self, doc):", "default")], False),
    ([], False),
    ([("# ✅ Cada máquina solo implementa lo que necesita", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("RobotCopier", "fixed"), ("(", "default"), ("ICopier", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("copy", "fn"), ("(self, doc):", "default")], False),
    ([('    print("Copiando...")', "st")], False),
    ([], False),
    ([("class ", "kw"), ("MultiFunctionPrinter", "fixed"), ("(", "default"), ("IPrinter", "cls"), ("(", "default")], False),
    ([("                      ", "default"), ("IScanner", "cls"), ("):", "default")], False),
    ([("  def ", "kw"), ("print", "fn"), ("(self, doc):", "default")], False),
    ([('    print("Imprimiendo...")', "st")], False),
    ([("  def ", "kw"), ("scan", "fn"), ("(self, doc):", "default")], False),
    ([('    print("Escaneando...")', "st")], False),
]

CODE_ISP_CLIENT = [
    ([("# ✅ Cliente depende solo de lo que usa", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("Office", "fixed"), (":", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("__init__", "fn"), ("(self, copier:", "default"), ("ICopier", "cls"), ("):", "default")], False),
    ([("    self.copier = copier", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("make_copy", "fn"), ("(self, doc):", "default")], False),
    ([("    self.copier.copy(doc)", "default")], False),
    ([], False),
    ([("# ✅ RobotCopier implementa ICopier — compatible.", "cm")], False),
    ([("# ✅ Si agregás scanner, solo cambia el tipo.", "cm")], False),
    ([], False),
    ([("robot = ", "default"), ("RobotCopier", "fixed"), ("()", "default")], False),
    ([("office = ", "default"), ("Office", "fixed"), ("(robot)", "default")], False),
    ([("office.make_copy", "fixed"), ("(doc)", "default")], False),
    ([], False),
    ([("# ISP en resumen:", "cm")], False),
    ([("# → Interfaces GRANDES = acoplamiento innecesario", "cm")], False),
    ([("# → Interfaces PEQUEÑAS = flexibilidad", "cm")], False),
]


ISP_STEP_CHAOS     = 0
ISP_STEP_SEPARATE  = 1
ISP_STEP_REFACTOR  = 2


class ISPLevel(BaseLevel):
    level_number = 4
    title        = "THE CODE ARCHITECT"
    subtitle     = "NIVEL 04  //  ISP — INTERFACE SEGREGATION PRINCIPLE"
    principle    = "I.S.P."

    def setup(self, state, panel, overlay, win):
        self.state   = state
        self.panel   = panel
        self.overlay = overlay
        self.win     = win

        state.interface_created = False
        state.client_refactored = False

        panel.configure(
            tabs={
                "broken":    "machine.py ⚠",
                "separate":  "interfaces.py",
                "client":    "office.py",
            },
            buttons=[
                (
                    "⚠  Simular: RobotCopier hereda IMachine",
                    "break", "danger", True,
                ),
                (
                    "✂  Separar interfaces pequeñas",
                    "separate", "normal", True,
                ),
                (
                    "▶  Refactorizar cliente Office",
                    "refactor", "success", False,
                ),
            ],
            code_module="levels.isp_level",
        )

        panel.set_code_content({
            "broken":    CODE_ISP_BROKEN,
            "separate":  CODE_ISP_SEPARATED,
            "client":    CODE_ISP_CLIENT,
        })

        panel.set_tab("broken")

    def handle_action(self, action: str):
        if action == "break":
            self._simulate_break()
        elif action == "separate":
            self._separate_interfaces()
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
            title="¡INTERFAZ INFLADA!",
            body=[
                "IMachine tiene print, scan, fax, copy.",
                "RobotCopier solo sabe copiar.",
                "",
                "Pero está forzado a implementar",
                "todos los métodos (aunque no los use).",
                "",
                "El ISP dice: los clientes no deben",
                "depender de métodos que no usan.",
                "",
                "¡Separémos IMachine en interfaces",
                "pequeñas y específicas!",
            ],
            btn_text="ENTENDIDO — VOY A REFACTORIZAR",
        )
        self.panel.set_tab("broken")

    def _separate_interfaces(self):
        if self.state.interface_created:
            return
        self.state.interface_created = True
        self.state.step             = ISP_STEP_SEPARATE
        self.state.maintainability  = min(100, self.state.maintainability + 40)
        self.state.stability        = min(100, self.state.stability + 25)
        self.state.broken           = False
        self.state.add_score(250)
        self.panel.set_tab("separate")
        self.overlay.show(
            kind="success",
            title="Interfaces SEPARADAS  ✅",
            body=[
                "¡Bien! IPrinter, IScanner, ICopier",
                "son interfaces pequeñas y específicas.",
                "",
                "RobotCopier ahora solo implementa",
                "ICopier, que tiene exactamente",
                "lo que necesita: copy().",
                "",
                "MultiFunctionPrinter puede usar",
                "IPrinter + IScanner juntos.",
                "",
                "Siguiente: refactorizar el cliente.",
            ],
            btn_text="CONTINUAR",
        )

    def _refactor_client(self):
        if self.state.client_refactored or not self.state.interface_created:
            return
        self.state.client_refactored = True
        self.state.step             = ISP_STEP_REFACTOR
        self.state.maintainability  = 100
        self.state.stability        = 100
        self.state.add_score(350)
        self.win.visible = True
