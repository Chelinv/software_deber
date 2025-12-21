from typing import List, Optional
from app.models.calificaciones_model import CalificacionBase

class CalificacionesRepository:
    def __init__(self, db):
        self.collection = db["calificaciones"]

    def get_all_calificaciones(self) -> List[CalificacionBase]:
        """Obtiene todas las calificaciones."""
        docs = self.collection.find()
        calificaciones = []
        for doc in docs:
            doc['id'] = str(doc.pop('_id'))  # Mapea _id a id como str
            calificaciones.append(CalificacionBase(**doc))
        return calificaciones

    def get_calificacion_by_id(self, calificacion_id: str) -> Optional[CalificacionBase]:
        """Obtiene una calificación por ID."""
        from bson import ObjectId
        doc = self.collection.find_one({"_id": ObjectId(calificacion_id)})
        if doc:
            doc['id'] = str(doc.pop('_id'))
            return CalificacionBase(**doc)
        return None

    def create_calificacion(self, calificacion: CalificacionBase) -> CalificacionBase:
        """Crea una nueva calificación."""
        doc = calificacion.dict(exclude={"id"})
        result = self.collection.insert_one(doc)
        calificacion.id = str(result.inserted_id)
        return calificacion

    def update_calificacion(self, calificacion_id: str, updated_calificacion: CalificacionBase) -> Optional[CalificacionBase]:
        """Actualiza una calificación."""
        from bson import ObjectId
        doc = updated_calificacion.dict(exclude={"id"})
        result = self.collection.update_one({"_id": ObjectId(calificacion_id)}, {"$set": doc})
        if result.matched_count > 0:
            return self.get_calificacion_by_id(calificacion_id)
        return None

    def delete_calificacion(self, calificacion_id: str) -> bool:
        """Elimina una calificación por ID."""
        from bson import ObjectId
        result = self.collection.delete_one({"_id": ObjectId(calificacion_id)})
        return result.deleted_count > 0