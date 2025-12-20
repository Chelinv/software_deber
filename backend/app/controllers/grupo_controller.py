from sqlalchemy.orm import Session
from app.services.grupo_service import GrupoService

class GrupoController:

    def __init__(self):
        self.service = GrupoService()

    def crear(self, db: Session, nombre: str, aula: str,asignatura_id: int, docente_id: int):
        return self.service.crear(
            db, nombre, aula, asignatura_id, docente_id
        )

    def listar(self, db: Session):
        return self.service.listar(db)
