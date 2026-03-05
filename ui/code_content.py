"""
Contenido de código Python para las pestañas del panel.
Formato: lista de (tokens, is_broken_line)
  tokens: lista de (texto, estilo)
  estilos: 'kw', 'cls', 'fn', 'st', 'cm', 'num', 'broken', 'fixed', 'default'
"""

# ─────────────────────────────────────────────
# video.py  —  Clase monstruo (viola SRP)
# ─────────────────────────────────────────────
CODE_BROKEN = [
    # (tokens, broken_line)
    ([("# ⚠ CLASE MONSTRUO — Viola el SRP", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("Video", "cls"), (":", "default")], False),
    ([("  def ", "kw"), ("__init__", "fn"),
      ("(self, title, clips):", "default")], False),
    ([("    self", "default"), (".title = title", "default")], False),
    ([("    self", "default"), (".clips = clips", "default")], False),
    ([], False),
    ([("  # 👁 Responsabilidad 1: Cálculo", "cm")], False),
    ([("  def ", "kw"), ("get_full_length", "broken"),
      ("(self):", "default")], True),
    ([("    return ", "kw"), ("sum", "fn"),
      ("(clip.length", "default")], False),
    ([("      for clip in self.clips)", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("get_total_size", "broken"),
      ("(self):", "default")], True),
    ([("    return ", "kw"), ("sum", "fn"),
      ("(clip.size", "default")], False),
    ([("      for clip in self.clips)", "default")], False),
    ([], False),
    ([("  # 💾 Responsabilidad 2: Persistencia", "cm")], False),
    ([("  def ", "kw"), ("save", "broken"), ("(self):", "default")], True),
    ([("    db = ", "default"), ("connect_db", "fn"), ("()", "default")], False),
    ([("    db.insert(self)", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("update", "broken"), ("(self):", "default")], True),
    ([("    db = ", "default"), ("connect_db", "fn"), ("()", "default")], False),
    ([("    db.update(self)", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("delete", "broken"), ("(self):", "default")], True),
    ([("    db = ", "default"), ("connect_db", "fn"), ("()", "default")], False),
    ([("    db.delete(self.title)", "default")], False),
    ([], False),
    ([("# ⚠ Si cambias el cálculo → rompe la DB", "cm")], False),
    ([("# ⚠ Si cambias la DB → rompe el cálculo", "cm")], False),
]

# ─────────────────────────────────────────────
# video_stats.py  —  Solo lógica de cálculo
# ─────────────────────────────────────────────
CODE_STATS = [
    ([("# ✅ video_stats.py — Una sola responsabilidad", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("VideoStats", "fixed"), (":", "default")], False),
    ([('  """Calcula estadísticas del video."""', "st")], False),
    ([], False),
    ([("  # ✅ Solo cambia si la lógica", "cm")], False),
    ([("  #    de cálculo cambia.", "cm")], False),
    ([], False),
    ([("  def ", "kw"), ("__init__", "fn"),
      ("(self, video):", "default")], False),
    ([("    self", "default"), (".video = video", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("get_full_length", "fn"),
      ("(self):", "default")], False),
    ([('    """Tiempo total de reproducción."""', "st")], False),
    ([("    return ", "kw"), ("sum", "fn"),
      ("(c.length", "default")], False),
    ([("      for c in self.video.clips)", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("get_total_size", "fn"),
      ("(self):", "default")], False),
    ([('    """Tamaño total en MB."""', "st")], False),
    ([("    return ", "kw"), ("sum", "fn"),
      ("(c.size", "default")], False),
    ([("      for c in self.video.clips)", "default")], False),
    ([], False),
    ([("# Uso:", "cm")], False),
    ([("# stats = ", "cm"), ("VideoStats", "fixed"), ("(video)", "cm")], False),
    ([("# stats.get_full_length()", "cm")], False),
]

# ─────────────────────────────────────────────
# video_repo.py  —  Solo persistencia
# ─────────────────────────────────────────────
CODE_REPO = [
    ([("# ✅ video_repo.py — Una sola responsabilidad", "cm")], False),
    ([], False),
    ([("class ", "kw"), ("VideoRepository", "fixed"), (":", "default")], False),
    ([('  """Persiste videos en la base de datos."""', "st")], False),
    ([], False),
    ([("  # ✅ Solo cambia si la DB cambia.", "cm")], False),
    ([], False),
    ([("  def ", "kw"), ("save", "fn"),
      ("(self, video):", "default")], False),
    ([('    """Inserta un video nuevo."""', "st")], False),
    ([("    db = ", "default"), ("connect_db", "fn"), ("()", "default")], False),
    ([("    db.insert(video)", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("update", "fn"),
      ("(self, video):", "default")], False),
    ([('    """Actualiza un video existente."""', "st")], False),
    ([("    db = ", "default"), ("connect_db", "fn"), ("()", "default")], False),
    ([("    db.update(video)", "default")], False),
    ([], False),
    ([("  def ", "kw"), ("delete", "fn"),
      ("(self, title):", "default")], False),
    ([('    """Elimina un video por título."""', "st")], False),
    ([("    db = ", "default"), ("connect_db", "fn"), ("()", "default")], False),
    ([("    db.delete(title)", "default")], False),
    ([], False),
    ([("# Uso:", "cm")], False),
    ([("# repo = ", "cm"), ("VideoRepository", "fixed"), ("()", "cm")], False),
    ([("# repo.save(video)", "cm")], False),
]
