from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class AsignaturaRepository:
    def __init__(self):
        self.collection_name = "asignaturas"

    async def crear(self, db: AsyncIOMotorDatabase, asignatura: dict) -> dict:
        result = await db[self.collection_name].insert_one(asignatura)
        asignatura["id"] = str(result.inserted_id)
        return asignatura

    async def listar(self, db: AsyncIOMotorDatabase) -> list:
        asignaturas = []
        cursor = db[self.collection_name].find({})
        async for document in cursor:
            document["id"] = str(document["_id"])
            asignaturas.append(document)
        return asignaturas
