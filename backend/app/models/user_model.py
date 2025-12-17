# app/models/user_model.py
from pydantic import BaseModel

class UserBase(BaseModel):
    """Esquema base para un usuario (datos comunes para entrada y salida)."""
    nombre: str
    email: str
    rol: str # Administrador, Docente, Estudiante, Padre

class UserIn(UserBase):
    """Esquema para la entrada (POST/PUT), incluye campos sensibles como la contraseña."""
    password: str

class UserOut(UserBase):
    """Esquema para la salida (GET/POST Response), no incluye la contraseña."""
    id: str

    class Config:
        # Permite que el modelo se use con objetos ORM (útil más tarde)
        from_attributes = True