from pydantic import BaseModel, Field

class GrupoBase(BaseModel):
    nombre: str
    aula: str
    asignatura_id: str
    docente_id: str

class GrupoCreate(GrupoBase):
    pass

class GrupoInDB(GrupoBase):
    id: str = Field(alias="_id")
    
    class Config:
        from_attributes = True
        populate_by_name = True
