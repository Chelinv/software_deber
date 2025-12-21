from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.asignatura_service import AsignaturaService

class AsignaturaController:
    def __init__(self):
        self.service = AsignaturaService()

    async def crear(self, db: AsyncIOMotorDatabase, nombre: str, codigo: str):
        return await self.service.crear(db, nombre, codigo)

    async def listar(self, db: AsyncIOMotorDatabase):
        return await self.service.listar(db)
