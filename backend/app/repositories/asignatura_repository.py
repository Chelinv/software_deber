from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.asignatura import AsignaturaCreate

class AsignaturaRepository:
    def __init__(self):
        self.collection_name = "asignaturas"

    async def crear(self, db: AsyncIOMotorDatabase, asignatura: AsignaturaCreate):
        asignatura_dict = asignatura.model_dump()
        result = await db[self.collection_name].insert_one(asignatura_dict)
        asignatura_dict["_id"] = str(result.inserted_id)
        return {**asignatura_dict, "id": str(result.inserted_id)}

    async def listar(self, db: AsyncIOMotorDatabase):
        asignaturas = []
        cursor = db[self.collection_name].find({})
        async for document in cursor:
            document["id"] = str(document["_id"])
            asignaturas.append(document)
        return asignaturas
