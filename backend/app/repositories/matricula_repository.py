from typing import List, Optional
from app.models.matricula_model import MatriculaBase

class MatriculaRepository:
    def __init__(self, db):
        self.collection = db["matriculas"]

    def get_all_matriculas(self) -> List[MatriculaBase]:
        """Obtiene todas las matrículas."""
        docs = self.collection.find()
        matriculas = []
        for doc in docs:
            doc['id'] = str(doc.pop('_id'))  # Mapea _id a id como str
            matriculas.append(MatriculaBase(**doc))
        return matriculas

    def get_matricula_by_id(self, matricula_id: str) -> Optional[MatriculaBase]:
        """Obtiene una matrícula por ID."""
        from bson import ObjectId
        doc = self.collection.find_one({"_id": ObjectId(matricula_id)})
        if doc:
            doc['id'] = str(doc.pop('_id'))
            return MatriculaBase(**doc)
        return None

    def create_matricula(self, matricula: MatriculaBase) -> MatriculaBase:
        """Crea una nueva matrícula."""
        doc = matricula.dict(exclude={"id"})
        result = self.collection.insert_one(doc)
        matricula.id = str(result.inserted_id)
        return matricula

    def update_matricula(self, matricula_id: str, updated_matricula: MatriculaBase) -> Optional[MatriculaBase]:
        """Actualiza una matrícula."""
        from bson import ObjectId
        doc = updated_matricula.dict(exclude={"id"})
        result = self.collection.update_one({"_id": ObjectId(matricula_id)}, {"$set": doc})
        if result.matched_count > 0:
            return self.get_matricula_by_id(matricula_id)
        return None

    def delete_matricula(self, matricula_id: str) -> bool:
        """Elimina una matrícula por ID."""
        from bson import ObjectId
        result = self.collection.delete_one({"_id": ObjectId(matricula_id)})
        return result.deleted_count > 0