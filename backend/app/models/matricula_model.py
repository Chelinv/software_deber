from pydantic import BaseModel

class MatriculaBase(BaseModel):
    """Esquema base para una matrícula (datos comunes para entrada y salida)."""
    id: str  # Cambia int a str
    estudiante_id: int
    asignatura_id: int
    fecha_matricula: str  # Formato YYYY-MM-DD

class MatriculaIn(MatriculaBase):
    """Esquema para la entrada (POST/PUT) de una matrícula."""
    pass

class MatriculaOut(MatriculaBase):
    """Esquema para la salida (GET/POST Response) de una matrícula."""
    id: str  # Cambia int a str

    class Config:
        # Permite que el modelo se use con objetos ORM (útil más tarde)
        from_attributes = True