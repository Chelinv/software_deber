from sqlalchemy.orm import Session
from app.models.asignatura import Asignatura

class AsignaturaRepository:

    def crear(self, db: Session, asignatura: Asignatura):
        db.add(asignatura)
        db.commit()
        db.refresh(asignatura)
        return asignatura

    def listar(self, db: Session):
        return db.query(Asignatura).all()
