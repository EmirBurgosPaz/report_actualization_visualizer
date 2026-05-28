import tkinter as tk
from tkinter import ttk
from config import C


COLUMNS = {
    "name":    {"header": "Nombre",             "width": 280, "anchor": "w",      "stretch": False},
    "date":    {"header": "Fecha modificación",  "width": 155, "anchor": "center", "stretch": False},
    "active":  {"header": "Activo",              "width":  60, "anchor": "center", "stretch": False},
    "belongs": {"header": "Pertenece",           "width": 180, "anchor": "w",      "stretch": False},
    "route":   {"header": "Ruta completa",       "width": 600, "anchor": "w",      "stretch": True},
}


def _apply_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Docs.Treeview",
        background=C.get("tree_bg", "#181825"),
        foreground=C.get("fg", "#cdd6f4"),
        fieldbackground=C.get("tree_bg", "#181825"),
        rowheight=26,
        font=("Segoe UI", 9),
    )
    style.configure(
        "Docs.Treeview.Heading",
        background=C.get("header_bg", "#313244"),
        foreground=C.get("fg", "#cdd6f4"),
        font=("Segoe UI", 9, "bold"),
        relief="flat",
    )
    style.map(
        "Docs.Treeview",
        background=[("selected", C.get("select_bg", "#45475a"))],
    )


class DocumentTreeview(tk.Frame):
    """Treeview con scrollbars para mostrar una lista de Documentos."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=C.get("bg", "#1e1e2e"), **kwargs)
        _apply_style()
        self._build()

    def _build(self):
        col_ids = list(COLUMNS.keys())

        self._tree = ttk.Treeview(
            self,
            columns=col_ids,
            show="headings",
            selectmode="browse",
            style="Docs.Treeview",
        )

        for col_id, cfg in COLUMNS.items():
            self._tree.heading(
                col_id,
                text=cfg["header"],
                command=lambda c=col_id: self._sort_by(c, False),
            )
            self._tree.column(
                col_id,
                width=cfg["width"],
                anchor=cfg["anchor"],
                stretch=cfg["stretch"],
            )

        vsb = ttk.Scrollbar(self, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._rows: list[tuple] = []

    # ------------------------------------------------------------------
    def load(self, rows: list[tuple]):
        """Carga una lista de tuplas (name, date, active, belongs, route)."""
        self._rows = rows
        self._render(rows)

    def filter(self, query: str) -> int:
        """Filtra las filas por query y devuelve el número de resultados."""
        if not query:
            filtered = self._rows
        else:
            filtered = [r for r in self._rows if any(query in str(c).lower() for c in r)]
        self._render(filtered)
        return len(filtered)

    def total(self) -> int:
        return len(self._rows)

    # ------------------------------------------------------------------
    def _render(self, rows: list[tuple]):
        self._tree.delete(*self._tree.get_children())
        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self._tree.insert("", "end", values=row, tags=(tag,))
        self._tree.tag_configure("even", background=C.get("tree_bg",  "#181825"))
        self._tree.tag_configure("odd",  background=C.get("tree_alt", "#1e1e2e"))

    def _sort_by(self, col: str, reverse: bool):
        idx = list(COLUMNS.keys()).index(col)
        self._rows = sorted(self._rows, key=lambda r: str(r[idx]).lower(), reverse=reverse)
        self._render(self._rows)
        self._tree.heading(col, command=lambda: self._sort_by(col, not reverse))
