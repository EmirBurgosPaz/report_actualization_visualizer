import tkinter as tk

from storage.storage_drawer import StorageDrawer
from config import C, KEYBOARD_KEYS

class ProjectManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Documentos actuales")
        
        app_width = 1550
        app_height = 880
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (app_width // 2)
        y = (screen_height // 2) - (app_height // 2)
        
        self.geometry(f"{app_width}x{app_height}+{x}+{y}")
        self.configure(bg=C["bg"])
        self.minsize(800, 500)

        main = tk.Frame(self, bg=C["bg"])
        main.pack(side="left", fill="both", expand=True)
        
        # --- NUEVO: Configuración crítica para eliminar flashes ---
        self.attributes('-alpha', 0)
        self.withdraw()

        repo = StorageDrawer("C:\Owncloud\Trabajo diario")
 

        self.bind(KEYBOARD_KEYS["escape"], self._on_close)
        
        # Forzar un ciclo completo de actualización
        self.update()
        self.update_idletasks()
        self.deiconify()              # Restaura la ventana después de withdraw()
        self.attributes('-alpha', 1)

    def _on_close(self, event=None):
        self.destroy()

if __name__ == "__main__":
    app = ProjectManagerApp()
    app.mainloop()