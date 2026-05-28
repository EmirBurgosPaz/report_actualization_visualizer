import tkinter as tk
from tkinter import messagebox

from storage.storage_drawer import StorageDrawer
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

        documentos = self._load_documents(r"C:\Owncloud\Trabajo diario")
        self._build_ui(documentos)

        self.bind(KEYBOARD_KEYS["escape"], lambda _: self.destroy())

        # Mostrar ventana ya construida
        self.update()
        self.update_idletasks()
        self.deiconify()
        self.attributes("-alpha", 1)

    # ------------------------------------------------------------------
    def _center_window(self, width: int, height: int):
        x = (self.winfo_screenwidth()  // 2) - (width  // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _load_documents(self, path: str) -> list:
        repo = StorageDrawer(path)
        try:
            return repo.load_data()
        except Exception as exc:
            self.after(200, lambda: messagebox.showerror(
                "Error al cargar",
                f"No se pudieron leer los archivos:\n{exc}",
            ))
            return []

    def _build_ui(self, documentos: list):
        AppHeader(self).pack(fill="x")
        DocumentPanel(self, documentos).pack(fill="both", expand=True)


# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = ProjectManagerApp()
    app.mainloop()
