from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.grupo import GrupoCreate

class GrupoRepository:
    def __init__(self):
        self.collection_name = "grupos"

    async def crear(self, db: AsyncIOMotorDatabase, grupo: GrupoCreate):
        grupo_dict = grupo.model_dump()
        result = await db[self.collection_name].insert_one(grupo_dict)
        return {**grupo_dict, "id": str(result.inserted_id)}

    async def listar(self, db: AsyncIOMotorDatabase):
        grupos = []
        cursor = db[self.collection_name].find({})
        async for document in cursor:
            document["id"] = str(document["_id"])
            grupos.append(document)
        return grupos
