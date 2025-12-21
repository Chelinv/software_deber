from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.calificaciones_model import CalificacionCreate, CalificacionOut
from app.repositories.calificaciones_repository import CalificacionesRepository

class CalificacionesService:
    def __init__(self):
        self.repository = CalificacionesRepository()

    async def create_calificacion(self, db: AsyncIOMotorDatabase, calificacion: CalificacionCreate) -> CalificacionOut:
        """Lógica de negocio: Valida y crea una calificación."""
        created_calificacion = await self.repository.create_calificacion(db, calificacion)
        return CalificacionOut(**created_calificacion)

    async def get_all_calificaciones(self, db: AsyncIOMotorDatabase) -> List[CalificacionOut]:
        """Obtiene todas las calificaciones."""
        calificaciones = await self.repository.get_all_calificaciones(db)
        return [CalificacionOut(**calificacion) for calificacion in calificaciones]

    async def get_calificacion_by_id(self, db: AsyncIOMotorDatabase, calificacion_id: str) -> CalificacionOut:
        """Obtiene una calificación por ID."""
        calificacion = await self.repository.get_calificacion_by_id(db, calificacion_id)
        if not calificacion:
            raise ValueError(f"Calificación con ID {calificacion_id} no encontrada")
        return CalificacionOut(**calificacion)

    async def update_calificacion(self, db: AsyncIOMotorDatabase, calificacion_id: str, updated_calificacion: CalificacionCreate) -> CalificacionOut:
        """Actualiza una calificación."""
        updated = await self.repository.update_calificacion(db, calificacion_id, updated_calificacion)
        if not updated:
            raise ValueError(f"Calificación con ID {calificacion_id} no encontrada")
        return CalificacionOut(**updated)

    async def delete_calificacion(self, db: AsyncIOMotorDatabase, calificacion_id: str) -> bool:
        """Elimina una calificación."""
        return await self.repository.delete_calificacion(db, calificacion_id)
