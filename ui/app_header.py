import tkinter as tk
from config import C


class AppHeader(tk.Frame):
    """Barra superior con título y texto de ayuda."""

    def __init__(self, parent,  **kwargs):
        super().__init__(parent, bg=C.get("header_bg", "#313244"), height=48, **kwargs)
        self.pack_propagate(False)
        self._build()
        self.app = parent.winfo_toplevel()


    def _build(self):
        tk.Label(
            self,
            text="📁  Documentos actuales",
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

        btn_agregar = tk.Button(
            self,
            text="+ Agregar Carpeta",
            command=self._abrir_selector_carpeta
        )
        btn_agregar.pack(side="right", padx=5)
    
    def _abrir_selector_carpeta(self):
        self.app.add_source_folder()