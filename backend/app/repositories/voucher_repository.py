from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class VoucherRepository:
    def __init__(self):
        self.collection_name = "vouchers"

    async def create(self, db: AsyncIOMotorDatabase, data: dict) -> dict:
        result = await db[self.collection_name].insert_one(data)
        data["id"] = str(result.inserted_id)
        return data

    async def get(self, db: AsyncIOMotorDatabase, voucher_id: str) -> dict | None:
        try:
            oid = ObjectId(voucher_id)
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
