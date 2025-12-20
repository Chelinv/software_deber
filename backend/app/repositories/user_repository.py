from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class UsuarioRepository:

    def __init__(self):
        self.collection_name = "usuarios"

    async def crear(self, db: AsyncIOMotorDatabase, usuario: dict):
        result = await db[self.collection_name].insert_one(usuario)
        usuario["id"] = str(result.inserted_id)
        return usuario

    async def obtener_todos(self, db: AsyncIOMotorDatabase):
        usuarios = []
        cursor = db[self.collection_name].find({})
        async for document in cursor:
            document["id"] = str(document["_id"])
            usuarios.append(document)
        return usuarios

    async def obtener_por_id(self, db: AsyncIOMotorDatabase, user_id: str):
        try:
            oid = ObjectId(user_id)
        except:
            return None
        document = await db[self.collection_name].find_one({"_id": oid})
        if document:
            document["id"] = str(document["_id"])
        return document

    async def obtener_por_email(self, db: AsyncIOMotorDatabase, email: str):
        document = await db[self.collection_name].find_one({"email": email})
        if document:
            document["id"] = str(document["_id"])
        return document

    async def actualizar(self, db: AsyncIOMotorDatabase, user_id: str, data: dict):
        try:
            oid = ObjectId(user_id)
        except:
            return None
            
        await db[self.collection_name].update_one({"_id": oid}, {"$set": data})
        return await self.obtener_por_id(db, user_id)

    async def eliminar(self, db: AsyncIOMotorDatabase, user_id: str):
        try:
            oid = ObjectId(user_id)
        except:
            return
        await db[self.collection_name].delete_one({"_id": oid})
