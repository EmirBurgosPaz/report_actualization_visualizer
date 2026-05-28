import tkinter as tk
from config import C


class AppHeader(tk.Frame):
    """Barra superior con título y texto de ayuda."""

    def __init__(self, parent, title: str = "📁  Documentos actuales", hint: str = "ESC para cerrar", **kwargs):
        super().__init__(parent, bg=C.get("header_bg", "#313244"), height=48, **kwargs)
        self.pack_propagate(False)
        self._build(title, hint)

    def _build(self, title: str, hint: str):
        tk.Label(
            self,
            text=title,
            bg=C.get("header_bg", "#313244"),
            fg=C.get("fg", "#cdd6f4"),
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).pack(side="left", padx=16, pady=10)

        tk.Label(
            self,
            text=hint,
            bg=C.get("header_bg", "#313244"),
            fg=C.get("fg_dim", "#6c7086"),
            font=("Segoe UI", 9),
        ).pack(side="right", padx=16)
