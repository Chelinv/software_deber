from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.asignatura_repository import AsignaturaRepository

class AsignaturaService:

    def __init__(self):
        self.repo = AsignaturaRepository()

    async def crear(self, db: AsyncIOMotorDatabase, nombre: str, codigo: str):
        asignatura_data = {
            "nombre": nombre,
            "codigo": codigo
        }
        return await self.repo.crear(db, asignatura_data)

    async def listar(self, db: AsyncIOMotorDatabase):
        return await self.repo.listar(db)
