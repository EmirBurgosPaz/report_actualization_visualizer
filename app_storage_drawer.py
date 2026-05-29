import tkinter as tk
from tkinter import filedialog, messagebox

from storage.storage_drawer import StorageDrawer
from storage.folder_registry import FolderRegistry
from ui.app_header import AppHeader
from ui.document_panel import DocumentPanel
from config import C, KEYBOARD_KEYS


class ProjectManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Documentos actuales")
        self._center_window(width=1550, height=880)
        self.configure(bg=C.get("bg", "#1e1e2e"))
        self.minsize(800, 500)

        # Ocultar mientras se construye para evitar flashes
        self.attributes("-alpha", 0)
        self.withdraw()

        # ── Registro persistente de carpetas ──────────────────────────
        self._registry = FolderRegistry()

        documentos = self._load_all_documents()
        self._build_ui(documentos)

        self.bind(KEYBOARD_KEYS["escape"], lambda _: self.destroy())

        # Mostrar ventana ya construida
        self.update()
        self.update_idletasks()
        self.deiconify()
        self.attributes("-alpha", 1)

    # ------------------------------------------------------------------
    # Ventana
    # ------------------------------------------------------------------

    def _center_window(self, width: int, height: int):
        x = (self.winfo_screenwidth()  // 2) - (width  // 2)
        y = (self.winfo_screenheight() // 2) - (height  // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ------------------------------------------------------------------
    # Carga de documentos
    # ------------------------------------------------------------------

    def _load_documents(self, path: str) -> list:
        """Carga documentos de una carpeta específica."""
        repo = StorageDrawer(path)
        try:
            return repo.load_data()
        except Exception as exc:
            print(f"Error al cargar '{path}': {exc}")
            return []

    def _load_all_documents(self) -> list:
        """Carga documentos de todas las carpetas registradas."""
        all_documents = []
        for folder_path in self._registry.all():
            docs = self._load_documents(folder_path)
            for doc in docs:
                doc.belongs = folder_path
            all_documents.extend(docs)
        return all_documents

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self, documentos: list):
        AppHeader(self).pack(fill="x")
        self._panel = DocumentPanel(self, documentos)
        self._panel.pack(fill="both", expand=True)

    def set_show_inactive(self, show: bool):
        """Llamado desde AppHeader para mostrar/ocultar inactivos."""
        self._panel.set_show_inactive(show)

    def _reload_documents(self):
        """Recarga los documentos y refresca el DocumentPanel."""
        documentos = self._load_all_documents()
        for widget in self.winfo_children():
            if isinstance(widget, DocumentPanel):
                widget.destroy()
        self._panel = DocumentPanel(self, documentos)
        self._panel.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Gestión de carpetas (API pública para el header / menú)
    # ------------------------------------------------------------------

    def add_source_folder(self):
        """Abre diálogo para seleccionar carpeta y la persiste."""
        path = filedialog.askdirectory(title="Seleccionar carpeta de documentos")
        if not path:
            return

        try:
            added = self._registry.add(path)
        except NotADirectoryError as exc:
            messagebox.showerror("Carpeta inválida", str(exc))
            return

        if not added:
            messagebox.showinfo("Información", "Esa carpeta ya está en la lista.")
            return

        self._reload_documents()

    def remove_source_folder(self, path: str):
        """Elimina una carpeta del registro y recarga documentos."""
        removed = self._registry.remove(path)
        if removed:
            self._reload_documents()

    def get_source_folders(self) -> list[str]:
        """Devuelve la lista actual de carpetas registradas."""
        return self._registry.all()


# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = ProjectManagerApp()
    app.mainloop()