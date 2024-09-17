from enum import Enum


class Seleccion(Enum):
    Seleccionado = 0
    Deseleccionado = 1


class Respuesta(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    MS = 98  # Más de una selección
    NS = 99  # No seleccionado


class Cuestionario(Enum):
    C1 = 0
    C2 = 1
    C3 = 2
    C4 = 3
    MS = 98  # Más de una selección
    NS = 99  # No seleccionado

    def nombre(self):
        return self.name


class Seccion(Enum):
    Respuestas = 0
    Cuestionario = 1
