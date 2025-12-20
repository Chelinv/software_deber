from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class RolEnum(str, enum.Enum):
    administrador = "Administrador"
    docente = "Docente"
    estudiante = "Estudiante"
    padre = "Padre"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)
