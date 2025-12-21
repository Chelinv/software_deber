from pydantic import BaseModel, Field

class MatriculaBase(BaseModel):
    """Esquema base para una matrícula (datos comunes para entrada y salida)."""
    estudiante_id: int
    asignatura_id: int
    fecha_matricula: str  # Formato YYYY-MM-DD

class MatriculaCreate(MatriculaBase):
    """Esquema para la entrada (POST/PUT) de una matrícula."""
    pass

class MatriculaOut(MatriculaBase):
    """Esquema para la salida (GET/POST Response) de una matrícula."""
    id: str = Field(alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True
