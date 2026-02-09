"""
Modelos Pydantic para usuarios
"""
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    rol: str
    nombre: Optional[str] = None

class UsuarioUpdate(BaseModel):
    email: Optional[str] = None
    rol: Optional[str] = None
    nombre: Optional[str] = None
    password: Optional[str] = None
    
    class Config:
        extra = "ignore"

class UsuarioOut(BaseModel):
    id: str
    email: str
    rol: str
    nombre: Optional[str] = None
    
    class Config:
        from_attributes = True
