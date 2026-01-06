from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.matricula_model import MatriculaCreate
from typing import List, Optional
from bson import ObjectId

class MatriculaRepository:
    def __init__(self):
        self.collection_name = "matriculas"

    async def get_all_matriculas(self, db: AsyncIOMotorDatabase) -> List[dict]:
        """Obtiene todas las matrículas."""
        cursor = db[self.collection_name].find()
        matriculas = []
        async for doc in cursor:
            doc['id'] = str(doc['_id'])
            doc['_id'] = str(doc['_id'])
            matriculas.append(doc)
        return matriculas

    async def get_matricula_by_id(self, db: AsyncIOMotorDatabase, matricula_id: str) -> Optional[dict]:
        """Obtiene una matrícula por ID."""
        try:
            oid = ObjectId(matricula_id)
        except:
            return None
        doc = await db[self.collection_name].find_one({"_id": oid})
        if doc:
            doc['id'] = str(doc['_id'])
            doc['_id'] = str(doc['_id'])
            return doc
        return None

    async def create_matricula(self, db: AsyncIOMotorDatabase, matricula: MatriculaCreate) -> dict:
        """Crea una nueva matrícula."""
        doc = matricula.model_dump()
        result = await db[self.collection_name].insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return {**doc, "id": str(result.inserted_id)}

    async def update_matricula(self, db: AsyncIOMotorDatabase, matricula_id: str, updated_matricula: MatriculaCreate) -> Optional[dict]:
        """Actualiza una matrícula."""
        try:
            oid = ObjectId(matricula_id)
        except:
            return None
        doc = updated_matricula.model_dump()
        result = await db[self.collection_name].update_one({"_id": oid}, {"$set": doc})
        if result.matched_count > 0:
            return await self.get_matricula_by_id(db, matricula_id)
        return None

    async def delete_matricula(self, db: AsyncIOMotorDatabase, matricula_id: str) -> bool:
        """Elimina una matrícula por ID."""
        try:
            oid = ObjectId(matricula_id)
        except:
            return False
        result = await db[self.collection_name].delete_one({"_id": oid})
        return result.deleted_count > 0
