import tkinter as tk
from models.documentos import Documentos
from ui.search_bar import SearchBar
from ui.document_treeview import DocumentTreeview
from config import C

CHECK_ON = "\u2611"  # ☑


def _to_rows(documentos: list[Documentos]) -> list[tuple]:
    return [
        (doc.name, doc.date, doc.active, doc.belongs, doc.route)
        for doc in documentos
    ]


class DocumentPanel(tk.Frame):
    """Panel principal: barra de búsqueda + tabla de documentos."""

    def __init__(self, parent, documentos: list[Documentos], **kwargs):
        super().__init__(parent, bg=C.get("bg", "#1e1e2e"), **kwargs)
        self._show_inactive = False
        self._build(documentos)

    def _build(self, documentos: list[Documentos]):
        self._search = SearchBar(self, on_change=self._on_search)
        self._search.pack(fill="x", padx=10, pady=(10, 4))

        self._table = DocumentTreeview(self, on_deactivate=self._on_deactivate)
        self._table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        rows = _to_rows(documentos)

        self._table.load(rows)

        rows = _to_rows(documentos)

        self._refresh_view()

    # ------------------------------------------------------------------
    # API pública — llamada desde ProjectManagerApp
    # ------------------------------------------------------------------

    def set_show_inactive(self, show: bool):
        """Muestra u oculta los documentos inactivos."""
        self._show_inactive = show
        self._refresh_view()

    # ------------------------------------------------------------------
    # Lógica de filtro
    # ------------------------------------------------------------------

    def _refresh_view(self):
        query = self._search.get_query() if hasattr(self._search, "get_query") else ""
        shown = self._table.filter(query, show_inactive=self._show_inactive)
        active_total = self._table.count_active()
        self._search.set_count(shown, active_total)

    def _on_search(self, query: str):
        shown = self._table.filter(query, show_inactive=self._show_inactive)
        active_total = self._table.count_active()
        self._search.set_count(shown, active_total)

    def _on_deactivate(self, route: str, active: int = None):
        """Llamado cada vez que cambia el estado activo de un documento."""
        self._refresh_view()