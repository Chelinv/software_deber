from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.grupo_service import GrupoService

class GrupoController:

    def __init__(self):
        self.service = GrupoService()

    async def crear(self, db: AsyncIOMotorDatabase, nombre: str, aula: str, asignatura_id: str, docente_id: str):
        return await self.service.crear(
            db, nombre, aula, asignatura_id, docente_id
        )

    async def listar(self, db: AsyncIOMotorDatabase):
        return await self.service.listar(db)
