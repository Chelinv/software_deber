from pydantic import BaseModel
from typing import Optional

class GrupoBase(BaseModel):
    nombre: str
    aula: str
    asignatura_id: str
    docente_id: str

class GrupoCreate(GrupoBase):
    pass

class GrupoOut(GrupoBase):
    id: str

    class Config:
        from_attributes = True
