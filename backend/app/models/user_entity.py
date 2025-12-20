import enum

class RolEnum(str, enum.Enum):
    administrador = "Administrador"
    docente = "Docente"
    estudiante = "Estudiante"
    padre = "Padre"
