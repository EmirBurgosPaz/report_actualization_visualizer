import os
import json
from datetime import datetime
from models.documentos import Documentos
from config import DATA_FILE


class StorageDrawer:
    """Lee los archivos que se encuentran en una carpeta."""
    def __init__(self, filepath: str = None):
        self.filepath = filepath
    
    def load_data(self):
        
        lista_documentos = []

        # Iterar sobre todos los elementos en la carpeta
        for ruta_directorio, subcarpetas, archivos in os.walk(self.filepath):
        
        # Iterar sobre los archivos encontrados en el directorio actual
            for nombre_archivo in archivos:
                
                if nombre_archivo.startswith('~$') or nombre_archivo.endswith('.tmp'):
                    continue

                ruta_completa = os.path.join(ruta_directorio, nombre_archivo)

                # Obtener el timestamp de la última modificación y convertirlo a formato legible
                timestamp_modificacion = os.path.getmtime(ruta_completa)
                fecha_modificacion = datetime.fromtimestamp(timestamp_modificacion).strftime('%Y-%m-%d %H:%M:%S')

                # Crear el diccionario para el archivo actual
                # Nota: Se corrigió el error tipográfico de "Nombre doumento" a "Nombre documento"
                diccionario_archivo = Documentos(
                    route= ruta_completa,
                    name= nombre_archivo,
                    date= fecha_modificacion,
                    active= 0,
                    belongs=  ""
                )

                lista_documentos.append(diccionario_archivo)

        return lista_documentos

    def read_data(self):
        with open(DATA_FILE, 'r', encoding='utf-8') as archivo:
            datos_leidos = json.load(archivo)
        
        lista_documentos_recuperados = []
        
        for item in datos_leidos:
            documento = Documentos(
                route=item["Ruta_documento"],
                name=item["Nombre_documento"],
                date=item["Fecha_modificacion"],
                active=item["Activo"],
                belongs=item["Pertenece"]
            )
            lista_documentos_recuperados.append(documento)
        
        return lista_documentos_recuperados
    
    @staticmethod
    def save_data(self, documentos: list[Documentos]):
        lista_diccionarios = [doc.to_dict() for doc in documentos]

        with open(DATA_FILE, 'w', encoding='utf-8') as archivo:
            json.dump(lista_diccionarios, archivo, indent=4, ensure_ascii=False)