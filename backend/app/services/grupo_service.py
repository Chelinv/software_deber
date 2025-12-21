from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.grupo_repository import GrupoRepository
from app.models.grupo import GrupoCreate

class GrupoService:
    def __init__(self):
        self.repo = GrupoRepository()

    async def crear(self, db: AsyncIOMotorDatabase, nombre: str, aula: str, asignatura_id: str, docente_id: str):
        grupo = GrupoCreate(
            nombre=nombre,
            aula=aula,
            asignatura_id=asignatura_id,
            docente_id=docente_id
        )
        return await self.repo.crear(db, grupo)

    async def listar(self, db: AsyncIOMotorDatabase):
        return await self.repo.listar(db)
