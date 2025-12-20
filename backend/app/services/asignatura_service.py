from sqlalchemy.orm import Session
from app.repositories.asignatura_repository import AsignaturaRepository
from app.models.asignatura import Asignatura

class AsignaturaService:

    def __init__(self):
        self.repo = AsignaturaRepository()

    def crear(self, db: Session, nombre: str, codigo: str):
        asignatura = Asignatura(nombre=nombre, codigo=codigo)
        return self.repo.crear(db, asignatura)

    def listar(self, db: Session):
        return self.repo.listar(db)
