from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.matricula_model import MatriculaCreate, MatriculaOut
from app.repositories.matricula_repository import MatriculaRepository
from bson import ObjectId

class MatriculaService:
    def __init__(self):
        self.repository = MatriculaRepository()

    async def create_matricula(self, db: AsyncIOMotorDatabase, matricula: MatriculaCreate, current_user: dict = None) -> MatriculaOut:
        """Lógica de negocio: Valida y crea una matrícula con validación de duplicados."""
        # Validación básica
        if not matricula.estudiante_id:
            raise ValueError("estudiante_id es requerido")
        
        if not matricula.asignatura_ids or len(matricula.asignatura_ids) == 0:
            raise ValueError("Debe seleccionar al menos una asignatura")
        
        # VALIDACIÓN DE DUPLICADOS: Verificar si el estudiante ya está inscrito en alguna materia
        existing_matricula = await db.matriculas.find_one({"estudiante_id": matricula.estudiante_id})
        
        if existing_matricula:
            # El estudiante ya tiene una matrícula, verificar duplicados
            existing_subjects = set(existing_matricula.get("asignatura_ids", []))
            new_subjects = set(matricula.asignatura_ids)
            
            # Encontrar materias duplicadas
            duplicates = existing_subjects & new_subjects
            
            if duplicates:
                # Obtener nombres de las materias duplicadas para el mensaje de error
                duplicate_names = []
                for asig_id in duplicates:
                    asignatura = await db.asignaturas.find_one({"_id": ObjectId(asig_id)})
                    if asignatura:
                        duplicate_names.append(asignatura.get("nombre", asig_id))
                
                raise ValueError(f"El estudiante ya está inscrito en: {', '.join(duplicate_names)}")
            
            # Combinar materias existentes con nuevas (sin duplicados)
            updated_subjects = list(existing_subjects | new_subjects)
            
            # Actualizar la matrícula existente
            result = await db.matriculas.update_one(
                {"_id": ObjectId(existing_matricula["_id"])},
                {"$set": {"asignatura_ids": updated_subjects}}
            )
            
            # Obtener la matrícula actualizada
            updated_matricula = await db.matriculas.find_one({"_id": ObjectId(existing_matricula["_id"])})
            updated_matricula["id"] = str(updated_matricula["_id"])
            return MatriculaOut(**updated_matricula)
        else:
            # No existe matrícula previa, crear una nueva
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
