from pydantic import BaseModel, Field, model_validator
from typing import Optional

class MatriculaBase(BaseModel):
    """Esquema base para una matrícula (datos comunes para entrada y salida)."""
    estudiante_id: str
    asignatura_ids: Optional[list[str]] = None  # Múltiples asignaturas por matrícula
    asignatura_id: Optional[str] = None  # Campo legado para compatibilidad
    fecha_matricula: str  # Formato YYYY-MM-DD

    @model_validator(mode='after')
    def convert_asignatura_id_to_ids(self):
        """Convierte asignatura_id (singular) a asignatura_ids (lista) para compatibilidad."""
        if self.asignatura_id and not self.asignatura_ids:
            # Si solo existe asignatura_id, convertir a lista
            self.asignatura_ids = [self.asignatura_id]
        elif not self.asignatura_ids:
            self.asignatura_ids = []
        # Limpiar el campo legado
        self.asignatura_id = None
        return self

class MatriculaCreate(MatriculaBase):
    """Esquema para la entrada (POST/PUT) de una matrícula."""
    pass

class MatriculaOut(BaseModel):
    """Esquema para la salida (GET/POST Response) de una matrícula."""
    id: str = Field(validation_alias="_id")
    estudiante_id: str
    asignatura_ids: list[str] = Field(default_factory=list)  # Con valor por defecto
    asignatura_id: Optional[str] = None  # Para compatibilidad con datos antiguos
    fecha_matricula: str

    @model_validator(mode='after')
    def convert_asignatura_id_to_ids(self):
        """Convierte asignatura_id (singular) a asignatura_ids (lista) para compatibilidad."""
        if self.asignatura_id and not self.asignatura_ids:
            self.asignatura_ids = [self.asignatura_id]
        elif not self.asignatura_ids:
            self.asignatura_ids = []
        return self

    class Config:
        from_attributes = True
        populate_by_name = True
