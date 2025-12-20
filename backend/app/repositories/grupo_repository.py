from sqlalchemy.orm import Session
from app.models.grupo import GrupoClase

class GrupoRepository:

    def crear(self, db: Session, grupo: GrupoClase):
        db.add(grupo)
        db.commit()
        db.refresh(grupo)
        return grupo

    def listar(self, db: Session):
        return db.query(GrupoClase).all()
