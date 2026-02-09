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

    async def actualizar(self, db: AsyncIOMotorDatabase, asignatura_id: str, nombre: str, codigo: str):
        asignatura = AsignaturaCreate(nombre=nombre, codigo=codigo)
        return await self.repo.actualizar(db, asignatura_id, asignatura)

    async def eliminar(self, db: AsyncIOMotorDatabase, asignatura_id: str):
        # PASO 1: Eliminar la asignatura de la BD
        result = await self.repo.eliminar(db, asignatura_id)
        
        # PASO 2: Limpiar referencias en matrículas (CASCADE DELETE)
        # Buscar todas las matrículas que contengan esta asignatura
        matriculas_cursor = db["matriculas"].find({"asignatura_ids": asignatura_id})
        
        matriculas_actualizadas = 0
        matriculas_eliminadas = 0
        
        async for matricula in matriculas_cursor:
            # Remover el ID de la asignatura eliminada
            asignatura_ids = matricula.get("asignatura_ids", [])
            asignatura_ids_nuevos = [aid for aid in asignatura_ids if aid != asignatura_id]
            
            if len(asignatura_ids_nuevos) > 0:
                # Si quedan asignaturas, actualizar la matrícula
                await db["matriculas"].update_one(
                    {"_id": matricula["_id"]},
                    {"$set": {"asignatura_ids": asignatura_ids_nuevos}}
                )
                matriculas_actualizadas += 1
            else:
                # Si no quedan asignaturas, eliminar la matrícula completa
                await db["matriculas"].delete_one({"_id": matricula["_id"]})
                matriculas_eliminadas += 1
        
        print(f"[CASCADE DELETE] Asignatura {asignatura_id} eliminada")
        print(f"  - Matriculas actualizadas: {matriculas_actualizadas}")
        print(f"  - Matriculas eliminadas: {matriculas_eliminadas}")
        
        return result

