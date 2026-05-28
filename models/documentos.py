"""
models/project.py — Definición de la entidad Project.
Solo describe QUÉ es un proyecto.
"""

from dataclasses import dataclass



@dataclass
class Documentos:
    route: str
    name: str
    date: str
    active: int
    belongs: str

    def to_dict(self) -> dict:
        return { "Ruta_documento": self.route, "Nombre_documento": self.name, "Fecha_modificacion":  self.date, "Activo": self.active , "Pertenece": self.belongs}

    @staticmethod
    def from_dict(d: dict) -> "reports":
        return Documentos( route=d["Ruta_documento"],name=d["Nombre_documento"],date=d["Fecha_modificacion"],active=d["Activo"], belongs=d["Pertenece"] )
