from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class GrupoClase(Base):
    __tablename__ = "grupos_clase"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    aula = Column(String, nullable=False)

    asignatura_id = Column(Integer, ForeignKey("asignaturas.id"))
    docente_id = Column(Integer, ForeignKey("usuarios.id"))
