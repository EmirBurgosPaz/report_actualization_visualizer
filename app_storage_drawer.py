import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys 
import re

from storage.storage_drawer import StorageDrawer
from storage.folder_registry import FolderRegistry
from ui.app_header import AppHeader
from ui.document_panel import DocumentPanel
from config import C, KEYBOARD_KEYS


from models.splash_config import SplashConfig
from ui.splash_window import TechPlexusSplash

README_FILE = "README.md"

def get_current_version():
    """Busca el número de versión dentro del README.md usando Regex."""
    if not os.path.exists(README_FILE):
        print(f"Error: No se encontró el archivo {README_FILE}.")
        sys.exit(1)
    
    with open(README_FILE, "r", encoding="utf-8") as file:
        content = file.read()
        # Busca un patrón tipo 1.2.3 o v1.2.3
        match = re.search(r'(\d+\.\d+\.\d+)', content)
        if match:
            return match.group(1)
        else:
            print("Error: No se encontró un número de versión (x.x.x) en el README.md")
            sys.exit(1)

class ProjectManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Documentos actuales")
        self.configure(bg=C.get("bg", "#1e1e2e"))
        self._center_window(width=1550, height=880)

        # Ocultar mientras se construye para evitar flashes
        self.attributes("-alpha", 0)
        self.withdraw()

        self.minsize(800, 500)

        # ── Registro persistente de carpetas ──────────────────────────
        self._registry = FolderRegistry()

        documentos = self._load_all_documents()
        self._build_ui(documentos)

        self.bind(KEYBOARD_KEYS["escape"], lambda _: self.destroy())
        self.bind(KEYBOARD_KEYS["refresh"],  self._reload_documents)

        # Mostrar ventana ya construida
        self.update()
        self.update_idletasks()

        splash = TechPlexusSplash(
                    parent=self,
                    config=SplashConfig(),
                    colors=C,  # Tu diccionario de config
                    app_name="Gestor de reportes \n actualizados",
                    version=get_current_version(),
                    author="Información"
                )

        self.wait_window(splash)
        
        # Toplevel fantasma que tapa el flash
        blocker = tk.Toplevel(bg=C.get("bg", "#1e1e2e"))
        blocker.geometry(self.geometry())
        blocker.overrideredirect(True)
        blocker.lift()
        blocker.update()

        # Mostrar la ventana principal detrás del blocker
        self.deiconify()
        self.update()
        self.update_idletasks()

        # Ahora sí destruir el blocker
        blocker.destroy()
        self.attributes("-alpha", 1)
        self.lift()
        self.focus_force()

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

    def _reload_documents(self, event = None):
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