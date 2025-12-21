from pydantic import BaseModel

class CalificacionBase(BaseModel):
    """Esquema base para una calificación (datos comunes para entrada y salida)."""
    id: str
    estudiante_id: int
    asignatura_id: int
    calificacion: float  # Valor numérico de la calificación
    fecha_evaluacion: str  # Formato YYYY-MM-DD

class CalificacionIn(CalificacionBase):
    """Esquema para la entrada (POST/PUT) de una calificación."""
    pass

class CalificacionOut(CalificacionBase):
    """Esquema para la salida (GET/POST Response) de una calificación."""
    id: str

    class Config:
        # Permite que el modelo se use con objetos ORM (útil más tarde)
        from_attributes = True