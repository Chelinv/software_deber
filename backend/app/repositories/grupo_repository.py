from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class GrupoRepository:
    def __init__(self):
        self.collection_name = "grupos"

    async def crear(self, db: AsyncIOMotorDatabase, grupo: dict) -> dict:
        result = await db[self.collection_name].insert_one(grupo)
        grupo["id"] = str(result.inserted_id)
        return grupo

    async def listar(self, db: AsyncIOMotorDatabase) -> list:
        grupos = []
        cursor = db[self.collection_name].find({})
        async for document in cursor:
            document["id"] = str(document["_id"])
            grupos.append(document)
        return grupos
