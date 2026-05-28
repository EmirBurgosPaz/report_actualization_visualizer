import tkinter as tk
from models.documentos import Documentos
from ui.search_bar import SearchBar
from ui.document_treeview import DocumentTreeview
from config import C


def _to_rows(documentos: list[Documentos]) -> list[tuple]:
    return [
        (doc.name, doc.date, "✓" if doc.active else "✗", doc.belongs, doc.route)
        for doc in documentos
    ]


class DocumentPanel(tk.Frame):
    """Panel principal: barra de búsqueda + tabla de documentos."""

    def __init__(self, parent, documentos: list[Documentos], **kwargs):
        super().__init__(parent, bg=C.get("bg", "#1e1e2e"), **kwargs)
        self._build(documentos)

    def _build(self, documentos: list[Documentos]):
        # ── Barra de búsqueda ──────────────────────────────────────────
        self._search = SearchBar(self, on_change=self._on_search)
        self._search.pack(fill="x", padx=10, pady=(10, 4))

        # ── Tabla ──────────────────────────────────────────────────────
        self._table = DocumentTreeview(self)
        self._table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Cargar datos
        rows = _to_rows(documentos)
        self._table.load(rows)
        self._search.set_count(len(rows), len(rows))

    def _on_search(self, query: str):
        shown = self._table.filter(query)
        self._search.set_count(shown, self._table.total())
