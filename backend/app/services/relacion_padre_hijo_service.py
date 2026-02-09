from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.relacion_padre_hijo_repository import RelacionPadreHijoRepository
from app.models.relacion_padre_hijo import RelacionPadreHijoCreate

class RelacionPadreHijoService:
    def __init__(self):
        self.repo = RelacionPadreHijoRepository()
    
    async def crear_relacion(self, db: AsyncIOMotorDatabase, padre_id: str, estudiante_id: str):
        """Crear o actualizar relación padre-hijo"""
        # Validar que el padre no esté ya asociado a otro estudiante
        relacion_existente = await self.repo.obtener_por_padre(db, padre_id)
        
        if relacion_existente:
            # Actualizar relación existente
            return await self.repo.actualizar(db, padre_id, estudiante_id)
        else:
            # Crear nueva relación
            relacion = RelacionPadreHijoCreate(padre_id=padre_id, estudiante_id=estudiante_id)
            return await self.repo.crear(db, relacion)
    
    async def obtener_hijo_de_padre(self, db: AsyncIOMotorDatabase, padre_id: str):
        """Obtener el ID del estudiante asociado a un padre"""
        relacion = await self.repo.obtener_por_padre(db, padre_id)
        return relacion.get("estudiante_id") if relacion else None
    
    async def obtener_padre_de_estudiante(self, db: AsyncIOMotorDatabase, estudiante_id: str):
        """Obtener el ID del padre asociado a un estudiante"""
        relacion = await self.repo.obtener_por_estudiante(db, estudiante_id)
        return relacion.get("padre_id") if relacion else None
    
    async def verificar_relacion(self, db: AsyncIOMotorDatabase, padre_id: str, estudiante_id: str):
        """Verificar si existe relación entre padre e hijo"""
        relacion = await self.repo.obtener_por_padre(db, padre_id)
        if not relacion:
            return False
        return relacion.get("estudiante_id") == estudiante_id
