from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.asignatura import AsignaturaCreate

class AsignaturaRepository:
    def __init__(self):
        self.collection_name = "asignaturas"

    async def crear(self, db: AsyncIOMotorDatabase, asignatura: AsignaturaCreate):
        asignatura_dict = asignatura.model_dump()
        result = await db[self.collection_name].insert_one(asignatura_dict)
        # Convert ObjectId to str for the response
        asignatura_dict["_id"] = str(result.inserted_id)
        asignatura_dict["id"] = str(result.inserted_id)
        return asignatura_dict

    async def listar(self, db: AsyncIOMotorDatabase):
        asignaturas = []
        cursor = db[self.collection_name].find({})
        async for document in cursor:
            # Convert ObjectId to string to avoid serialization error
            document["id"] = str(document["_id"])
            # Remove _id to clean up response if needed, but Pydantic alias="_id" handles it if present
            # However, the error 'ObjectId' object is not iterable suggests direct return of dict with ObjectId
            # So we ensure _id is handled or removed if causing issues
            if "_id" in document:
                document["_id"] = str(document["_id"])
            asignaturas.append(document)
        return asignaturas
