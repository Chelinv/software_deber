from sqlalchemy.orm import Session
from app.services.asignatura_service import AsignaturaService

class AsignaturaController:

    def __init__(self):
        self.service = AsignaturaService()

    def crear(self, db: Session, nombre: str, codigo: str):
        return self.service.crear(db, nombre, codigo)

    def listar(self, db: Session):
        return self.service.listar(db)
