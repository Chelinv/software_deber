from pydantic import BaseModel, Field

class CalificacionBase(BaseModel):
    """Esquema base para una calificación (datos comunes para entrada y salida)."""
    estudiante_id: str
    asignatura_id: str
    calificacion: float  # Valor numérico de la calificación
    fecha_evaluacion: str  # Formato YYYY-MM-DD

class CalificacionCreate(CalificacionBase):
    """Esquema para la entrada (POST/PUT) de una calificación."""
    pass

class CalificacionOut(CalificacionBase):
    """Esquema para la salida (GET/POST Response) de una calificación."""
    id: str = Field(alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True
