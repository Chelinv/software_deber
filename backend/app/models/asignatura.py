from pydantic import BaseModel, Field

class AsignaturaBase(BaseModel):
    nombre: str
    codigo: str

class AsignaturaCreate(AsignaturaBase):
    pass

class AsignaturaInDB(AsignaturaBase):
    id: str = Field(alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True
