from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RelacionPadreHijoBase(BaseModel):
    padre_id: str  # ID del usuario con rol "Padre"
    estudiante_id: str  # ID del usuario con rol "Estudiante"

class RelacionPadreHijoCreate(RelacionPadreHijoBase):
    pass

class RelacionPadreHijoOut(RelacionPadreHijoBase):
    id: str
    fecha_creacion: Optional[str] = None
    
    class Config:
        from_attributes = True
