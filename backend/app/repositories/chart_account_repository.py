from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class ChartAccountRepository:
    def __init__(self):
        self.collection_name = "chart_accounts"

    async def create(self, db: AsyncIOMotorDatabase, data: dict) -> dict:
        data = data.copy()
        data.setdefault("saldo", 0.0)
        result = await db[self.collection_name].insert_one(data)
        data["id"] = str(result.inserted_id)
        return data

    async def get(self, db: AsyncIOMotorDatabase, account_id: str) -> dict | None:
        try:
            oid = ObjectId(account_id)
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

    async def update_saldo(self, db: AsyncIOMotorDatabase, account_id: str, nuevo_saldo: float) -> dict | None:
        try:
            oid = ObjectId(account_id)
        except:
            return None
        
        await db[self.collection_name].update_one({"_id": oid}, {"$set": {"saldo": nuevo_saldo}})
        return await self.get(db, account_id)
