from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class TransactionRepository:
    def __init__(self):
        self.collection_name = "transactions"

    async def create(self, db: AsyncIOMotorDatabase, data: dict) -> dict:
        result = await db[self.collection_name].insert_one(data)
        data["id"] = str(result.inserted_id)
        return data

    async def get(self, db: AsyncIOMotorDatabase, transaction_id: str) -> dict | None:
        try:
            oid = ObjectId(transaction_id)
        except:
            return None
        doc = await db[self.collection_name].find_one({"_id": oid})
        if doc:
            doc["id"] = str(doc["_id"])
        return doc

    async def list(self, db: AsyncIOMotorDatabase) -> list[dict]:
        docs = []
        async for doc in db[self.collection_name].find({}):
            doc["id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def update(self, db: AsyncIOMotorDatabase, transaction_id: str, data: dict) -> dict | None:
        try:
            oid = ObjectId(transaction_id)
        except:
            return None
        
        await db[self.collection_name].update_one({"_id": oid}, {"$set": data})
        return await self.get(db, transaction_id)
