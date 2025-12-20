from sqlalchemy.orm import Session
from app.repositories.grupo_repository import GrupoRepository
from app.models.grupo import GrupoClase

class GrupoService:

    def __init__(self):
        self.repo = GrupoRepository()

    def crear(self, db: Session, nombre: str, aula: str,asignatura_id: int, docente_id: int):
        grupo = GrupoClase(
            nombre=nombre,
            aula=aula,
            asignatura_id=asignatura_id,
            docente_id=docente_id
        )
        return self.repo.crear(db, grupo)

    def listar(self, db: Session):
        return self.repo.listar(db)
