from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.relacion_padre_hijo import RelacionPadreHijoCreate
from datetime import datetime

class RelacionPadreHijoRepository:
    def __init__(self):
        self.collection_name = "relaciones_padre_hijo"
    
    async def crear(self, db: AsyncIOMotorDatabase, relacion: RelacionPadreHijoCreate):
        """Crear una nueva relación padre-hijo"""
        relacion_dict = relacion.model_dump()
        relacion_dict["fecha_creacion"] = datetime.now().isoformat()
        
        result = await db[self.collection_name].insert_one(relacion_dict)
        relacion_dict["id"] = str(result.inserted_id)
        relacion_dict["_id"] = str(result.inserted_id)
        return relacion_dict
    
    async def obtener_por_padre(self, db: AsyncIOMotorDatabase, padre_id: str):
        """Obtener el estudiante asociado a un padre"""
        relacion = await db[self.collection_name].find_one({"padre_id": padre_id})
        if relacion:
            relacion["id"] = str(relacion["_id"])
            relacion["_id"] = str(relacion["_id"])
        return relacion
    
    async def obtener_por_estudiante(self, db: AsyncIOMotorDatabase, estudiante_id: str):
        """Obtener el padre asociado a un estudiante"""
        relacion = await db[self.collection_name].find_one({"estudiante_id": estudiante_id})
        if relacion:
            relacion["id"] = str(relacion["_id"])
            relacion["_id"] = str(relacion["_id"])
        return relacion
    
    async def eliminar(self, db: AsyncIOMotorDatabase, relacion_id: str):
        """Eliminar una relación padre-hijo"""
        from bson import ObjectId
        result = await db[self.collection_name].delete_one({"_id": ObjectId(relacion_id)})
        return result.deleted_count > 0
    
    async def actualizar(self, db: AsyncIOMotorDatabase, padre_id: str, estudiante_id: str):
        """Actualizar o crear relación para un padre"""
        # Primero eliminar cualquier relación existente del padre
        await db[self.collection_name].delete_many({"padre_id": padre_id})
        
        # Crear nueva relación
        relacion = RelacionPadreHijoCreate(padre_id=padre_id, estudiante_id=estudiante_id)
        return await self.crear(db, relacion)
