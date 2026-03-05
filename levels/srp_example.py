"""
srp_example.py — Ejemplo completo del Principio de Responsabilidad Única.

Este archivo contiene el código Python real que el juego enseña.
Podés ejecutarlo directamente para ver el antes/después del SRP.
"""

# ──────────────────────────────────────────────────────────────────────────────
# ❌ ANTES: Clase que viola el SRP
#    La clase Video tiene DOS responsabilidades:
#    1. Calcular estadísticas (get_full_length, get_total_size)
#    2. Persistir datos en la base de datos (save, update, delete)
#
#    Problema: si cambias la lógica de cálculo, podés romper la persistencia.
#    Dos razones para cambiar = viola el SRP.
# ──────────────────────────────────────────────────────────────────────────────

class VideoMonstruo:
    """
    ⚠  Esta clase viola el SRP.
    Tiene demasiadas responsabilidades en un solo lugar.
    """

    def __init__(self, title: str, clips: list):
        self.title = title
        self.clips = clips

    # Responsabilidad 1: Cálculo de estadísticas
    def get_full_length(self) -> float:
        return sum(clip["length"] for clip in self.clips)

    def get_total_size(self) -> float:
        return sum(clip["size"] for clip in self.clips)

    # Responsabilidad 2: Persistencia en base de datos
    def save(self):
        print(f"[DB] INSERT video '{self.title}'")

    def update(self):
        print(f"[DB] UPDATE video '{self.title}'")

    def delete(self):
        print(f"[DB] DELETE video '{self.title}'")


# ──────────────────────────────────────────────────────────────────────────────
# ✅ DESPUÉS: Aplicando el SRP
#    Separamos en tres clases, cada una con UNA sola responsabilidad.
# ──────────────────────────────────────────────────────────────────────────────

class Video:
    """
    ✅ Solo almacena los datos del video.
    No sabe nada de cálculo ni de base de datos.
    """

    def __init__(self, title: str, clips: list):
        self.title = title
        self.clips = clips


class VideoStats:
    """
    ✅ Responsabilidad única: calcular estadísticas.
    Solo cambia si la lógica de cálculo cambia.
    """

    def __init__(self, video: Video):
        self.video = video

    def get_full_length(self) -> float:
        """Retorna la duración total en segundos."""
        return sum(clip["length"] for clip in self.video.clips)

    def get_total_size(self) -> float:
        """Retorna el tamaño total en MB."""
        return sum(clip["size"] for clip in self.video.clips)


class VideoRepository:
    """
    ✅ Responsabilidad única: persistencia en base de datos.
    Solo cambia si la forma de guardar datos cambia.
    """

    def save(self, video: Video) -> None:
        """Inserta un video nuevo en la base de datos."""
        print(f"[DB] INSERT video '{video.title}'")

    def update(self, video: Video) -> None:
        """Actualiza un video existente."""
        print(f"[DB] UPDATE video '{video.title}'")

    def delete(self, title: str) -> None:
        """Elimina un video por su título."""
        print(f"[DB] DELETE video '{title}'")


# ──────────────────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    clips = [
        {"length": 120, "size": 50.0},
        {"length": 200, "size": 80.5},
        {"length": 90,  "size": 35.2},
    ]

    print("=" * 50)
    print("❌ CLASE MONSTRUO (viola SRP)")
    print("=" * 50)
    v_mono = VideoMonstruo("Tutorial Python", clips)
    print(f"  Duración: {v_mono.get_full_length()} seg")
    print(f"  Tamaño:   {v_mono.get_total_size()} MB")
    v_mono.save()
    v_mono.update()

    print()
    print("=" * 50)
    print("✅ DESPUÉS DE APLICAR EL SRP")
    print("=" * 50)
    video = Video("Tutorial Python", clips)
    stats = VideoStats(video)
    repo  = VideoRepository()

    print(f"  Duración: {stats.get_full_length()} seg")
    print(f"  Tamaño:   {stats.get_total_size()} MB")
    repo.save(video)
    repo.update(video)

    print()
    print("Ventaja del SRP:")
    print("  → Puedo cambiar VideoStats sin tocar VideoRepository")
    print("  → Puedo cambiar la DB sin romper los cálculos")
    print("  → Cada clase es independiente y fácil de testear")
