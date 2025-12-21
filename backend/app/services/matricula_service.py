from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.matricula_model import MatriculaCreate, MatriculaOut
from app.repositories.matricula_repository import MatriculaRepository

class MatriculaService:
    def __init__(self):
        self.repository = MatriculaRepository()

    async def create_matricula(self, db: AsyncIOMotorDatabase, matricula: MatriculaCreate) -> MatriculaOut:
        """Lógica de negocio: Valida y crea una matrícula."""
        # Validación básica (ejemplo)
        if matricula.estudiante_id <= 0 or matricula.asignatura_id <= 0:
            raise ValueError("estudiante_id y asignatura_id deben ser positivos")
        created_matricula = await self.repository.create_matricula(db, matricula)
        return MatriculaOut(**created_matricula)

    async def get_all_matriculas(self, db: AsyncIOMotorDatabase) -> List[MatriculaOut]:
        """Obtiene todas las matrículas."""
        matriculas = await self.repository.get_all_matriculas(db)
        return [MatriculaOut(**matricula) for matricula in matriculas]

    async def get_matricula_by_id(self, db: AsyncIOMotorDatabase, matricula_id: str) -> MatriculaOut:
        """Obtiene una matrícula por ID."""
        matricula = await self.repository.get_matricula_by_id(db, matricula_id)
        if not matricula:
            raise ValueError(f"Matrícula con ID {matricula_id} no encontrada")
        return MatriculaOut(**matricula)

    async def update_matricula(self, db: AsyncIOMotorDatabase, matricula_id: str, updated_matricula: MatriculaCreate) -> MatriculaOut:
        """Actualiza una matrícula."""
        updated = await self.repository.update_matricula(db, matricula_id, updated_matricula)
        if not updated:
            raise ValueError(f"Matrícula con ID {matricula_id} no encontrada")
        return MatriculaOut(**updated)

    async def delete_matricula(self, db: AsyncIOMotorDatabase, matricula_id: str) -> bool:
        """Elimina una matrícula."""
        return await self.repository.delete_matricula(db, matricula_id)
