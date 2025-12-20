from pydantic import BaseModel
from typing import Optional

class AsignaturaBase(BaseModel):
    nombre: str
    codigo: str

class AsignaturaCreate(AsignaturaBase):
    pass

class AsignaturaOut(AsignaturaBase):
    id: str

    class Config:
        from_attributes = True
