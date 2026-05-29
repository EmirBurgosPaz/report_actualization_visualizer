import tkinter as tk
from tkinter import ttk
from config import C


COLUMNS = {
    "name":    {"header": "Nombre",              "width": 280, "anchor": "w",      "stretch": False},
    "date":    {"header": "Fecha modificación",  "width": 155, "anchor": "center", "stretch": False},
    "active":  {"header": "Activo",              "width":  60, "anchor": "center", "stretch": False},
    "belongs": {"header": "Pertenece",           "width": 180, "anchor": "w",      "stretch": False},
    "route":   {"header": "Ruta completa",       "width": 600, "anchor": "w",      "stretch": True},
}

ACTIVE_COL_INDEX = list(COLUMNS.keys()).index("active")  # 2

CHECK_ON  = "\u2611"  # ☑
CHECK_OFF = "\u2610"  # ☐


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

    def __init__(self, parent, on_deactivate=None, **kwargs):
        super().__init__(parent, bg=C.get("bg", "#1e1e2e"), **kwargs)
        self._on_deactivate = on_deactivate
        _apply_style()
        self._build()

    # ------------------------------------------------------------------
    # Construcción
    # ------------------------------------------------------------------

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

        self._tree.bind("<ButtonRelease-1>", self._on_click)
        self._rows: list[tuple] = []

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def load(self, rows: list[tuple]):
        """Carga una lista de tuplas (name, date, active, belongs, route)."""
        self._rows = [self._normalize(r) for r in rows]

    def filter(self, query: str, show_inactive: bool = False) -> int:
        """
        Filtra por query y por estado activo.
        Devuelve el número de filas visibles.
        """
        rows = self._rows

        # 1. Filtrar inactivos si corresponde
        if not show_inactive:
            rows = [r for r in rows if r[ACTIVE_COL_INDEX] == CHECK_ON]

        # 2. Filtrar por búsqueda
        if query:
            rows = [r for r in rows if any(query.lower() in str(c).lower() for c in r)]

        self._render(rows)
        return len(rows)

    def total(self) -> int:
        return len(self._rows)

    def count_active(self) -> int:
        """Devuelve cuántos documentos están activos (☑) en el master."""
        return sum(1 for r in self._rows if r[ACTIVE_COL_INDEX] == CHECK_ON)

    # ------------------------------------------------------------------
    # Checkbox / toggle
    # ------------------------------------------------------------------

    def _on_click(self, event: tk.Event):
        region = self._tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        col_id    = self._tree.identify_column(event.x)
        col_index = int(col_id.lstrip("#")) - 1

        if col_index != ACTIVE_COL_INDEX:
            return

        item_id = self._tree.identify_row(event.y)
        if not item_id:
            return

        self._toggle_active(item_id)

    def _toggle_active(self, item_id: str):
        """
        CHECK_OFF -> CHECK_ON  (activo=1): marca en uso y persiste.
        CHECK_ON  -> CHECK_OFF (activo=0): desmarca en uso y persiste.
        """
        from storage.storage_drawer import StorageDrawer

        values    = list(self._tree.item(item_id, "values"))
        is_active = values[ACTIVE_COL_INDEX] == CHECK_ON

        new_symbol = CHECK_OFF if is_active else CHECK_ON
        new_active  = 0        if is_active else 1

        values[ACTIVE_COL_INDEX] = new_symbol
        self._tree.item(item_id, values=values)
        self._sync_master(item_id, values)

        route = values[-1]
        StorageDrawer.update_active(route, new_active)

        if callable(self._on_deactivate):
            self._on_deactivate(route, new_active)

    def _sync_master(self, item_id: str, new_values: list):
        route = new_values[-1]
        self._rows = [
            tuple(new_values) if r[-1] == route else r
            for r in self._rows
        ]

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(row: tuple) -> tuple:
        lst = list(row)
        raw = lst[ACTIVE_COL_INDEX]

        if isinstance(raw, bool):
            lst[ACTIVE_COL_INDEX] = CHECK_ON if raw else CHECK_OFF
        elif str(raw) in ("1", "True", CHECK_ON):
            lst[ACTIVE_COL_INDEX] = CHECK_ON
        else:
            lst[ACTIVE_COL_INDEX] = CHECK_OFF
        return tuple(lst)

    def _render(self, rows: list[tuple]):
        from datetime import datetime
    
        today = datetime.today().date()
        date_col = list(COLUMNS.keys()).index("date")
    
        self._tree.delete(*self._tree.get_children())
        for i, row in enumerate(rows):
            is_active = row[ACTIVE_COL_INDEX] == CHECK_ON
    
            # Determinar si la fecha es anterior a hoy
            try:
                row_date = datetime.strptime(row[date_col], "%Y-%m-%d %H:%M:%S").date()
                is_outdated = row_date < today
            except (ValueError, TypeError):
                is_outdated = False
    
            if is_active and is_outdated:
                tag = "outdated"
            elif i % 2 == 0:
                tag = "even"
            else:
                tag = "odd"
    
            self._tree.insert("", "end", values=row, tags=(tag,))
    
        self._tree.tag_configure("even",     background=C.get("tree_bg",  "#181825"))
        self._tree.tag_configure("odd",      background=C.get("tree_alt", "#1e1e2e"))
        self._tree.tag_configure("outdated", background=C.get("outdated", "#4a1c1c"))

    def _sort_by(self, col: str, reverse: bool):
        idx = list(COLUMNS.keys()).index(col)
        self._rows = sorted(self._rows, key=lambda r: str(r[idx]).lower(), reverse=reverse)
        col_keys = list(COLUMNS.keys())
        current_shown = [
            self._tree.item(i, "values")
            for i in self._tree.get_children()
        ]
        current_shown_sorted = sorted(current_shown, key=lambda r: str(r[idx]).lower(), reverse=reverse)
        self._render(current_shown_sorted)
        self._tree.heading(col, command=lambda: self._sort_by(col, not reverse))