import os
import json
from datetime import datetime
from models.documentos import Documentos
from config import DATA_FILE


class StorageDrawer:
    """Lee los archivos que se encuentran en una carpeta."""

    def __init__(self, filepath: str = None):
        self.filepath = filepath

    def load_data(self) -> list[Documentos]:
        """
        Lee archivos del disco y fusiona el campo 'active' desde DATA_FILE.
        Si un archivo ya fue guardado antes, se respeta su estado activo.
        Si es nuevo (no está en el JSON), se inicializa en active=0 y se guarda.
        """
        # 1. Cargar estados previos del JSON (por ruta)
        estados = self._load_estados()

        # 2. Leer archivos del disco
        lista_documentos = []
        nuevos = []  # archivos que no estaban en el JSON

        for ruta_directorio, _, archivos in os.walk(self.filepath):
            for nombre_archivo in archivos:

                if nombre_archivo.startswith('~$') or nombre_archivo.endswith('.tmp'):
                    continue

                ruta_completa = os.path.join(ruta_directorio, nombre_archivo)
                timestamp_modificacion = os.path.getmtime(ruta_completa)
                fecha_modificacion = datetime.fromtimestamp(timestamp_modificacion).strftime('%Y-%m-%d %H:%M:%S')

                # Respetar estado previo; si es nuevo usar 0
                active = estados.get(ruta_completa, None)
                es_nuevo = active is None
                if es_nuevo:
                    active = 0

                doc = Documentos(
                    route=ruta_completa,
                    name=nombre_archivo,
                    date=fecha_modificacion,
                    active=active,
                    belongs=""
                )
                lista_documentos.append(doc)

                if es_nuevo:
                    nuevos.append(doc)

        # 3. Persistir documentos nuevos en el JSON
        if nuevos:
            self._append_nuevos(nuevos)

        return lista_documentos

    def read_data(self) -> list[Documentos]:
        with open(DATA_FILE, 'r', encoding='utf-8') as archivo:
            datos_leidos = json.load(archivo)

        return [
            Documentos(
                route=item["Ruta_documento"],
                name=item["Nombre_documento"],
                date=item["Fecha_modificacion"],
                active=item["Activo"],
                belongs=item["Pertenece"]
            )
            for item in datos_leidos
        ]

    def save_data(self, documentos: list[Documentos]):
        lista_diccionarios = [doc.to_dict() for doc in documentos]
        with open(DATA_FILE, 'w', encoding='utf-8') as archivo:
            json.dump(lista_diccionarios, archivo, indent=4, ensure_ascii=False)

    @staticmethod
    def update_active(route: str, active: int):

        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)


        encontrado = False
        for item in datos:
            if item.get("Ruta_documento") == route:
                item["Activo"] = active
                encontrado = True
                break
            

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    @staticmethod
    def _load_estados() -> dict[str, int]:
        """Devuelve {ruta: active} leyendo DATA_FILE. Retorna {} si no existe."""
        if not os.path.exists(DATA_FILE):
            return {}
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return {item["Ruta_documento"]: item["Activo"] for item in datos}
        except (json.JSONDecodeError, KeyError):
            return {}

    @staticmethod
    def _append_nuevos(nuevos: list[Documentos]):
        """Agrega documentos nuevos al JSON sin sobreescribir los existentes."""
        datos = []
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
            except (json.JSONDecodeError, OSError):
                datos = []

        rutas_existentes = {item["Ruta_documento"] for item in datos}
        for doc in nuevos:
            if doc.route not in rutas_existentes:
                datos.append(doc.to_dict())

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)