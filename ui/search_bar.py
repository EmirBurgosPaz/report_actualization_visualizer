import tkinter as tk
from config import C


class SearchBar(tk.Frame):
    """Barra de búsqueda con label, entry y contador de resultados."""

    def __init__(self, parent, on_change: callable, **kwargs):
        super().__init__(parent, bg=C.get("bg", "#1e1e2e"), **kwargs)
        self._on_change = on_change
        self._build()

    def _build(self):
        tk.Label(
            self,
            text="🔍 Buscar:",
            bg=C.get("bg", "#1e1e2e"),
            fg=C.get("fg", "#cdd6f4"),
            font=("Segoe UI", 10),
        ).pack(side="left", padx=(0, 6))

        self._var = tk.StringVar()
        self._var.trace_add("write", self._on_write)

        tk.Entry(
            self,
            textvariable=self._var,
            bg=C.get("entry_bg", "#313244"),
            fg=C.get("fg", "#cdd6f4"),
            insertbackground=C.get("fg", "#cdd6f4"),
            relief="flat",
            font=("Segoe UI", 10),
            width=40,
        ).pack(side="left", ipady=4)

        self._count_label = tk.Label(
            self,
            text="",
            bg=C.get("bg", "#1e1e2e"),
            fg=C.get("fg_dim", "#6c7086"),
            font=("Segoe UI", 9),
        )
        self._count_label.pack(side="right", padx=8)

    def _on_write(self, *_):
        self._on_change(self._var.get().strip().lower())

    def set_count(self, shown: int, total: int):
        self._count_label.config(text=f"{total} de {shown} documentos")
    
    def get_query(self) -> str:
        return self._var.get().strip().lower()
