import json
import os


# Archivo donde se guardan las carpetas seleccionadas por el usuario.
# Se ubica junto a este módulo para no depender de un DATA_FILE externo.
_DEFAULT_REGISTRY_FILE = os.path.join(
    os.path.dirname(__file__), "folder_registry.json"
)


class FolderRegistry:
    """
    Persiste la lista de carpetas seleccionadas por el usuario entre sesiones.

    Uso básico
    ----------
        registry = FolderRegistry()
        registry.add("C:/mis_reportes")
        folders = registry.all()       # ['C:/mis_reportes']
        registry.remove("C:/mis_reportes")
    """

    def __init__(self, registry_file: str = None):
        self._file = registry_file or _DEFAULT_REGISTRY_FILE
        self._folders: list[str] = self._load()

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def all(self) -> list[str]:
        """Devuelve una copia de la lista de carpetas registradas."""
        return self._folders.copy()

    def add(self, path: str) -> bool:
        """
        Agrega una carpeta si existe en disco y no estaba ya registrada.

        Returns
        -------
        True  → se agregó y guardó.
        False → ya existía o la ruta no existe.
        """
        path = os.path.normpath(path)
        if path in self._folders:
            return False
        if not os.path.isdir(path):
            raise NotADirectoryError(f"La ruta no es una carpeta válida: {path}")
        self._folders.append(path)
        self._save()
        return True

    def remove(self, path: str) -> bool:
        """
        Elimina una carpeta del registro.

        Returns
        -------
        True  → se eliminó y guardó.
        False → la carpeta no estaba registrada.
        """
        path = os.path.normpath(path)
        if path not in self._folders:
            return False
        self._folders.remove(path)
        self._save()
        return True

    def clear(self):
        """Elimina todas las carpetas registradas."""
        self._folders.clear()
        self._save()

    def __contains__(self, path: str) -> bool:
        return os.path.normpath(path) in self._folders

    def __len__(self) -> int:
        return len(self._folders)

    # ------------------------------------------------------------------
    # Persistencia interna
    # ------------------------------------------------------------------

    def _load(self) -> list[str]:
        """Lee el archivo JSON; devuelve lista vacía si no existe o está corrupto."""
        if not os.path.exists(self._file):
            return []
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                # Filtrar rutas que ya no existen en disco (opcional: avisar al usuario)
                valid = [p for p in data if os.path.isdir(p)]
                if len(valid) != len(data):
                    # Hubo rutas inválidas → re-guardar lista limpia
                    self._folders = valid
                    self._save()
                return valid
        except (json.JSONDecodeError, OSError):
            pass
        return []

    def _save(self):
        """Escribe la lista actual en el archivo JSON."""
        os.makedirs(os.path.dirname(self._file) or ".", exist_ok=True)
        with open(self._file, "w", encoding="utf-8") as f:
            json.dump(self._folders, f, indent=2, ensure_ascii=False)