from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.asignatura_repository import AsignaturaRepository
from app.models.asignatura import AsignaturaCreate

class AsignaturaService:
    def __init__(self):
        self.repo = AsignaturaRepository()

    async def crear(self, db: AsyncIOMotorDatabase, nombre: str, codigo: str):
        asignatura = AsignaturaCreate(nombre=nombre, codigo=codigo)
        return await self.repo.crear(db, asignatura)

    async def listar(self, db: AsyncIOMotorDatabase):
        return await self.repo.listar(db)
