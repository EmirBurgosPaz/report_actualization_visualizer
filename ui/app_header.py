import tkinter as tk
from config import C


class AppHeader(tk.Frame):
    """Barra superior con título, toggle de inactivos y texto de ayuda."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=C.get("header_bg", "#313244"), height=48, **kwargs)
        self.pack_propagate(False)
        self.app = parent.winfo_toplevel()
        self._show_inactive = False  # estado del toggle
        self._build()

    def _build(self):
        tk.Label(
            self,
            text="Documentos actuales",
            bg=C.get("header_bg", "#313244"),
            fg=C.get("fg", "#cdd6f4"),
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).pack(side="left", padx=16, pady=10)

        tk.Label(
            self,
            text="ESC para cerrar",
            bg=C.get("header_bg", "#313244"),
            fg=C.get("fg_dim", "#6c7086"),
            font=("Segoe UI", 9),
        ).pack(side="right", padx=16)

        tk.Button(
            self,
            text="+ Agregar Carpeta",
            command=self._abrir_selector_carpeta,
        ).pack(side="right", padx=5)

        self._toggle_btn = tk.Button(
            self,
            text="Mostrar inactivos",
            command=self._toggle_inactive,
        )
        self._toggle_btn.pack(side="right", padx=5)

    # ------------------------------------------------------------------

    def _abrir_selector_carpeta(self):
        self.app.add_source_folder()

    def _toggle_inactive(self):
        self._show_inactive = not self._show_inactive
        label = "Ocultar inactivos" if self._show_inactive else "Mostrar inactivos"
        self._toggle_btn.config(text=label)
        self.app.set_show_inactive(self._show_inactive)