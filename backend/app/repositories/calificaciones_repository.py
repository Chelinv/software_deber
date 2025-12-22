from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.calificaciones_model import CalificacionCreate
from typing import List, Optional
from bson import ObjectId

class CalificacionesRepository:
    def __init__(self):
        self.collection_name = "calificaciones"

    async def get_all_calificaciones(self, db: AsyncIOMotorDatabase) -> List[dict]:
        """Obtiene todas las calificaciones."""
        cursor = db[self.collection_name].find()
        calificaciones = []
        async for doc in cursor:
            doc['id'] = str(doc['_id'])
            calificaciones.append(doc)
        return calificaciones

    async def get_calificacion_by_id(self, db: AsyncIOMotorDatabase, calificacion_id: str) -> Optional[dict]:
        """Obtiene una calificación por ID."""
        try:
            oid = ObjectId(calificacion_id)
        except:
            return None
        doc = await db[self.collection_name].find_one({"_id": oid})
        if doc:
            doc['id'] = str(doc['_id'])
            return doc
        return None

    async def create_calificacion(self, db: AsyncIOMotorDatabase, calificacion: CalificacionCreate) -> dict:
        """Crea una nueva calificación."""
        doc = calificacion.model_dump()
        result = await db[self.collection_name].insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return {**doc, "id": str(result.inserted_id)}

    async def update_calificacion(self, db: AsyncIOMotorDatabase, calificacion_id: str, updated_calificacion: CalificacionCreate) -> Optional[dict]:
        """Actualiza una calificación."""
        try:
            oid = ObjectId(calificacion_id)
        except:
            return None
        doc = updated_calificacion.model_dump()
        result = await db[self.collection_name].update_one({"_id": oid}, {"$set": doc})
        if result.matched_count > 0:
            return await self.get_calificacion_by_id(db, calificacion_id)
        return None

    async def delete_calificacion(self, db: AsyncIOMotorDatabase, calificacion_id: str) -> bool:
        """Elimina una calificación por ID."""
        try:
            oid = ObjectId(calificacion_id)
        except:
            return False
        result = await db[self.collection_name].delete_one({"_id": oid})
        return result.deleted_count > 0
